/**
 * Click-contract audit.
 *
 * Slidev auto-counts bare `v-click` directives, but NOT numbered ones beyond
 * the count it infers, and not anything inside a child component. A slide
 * whose declared `clicks:` is lower than its highest `v-click="n"` silently
 * swallows the reveals past that point - no error, no warning, and you only
 * notice mid-lecture.
 *
 * This checks every slide statically:  declared clicks >= highest index used.
 *
 *   node scripts/check-clicks.mjs
 */
import { readFileSync, readdirSync } from 'node:fs'
import { join } from 'node:path'

const DIR = 'pages'
const problems = []
let slideNo = 0, checked = 0

for (const file of readdirSync(DIR).filter(f => f.endsWith('.md')).sort()) {
  const text = readFileSync(join(DIR, file), 'utf8')
  // Split into slides on frontmatter fences; the first slide starts at the top.
  const parts = text.split(/^---$/m)
  // parts alternates: '', frontmatter, body, frontmatter, body, ...
  for (let i = 1; i < parts.length; i += 2) {
    const fm = parts[i] ?? ''
    const body = parts[i + 1] ?? ''
    slideNo++
    checked++

    const declared = /(?:^|\n)clicks:\s*(\d+)/.exec(fm)
    const declaredN = declared ? Number(declared[1]) : null

    const indices = [...body.matchAll(/v-click="(\d+)"/g)].map(m => Number(m[1]))
    const ranges = [...body.matchAll(/v-click="\[(\d+),\s*(\d+)\]"/g)].flatMap(m => [Number(m[1]), Number(m[2])])
    const maxUsed = Math.max(0, ...indices, ...ranges)
    const bare = (body.match(/v-click(?![="])/g) || []).length

    const title = (/^#\s+(.+)$/m.exec(body)?.[1] ?? '(no heading)').replace(/<[^>]+>/g, '').slice(0, 44)

    if (maxUsed > 0 && declaredN === null)
      problems.push(`slide ${String(slideNo).padStart(3)}  ${file}  uses v-click="${maxUsed}" but declares no clicks:   ${title}`)
    else if (maxUsed > 0 && declaredN < maxUsed)
      problems.push(`slide ${String(slideNo).padStart(3)}  ${file}  clicks: ${declaredN} < highest v-click="${maxUsed}"   ${title}`)
    else if (declaredN !== null && maxUsed > 0 && declaredN > maxUsed && bare === 0)
      problems.push(`slide ${String(slideNo).padStart(3)}  ${file}  clicks: ${declaredN} but nothing uses index > ${maxUsed} (dead clicks)   ${title}`)
  }
}

// --- component lint -------------------------------------------------------
// Slidev runs UnoCSS with the attributify preset, which reads bare HTML
// attributes as utility classes. `opacity="1"` is parsed as `opacity-1`, and
// on the Tailwind scale that is ONE PER CENT - so a fully opaque element
// renders invisible, and only when the value is exactly 1. It cost an
// afternoon once; it is a one-line check now.
const lint = []
for (const file of readdirSync('components').filter(f => f.endsWith('.vue'))) {
  const text = readFileSync(join('components', file), 'utf8')
  for (const [i, line] of text.split('\n').entries()) {
    if (/:opacity\s*=/.test(line))
      lint.push(`components/${file}:${i + 1}  bind opacity through :style, not the attribute (UnoCSS attributify reads opacity="1" as 1%)`)
  }
}

const all = [...problems, ...lint]
console.log(all.length ? all.join('\n') : 'clicks and component lint both clean')
console.log(`\n${checked} slides checked, ${all.length} problem(s)`)
process.exit(all.length ? 1 : 0)
