/**
 * Build docs/study/transformers-study.html from its Markdown sources.
 *
 *   node scripts/build-study.mjs        (or: npm run study)
 *
 * The Markdown files are the single source of truth - edit them, never the
 * generated HTML:
 *   docs/study/cheatsheet.md   -> Cheat sheet tab (rendered in the page)
 *   docs/study/flashcards.md   -> Flashcards tab   (## group, <details> card)
 *   docs/study/quiz.md         -> Quiz tab         (### Qn · MC|compute + answer key)
 *   composables/useDeckNumbers.ts -> Playground tab (the same numbers as the decks)
 *
 * Fails loudly if a card, question or answer cannot be parsed, so a format
 * slip in the Markdown never silently drops content from the page.
 */
import { readFileSync, writeFileSync } from 'node:fs'

const read = p => readFileSync(p, 'utf8')
const fail = msg => { console.error(`build-study: ${msg}`); process.exit(1) }

// ---- flashcards -----------------------------------------------------------
function parseFlashcards(md) {
  const cards = []
  const groups = md.split(/^## /m).slice(1)
  for (const g of groups) {
    const group = g.slice(0, g.indexOf('\n')).trim()
    const re = /<details><summary><b>(Core|Deeper)<\/b> · ([\s\S]*?)<\/summary>([\s\S]*?)<\/details>/g
    let m, n = 0
    while ((m = re.exec(g))) {
      cards.push({ group, level: m[1], q: m[2].trim(), a: m[3].trim() })
      n++
    }
    const opened = (g.match(/<details>/g) || []).length
    if (opened !== n) fail(`flashcards group "${group}": ${opened} <details> but ${n} parsed`)
  }
  if (!cards.length) fail('no flashcards parsed')
  return cards
}

// ---- quiz -----------------------------------------------------------------
function parseQuiz(md) {
  const [body, key] = md.split(/^## Answer key/m)
  if (!key) fail('quiz: no "## Answer key" section')
  const answers = {}
  for (const m of key.matchAll(/^\*\*Q(\d+) — ([^*]+?)\*\*\s*([\s\S]*?)(?=^\*\*Q\d+ — |$(?![\s\S]))/gm)) {
    answers[m[1]] = { head: m[2].trim(), text: m[3].trim() }
  }
  const qs = []
  for (const block of body.split(/^### /m).slice(1)) {
    const head = block.slice(0, block.indexOf('\n'))
    const hm = head.match(/^Q(\d+) · (MC|compute)/)
    if (!hm) fail(`quiz: bad heading "${head}"`)
    const [, id, kind] = hm
    const rest = block.slice(block.indexOf('\n') + 1).replace(/\n---\s*$/, '').trim()
    const options = [...rest.matchAll(/^- ([A-D])\) (.*)$/gm)].map(o => ({ key: o[1], text: o[2].trim() }))
    const prompt = rest.replace(/^- [A-D]\) .*$/gm, '').trim()
    const ans = answers[id]
    if (!ans) fail(`quiz: no answer for Q${id}`)
    if (kind === 'MC') {
      const letter = ans.head.replace(/\.$/, '')
      if (options.length < 2) fail(`quiz Q${id}: MC with ${options.length} options`)
      if (!options.some(o => o.key === letter)) fail(`quiz Q${id}: answer "${letter}" is not an option`)
      qs.push({ id: +id, kind, prompt, options, correct: letter, explain: ans.text })
    } else {
      qs.push({ id: +id, kind, prompt, answer: ans.head.replace(/\.$/, ''), explain: ans.text })
    }
  }
  if (Object.keys(answers).length !== qs.length) fail(`quiz: ${qs.length} questions but ${Object.keys(answers).length} answers`)
  return qs
}

// ---- deck numbers ---------------------------------------------------------
function parseNumbers(ts) {
  const m = ts.match(/export const N = (\{[\s\S]*\}) as const/)
  if (!m) fail('could not find `export const N = {...} as const` in useDeckNumbers.ts')
  return JSON.parse(m[1])
}

const N = parseNumbers(read('composables/useDeckNumbers.ts'))
const data = {
  cheatsheet: read('docs/study/cheatsheet.md'),
  cards: parseFlashcards(read('docs/study/flashcards.md')),
  quiz: parseQuiz(read('docs/study/quiz.md')),
  numbers: {
    worked: N.worked,
    decode: N.decode,
    bpe: N.bpe,
  },
  built: new Date().toISOString().slice(0, 10),
}

const template = read('docs/study/_template.html')
const marker = '/*__STUDY_DATA__*/null'
if (!template.includes(marker)) fail(`template is missing ${marker}`)
// JSON is valid JS; escape "</" so no string can close the <script> element.
const json = JSON.stringify(data).replace(/<\//g, '<\\/')
writeFileSync('docs/study/transformers-study.html', template.replace(marker, json))
console.log(`wrote docs/study/transformers-study.html  (${data.cards.length} cards, ${data.quiz.length} questions)`)
