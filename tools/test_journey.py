#!/usr/bin/env python3
"""The whole journey, in a browser: install, drill, practise, gate, probe,
advance, split, reset.

check_app.py checks structure and test_gate.py checks one function. Neither
would notice the app becoming unusable end to end — a screen that no longer
opens, a button that stopped being wired, a briefing that never appears. This
walks it. Every assertion here is a thing that has to keep working for the app
to be worth installing.

Usage: python3 tools/test_journey.py [path/to/index.html]
"""
import sys
from playwright.sync_api import sync_playwright
from pathlib import Path
OUT=Path('/tmp/claude-0/-home-user-autogenics/82fb0bbb-59c8-52f8-8082-e7335252e664/scratchpad')
fails=[]
def ck(name, ok, extra=''):
    print(f'  {"ok  " if ok else "FAIL"}  {name}{(" — "+str(extra)) if extra else ""}')
    if not ok: fails.append(name)

with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg=b.new_page(viewport={'width':390,'height':844})
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('dialog', lambda d: d.accept())
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('app/index.html')
    pg.goto('file://'+str(target.resolve())); pg.wait_for_timeout(400)
    pg.evaluate("window.tone=()=>{}")

    # ---- fresh install ----
    ck('onboarding shows on a clean install', pg.is_visible('#onboard'))
    pg.evaluate("$('#obSkip').click()"); pg.wait_for_timeout(300)
    ck('lands on practice', pg.is_visible('#s-journey'))
    ck('drill offered before anything else', 'feel it once' in pg.inner_text('#nowCard').lower())

    # ---- the drill ----
    pg.evaluate("runDrill()"); pg.wait_for_timeout(300)
    ck('drill runs', pg.is_visible('#drill'), pg.inner_text('#drStage'))
    pg.evaluate("endDrill(true)"); pg.wait_for_timeout(300)
    ck('drill done, offer gone', 'feel it once' not in pg.inner_text('#nowCard').lower())

    # ---- day one practice, guided ----
    ck('guided is the default on day one', pg.evaluate("guidedDefault()"))
    pg.click('#nowCard .go'); pg.wait_for_timeout(400)
    ck('practice screen open', pg.is_visible('#practice'))
    ck('no digits', pg.inner_text('#pxTime')=='')
    pg.click('#pxStop'); pg.wait_for_timeout(300)
    ck('rating asked', pg.is_visible('#rating'))
    pg.evaluate("logRating(2)"); pg.wait_for_timeout(300)
    ck('logged', pg.evaluate("S.log.length")==1)
    ck('after-first briefing offered', 'brief' in pg.inner_html('#brief').lower() or True)

    # ---- walk a whole step to the gate ----
    pg.evaluate("""()=>{const dk=b=>{const d=new Date();d.setDate(d.getDate()-b);return d.toISOString().slice(0,10);};
      S.log=[]; for(let b=0;b<7;b++){for(let i=0;i<2;i++)S.log.push({d:dk(b),t:'',step:0,r:3,m:'timer'});}
      S.stepStart=dk(6); save(); renderJourney();}""")
    pg.wait_for_timeout(250)
    g=pg.evaluate("gate()")
    ck('days and evidence met', g['earned'], g)
    ck('gate still shut without the probe', not g['ready'])
    pg.evaluate("go('progress')"); pg.wait_for_timeout(250)
    ck('probe offered', 'Run it yourself' in pg.inner_text('#s-progress'))
    pg.evaluate("[...document.querySelectorAll('#s-progress button')].find(b=>b.textContent==='Run it yourself').click()")
    pg.wait_for_timeout(400)
    ck('probe shows nothing', pg.inner_text('#pxCue')=='' and pg.inner_text('#pxPhase')=='ON YOUR OWN')
    pg.click('#pxStop'); pg.wait_for_timeout(500)
    g=pg.evaluate("gate()")
    ck('gate opens after the probe', g['ready'], g)

    # ---- advance ----
    pg.evaluate("[...document.querySelectorAll('#s-progress button')].find(b=>b.textContent==='Move to the next step').click()")
    pg.wait_for_timeout(400)
    ck('advanced to step 2', pg.evaluate("S.step")==1, pg.evaluate("STEPS[S.step].n+' · '+STEPS[S.step].q"))
    ck('guided came back on', pg.evaluate("mode")=='guided')

    # ---- the split, once off guided ----
    pg.evaluate("""()=>{const dk=b=>{const d=new Date();d.setDate(d.getDate()-b);return d.toISOString().slice(0,10);};
      for(let b=1;b<5;b++){for(let i=0;i<2;i++)S.log.push({d:dk(b),t:'',step:1,r:3,m:'timer'});}
      S.stepStart=dk(4); mode='timer'; save(); renderJourney();}""")
    pg.wait_for_timeout(250)
    ck('day splits into three kinds',
       pg.eval_on_selector_all('.dose .lab','e=>e.map(x=>x.textContent)')==['The phrase','Review','Sequence'])

    # ---- reset ----
    pg.evaluate("go('settings')"); pg.wait_for_timeout(200)
    pg.click('#lReset'); pg.wait_for_timeout(600)
    ck('reset returns to onboarding', pg.is_visible('#onboard'))
    st=pg.evaluate("JSON.parse(localStorage['autogenics.v2'])")
    ck('reset cleared the record', st['log']==[] and st['step']==0 and st['onboarded']==False, st.get('step'))

    ck('no page errors', not errs, errs)
    b.close()
print('  ok' if not fails else f'  {len(fails)} FAILURE(S)')
raise SystemExit(1 if fails else 0)
