/**
 * Overflow check for the lecture-hall legibility pass.
 *
 * Slidev keeps neighbouring slides mounted at height 0 and renders the active
 * one into a `.slidev-layout` that fills the 720px container, with the chapter
 * footer occupying the bottom ~39px. Content that reaches the footer collides
 * with it - invisible while authoring, obvious from the back of a hall.
 *
 * Reports every slide whose content, at its LAST click state, reaches the
 * footer (or the canvas bottom on layouts that hide the footer).
 *
 *   node check-overflow.mjs http://localhost:3030 73
 */
import { chromium } from 'playwright-chromium'

const base = process.argv[2] ?? 'http://localhost:3030'
const total = Number(process.argv[3] ?? 73)

const browser = await chromium.launch()
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } })
const bad = []

for (let n = 1; n <= total; n++) {
  await page.goto(`${base}/${n}?clicks=99`, { waitUntil: 'networkidle' })
  await page.waitForTimeout(300)

  const r = await page.evaluate(() => {
    const container = document.querySelector('.slidev-slide-container')
    if (!container) return null

    // The active slide is the only .slidev-layout with a real height.
    const layout = [...container.querySelectorAll('.slidev-layout')]
      .find(el => el.getBoundingClientRect().height > 1)
    if (!layout) return null

    const footer = container.querySelector('.ann-footer')
    const limit = footer
      ? footer.getBoundingClientRect().top
      : container.getBoundingClientRect().bottom

    let maxB = 0, worst = ''
    for (const c of layout.querySelectorAll('*')) {
      const cb = c.getBoundingClientRect()
      if (cb.height < 2 || cb.width < 2) continue
      if (cb.bottom > maxB) {
        maxB = cb.bottom
        worst = ((c.className || '').toString().split(' ')[0] || c.tagName) +
                ' | ' + (c.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40)
      }
    }
    return { over: Math.round(maxB - limit), slack: Math.round(limit - maxB), worst }
  })

  if (r && r.over > 0) bad.push(`slide ${String(n).padStart(3)}  +${String(r.over).padStart(3)}px  ${r.worst}`)
}

await browser.close()
console.log(bad.length ? bad.join('\n') : 'no slide reaches the footer')
console.log(`\n${bad.length} of ${total} slides overflow`)
