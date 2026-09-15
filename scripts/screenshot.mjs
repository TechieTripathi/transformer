/**
 * Screenshot slides from a running dev server.
 *
 * This exists for the LECTURE-HALL LEGIBILITY PASS, which is the real
 * acceptance test for this deck: the back row of a 500-seat hall is 25-30 m
 * from the screen, and a projector in a lit room gives maybe 15:1 contrast
 * against a laptop's 1000:1. A slide that reads beautifully while you build
 * it can be unreadable where two thirds of the audience is sitting.
 *
 * So: capture every slide, then view the PNGs at 25%. Anything you cannot
 * read at that size fails, regardless of how it looks in the browser.
 *
 * It also fails loudly on console and page errors, which is the only way to
 * catch a component that builds fine and then throws at runtime.
 *
 *   npm run dev -- --port 3033
 *   node scripts/screenshot.mjs http://localhost:3033 out/ 1 2:4 7:3
 *
 * A bare number is a slide; `7:3` is slide 7 at click 3. With no slide
 * arguments it walks the whole deck.
 */
import { chromium } from 'playwright-chromium'
import { mkdir } from 'node:fs/promises'

const [, , base = 'http://localhost:3030', outDir = 'shots', ...specs] = process.argv
await mkdir(outDir, { recursive: true })

const browser = await chromium.launch()
const page = await browser.newPage({
  viewport: { width: 1280, height: 720 },
  deviceScaleFactor: 2,
})

// Hide the dev-server chrome: the nav controls sit on top of the slide, and
// in headless Chromium their icon font does not load, so every button renders
// as its own tooltip text across the top of the capture.
await page.addStyleTag({ content: `
  .slidev-nav-controls, #slide-controls, .slidev-icon-btn,
  [class*="nav-controls"], .v-popper__popper,
  .slidev-page-no, [class*="page-no"] { display: none !important; }
` }).catch(() => {})

const errors = []
page.on('pageerror', e => errors.push(`PAGEERROR  ${e.message}`))
page.on('console', m => { if (m.type() === 'error') errors.push(`CONSOLE    ${m.text()}`) })

let targets = specs
if (!targets.length) {
  await page.goto(`${base}/1`, { waitUntil: 'networkidle' })
  const total = await page.evaluate(() =>
    document.querySelectorAll('#slide-container, .slidev-page').length || 0)
  targets = Array.from({ length: total || 120 }, (_, i) => String(i + 1))
}

for (const spec of targets) {
  const [n, clicks] = String(spec).split(':')
  const url = `${base}/${n}${clicks ? `?clicks=${clicks}` : ''}`
  const res = await page.goto(url, { waitUntil: 'networkidle' })
  if (!res || res.status() >= 400) { errors.push(`HTTP ${res?.status()} on ${url}`); continue }
  await page.addStyleTag({ content: `
    .slidev-nav-controls, #slide-controls, .slidev-icon-btn,
    [class*="nav-controls"], .v-popper__popper,
    .slidev-page-no, [class*="page-no"] { display: none !important; }
  ` }).catch(() => {})
  await page.waitForTimeout(1400)
  const name = `slide-${String(n).padStart(3, '0')}${clicks ? `-c${clicks}` : ''}.png`
  await page.screenshot({ path: `${outDir}/${name}` })
  process.stdout.write(`${name}\n`)
}

await browser.close()

if (errors.length) {
  console.log('\n--- ERRORS ---')
  console.log([...new Set(errors)].join('\n'))
  process.exit(1)
}
console.log('\nno console or page errors')
