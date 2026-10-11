"""Check rendered workshop pages, touch exercises and slide reading view."""
import asyncio
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def copyfile(self, source, outputfile):
        try:
            super().copyfile(source, outputfile)
        except (BrokenPipeError, ConnectionResetError):
            pass


async def assert_fits(page, label):
    bounds = await page.evaluate("""() => ({
      viewport: innerWidth, content: document.documentElement.scrollWidth,
      offenders: [...document.querySelectorAll('main table, main pre, .entry, .toolbar, .reveal .slides > section')]
        .filter(e => e.getBoundingClientRect().right > innerWidth + 1)
        .map(e => ({tag: e.tagName, text: e.innerText.slice(0, 80)}))
    })""")
    assert bounds['content'] <= bounds['viewport'] + 1, (label, bounds)


async def main():
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT / 'docs')))
    Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}'
    errors = []
    routes = [str(p.relative_to(ROOT / 'docs')) for p in (ROOT / 'docs').glob('*.html')]
    routes += [str(p.relative_to(ROOT / 'docs')) for p in (ROOT / 'docs' / 'steps').glob('*.html')]
    routes += ['review/index.html', 'annotate/index.html']
    screenshots = Path('/tmp/workshop-responsive')
    screenshots.mkdir(exist_ok=True)
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-dev-shm-usage'])
            page = await browser.new_page(has_touch=True)
            page.on('pageerror', lambda error: errors.append(str(error)))
            # The saved video is checked separately; avoid requiring the public MP4.
            await page.route('**/*', lambda route: route.continue_() if route.request.url.startswith(base) and route.request.resource_type != 'media' else route.abort())
            checks = 0
            for width, height in [(320, 740), (390, 844), (768, 1024), (1024, 768), (1440, 900)]:
                await page.set_viewport_size({'width': width, 'height': height})
                for route in routes:
                    response = await page.goto(base + '/' + route, wait_until='networkidle')
                    assert response.status == 200, route
                    if route == 'slides.html':
                        await page.wait_for_function('window.Reveal?.isReady()')
                        reading = width <= 1024
                        await page.wait_for_function('expected => document.documentElement.classList.contains("workshop-reading") === expected', arg=reading)
                        if reading:
                            assert await page.locator('.reveal .slides > section:visible').count() == await page.evaluate('Reveal.getTotalSlides()')
                            assert await page.locator('.reveal .slides > section[aria-hidden="true"]').count() == 0
                            size = await page.locator('.reveal .slides > section p').first.evaluate('(e) => parseFloat(getComputedStyle(e).fontSize)')
                            assert size >= 16, (width, size)
                            assert not await page.locator('.workshop-reading-nav').is_hidden()
                            assert await page.locator('.reveal .fragment').first.is_visible()
                            image = page.locator('img[src$="qr-review.png"]')
                            await image.scroll_into_view_if_needed()
                            await page.wait_for_function("""document.querySelector('img[src$="qr-review.png"]')?.naturalWidth > 0""")
                        else:
                            assert await page.locator('.workshop-reading-nav').is_hidden()
                    elif route == 'index.html':
                        toggle = page.locator('.navbar-toggler')
                        if await toggle.is_visible():
                            await toggle.tap()
                            await page.locator('#navbarCollapse').wait_for(state='visible')
                            await page.locator('#navbarCollapse .dropdown-toggle').first.tap()
                            assert await page.locator('#navbarCollapse .dropdown-menu').first.is_visible()
                            await toggle.tap()
                    elif route == 'review/index.html':
                        await page.locator('#r_R8').wait_for()
                        await page.locator('input[name="d_R8"][value="accept"]').check()
                        await page.locator('#r_R8').fill('The career matches; preserve the disputed date.')
                        await page.reload(wait_until='networkidle')
                        assert await page.locator('input[name="d_R8"][value="accept"]').is_checked()
                        assert 'career matches' in await page.locator('#r_R8').input_value()
                        await page.locator('#cases details').evaluate('(e) => e.open = true')
                    elif route == 'annotate/index.html':
                        await page.locator('#entry .w').first.wait_for()
                        await page.locator('#entry .w').nth(0).tap()
                        await page.locator('#entry .w').nth(1).tap()
                        await page.locator('#btnCompare').tap()
                        assert await page.locator('#mine td').count() == 2
                        entries = await page.locator('#pick option').count()
                        for i in range(entries):
                            await page.locator('#pick').select_option(str(i))
                            await page.locator('#btnCompare').click()
                            await page.wait_for_function('document.querySelectorAll("#theirs table:not(.workshop-table)").length === 0')
                            await assert_fits(page, f'{route}, entry {i}, {width}px')
                    await assert_fits(page, f'{route}, {width}px')
                    checks += 1
                    if width in [390, 768] and route in ['index.html', 'slides.html', 'annotate/index.html', 'review/index.html']:
                        if route == 'slides.html':
                            await page.locator('#live-three-searches').scroll_into_view_if_needed()
                        else:
                            await page.evaluate('scrollTo(0,0)')
                        await page.screenshot(path=str(screenshots / f'{width}-{route.replace("/", "-")}.png'))
                print(f'{width}px: all {len(routes)} pages and {entries} annotation comparisons fit.', flush=True)
            # A projector or scaled laptop at 1024 pixels with a mouse must keep presentation mode and keyboard control.
            desk = await browser.new_page(viewport={'width': 1024, 'height': 768})
            await desk.goto(base + '/slides.html', wait_until='networkidle')
            await desk.wait_for_function('window.Reveal?.isReady()')
            await desk.wait_for_timeout(300)
            assert not await desk.evaluate('document.documentElement.classList.contains("workshop-reading")')
            assert await desk.evaluate('Reveal.getConfig().keyboard')
            await desk.close()
            phone = await browser.new_page(has_touch=True, viewport={'width': 390, 'height': 844})
            await phone.goto(base + '/slides.html?present', wait_until='networkidle')
            await phone.wait_for_function('window.Reveal?.isReady()')
            await phone.wait_for_timeout(300)
            assert not await phone.evaluate('document.documentElement.classList.contains("workshop-reading")')
            await phone.close()

            # Switching between reading and presentation modes must restore the deck.
            await page.goto(base + '/slides.html', wait_until='networkidle')
            await page.wait_for_function('window.Reveal?.isReady()')
            await page.set_viewport_size({'width': 390, 'height': 844})
            await page.wait_for_function('document.documentElement.classList.contains("workshop-reading")')
            await page.set_viewport_size({'width': 1440, 'height': 900})
            await page.wait_for_function('!document.documentElement.classList.contains("workshop-reading")')
            await page.evaluate("Reveal.slide([...document.querySelectorAll('.reveal .slides > section')].findIndex(s => s.querySelector('h2')?.textContent === 'Live: three searches'))")
            assert 'Read the whole biography' in await page.locator('.reveal section.present').inner_text()
            await assert_fits(page, 'desktop after resizing')
            assert not errors, errors
            await browser.close()
            print(f'{checks} page/viewport checks passed; exercises, resize and browser errors checked.')
    finally:
        server.shutdown()


if __name__ == '__main__':
    asyncio.run(main())
