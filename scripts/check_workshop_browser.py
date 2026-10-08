"""Capture the current atlas example or inspect the rendered workshop locally."""
import argparse
import asyncio
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--capture-atlas',action='store_true')
parser.add_argument('--site-dir',type=Path,default=ROOT/'docs')
args=parser.parse_args()

async def main():
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
        page=await browser.new_page(viewport={'width':1440,'height':1000})
        if args.capture_atlas:
            await page.goto('https://jimclifford.ca/col_matching/?p=kgp_col1878-p447b3',wait_until='domcontentloaded')
            await page.wait_for_function("window.ATLAS?.App.careers && document.querySelectorAll('.ros-entry').length>0",timeout=60000)
            await page.wait_for_timeout(1000)
            await page.screenshot(path=str(ROOT/'images/atlas-wodehouse-repaired.png'))
            print('Saved current Wodehouse atlas image.')
        else:
            handler=partial(SimpleHTTPRequestHandler,directory=str(args.site_dir))
            server=ThreadingHTTPServer(('127.0.0.1',0),handler)
            Thread(target=server.serve_forever,daemon=True).start()
            base=f'http://127.0.0.1:{server.server_port}'
            errors=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            await page.goto(base+'/slides.html',wait_until='networkidle')
            await page.wait_for_function('window.Reveal?.isReady()')
            await page.evaluate("() => {const s=[...document.querySelectorAll('.reveal .slides > section')];Reveal.slide(s.findIndex(x=>x.id==='cross-service-career'));}")
            await page.wait_for_timeout(400)
            await page.screenshot(path='/tmp/workshop-cross-service-slide.png')
            bounds=await page.evaluate("""() => {
              const s=Reveal.getCurrentSlide(),r=s.getBoundingClientRect();
              return {bottom:r.bottom,height:innerHeight,text:s.innerText};
            }""")
            assert bounds['bottom'] <= bounds['height'],bounds
            assert 'One career across two Lists' in bounds['text']
            titles=[
                'Read records against the source',
                'Replay a past correction',
                'Same entries, different workflows',
                'A past repair: which Victoria?',
                'A past repair: what counts as an event?',
                'Three decisions, with reasons',
            ]
            await page.evaluate("Reveal.configure({transition:'none'})")
            for title in titles:
                index=await page.evaluate("title => [...document.querySelectorAll('.reveal .slides > section')].findIndex(s=>s.querySelector('h2')?.textContent===title)",title)
                assert index>=0,title
                await page.evaluate('index => Reveal.slide(index)',index)
                await page.wait_for_timeout(100)
                bounds=await page.evaluate("""() => {
                    const s=Reveal.getCurrentSlide(),r=s.getBoundingClientRect();
                    return {bottom:r.bottom,height:innerHeight,title:s.querySelector('h2').textContent};
                }""")
                assert bounds['bottom'] <= bounds['height'],bounds
                await page.screenshot(path=f'/tmp/workshop-slide-{index}.png')
            await page.goto(base+'/steps/01-atlas.html',wait_until='networkidle')
            img=page.locator('img[src$="atlas-wodehouse-repaired.png"]')
            assert await img.evaluate('(e)=>e.complete && e.naturalWidth>0')
            await img.scroll_into_view_if_needed()
            await page.screenshot(path='/tmp/workshop-rebuilt-example.png')
            await page.goto(base+'/presenter.html',wait_until='networkidle')
            assert 'Completed repairs as teaching examples' in await page.locator('body').inner_text()
            assert 'unfinished repairs' not in await page.locator('body').inner_text()
            assert not errors,errors
            server.shutdown()
            print('Seven revised slides, rebuilt image and presenter notes passed; no browser errors.')
        await browser.close()

if __name__=='__main__':asyncio.run(main())
