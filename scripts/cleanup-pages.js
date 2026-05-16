/**
 * cleanup-pages.js
 * Remove nav, footer, inline style e GA hardcoded de todas as páginas.
 * Depois de rodar, o middleware injeta layout.js e GA automaticamente.
 */
const fs = require('fs')
const path = require('path')

const ROOT = path.resolve(__dirname, '..')

const SKIP_DIRS  = new Set(['node_modules', 'admin', 'scripts', '.git'])
const SKIP_ROOTS = new Set([path.join(ROOT, 'index.html')])

function collect(dir, results = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name)
    if (entry.isDirectory()) {
      if (!SKIP_DIRS.has(entry.name)) collect(full, results)
    } else if (entry.name.endsWith('.html') && !SKIP_ROOTS.has(full)) {
      results.push(full)
    }
  }
  return results
}

function clean(html) {
  // Skip redirect stubs
  if (html.includes('http-equiv="refresh"')) return null
  // Skip already clean pages
  if (html.includes('layout.js') && !html.includes('<style') && !html.includes('<header')) return null

  const original = html
  const hadStyle = /<style[^>]*>/i.test(html)

  // 1. Remove <style>...</style> blocks
  html = html.replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')

  // 2. Remove GA inline scripts (com ou sem comentário)
  html = html.replace(/\s*<!--\s*Google tag[\s\S]*?-->\s*<script[^>]*src="https:\/\/www\.googletagmanager[^"]*"[^>]*><\/script>\s*<script>[\s\S]*?<\/script>/gi, '')
  html = html.replace(/<script[^>]*src="https:\/\/www\.googletagmanager\.com[^"]*"[^>]*><\/script>\s*<script>[\s\S]*?gtag\(['"]config['"][\s\S]*?<\/script>/gi, '')

  // 3. Remove <header>...</header>
  html = html.replace(/<header[\s\S]*?<\/header>/gi, '')

  // 4. Remove <footer>...</footer>
  html = html.replace(/<footer[\s\S]*?<\/footer>/gi, '')

  // 5. Remove <section class="cta-sec">...</section> (CTA hardcoded)
  html = html.replace(/<section\s[^>]*class="cta-sec"[\s\S]*?<\/section>/gi, '')

  // 6. Remove site nav: <nav ... id="mainNav">...</nav>
  html = html.replace(/<nav[^>]*id="mainNav"[\s\S]*?<\/nav>/gi, '')

  // 7. Remove mobile menu/nav div
  html = html.replace(/<div[^>]*class="mobile-(?:menu|nav)"[\s\S]*?<\/div>/gi, '')

  // 8. Remove ticker div (hardcoded)
  html = html.replace(/<div[^>]*class="ticker"[^>]*>[\s\S]*?<!-- end ticker -->/gi, '')

  // 9. Remove wa-float link
  html = html.replace(/<a[^>]*class="wa-float"[\s\S]*?<\/a>/gi, '')

  // 10. Remove inline nav JS (burger, scroll, mobileMenu)
  html = html.replace(/<script>[\s\S]*?getElementById\('mainNav'\)[\s\S]*?<\/script>/gi, '')
  html = html.replace(/<script>[\s\S]*?getElementById\("mainNav"\)[\s\S]*?<\/script>/gi, '')

  // 11. Fix relative asset paths → absolute
  html = html.replace(/\b(href|src)="assets\//g, '$1="/assets/')

  // 12. Ensure noturno.css
  if (!html.includes('noturno.css')) {
    html = html.replace('</head>', '  <link rel="stylesheet" href="/assets/css/noturno.css">\n</head>')
  }

  // 13. Ensure Google Fonts
  if (!html.includes('fonts.googleapis.com/css2')) {
    const fonts = [
      '  <link rel="preconnect" href="https://fonts.googleapis.com">',
      '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
      '  <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Barlow+Condensed:wght@700;800;900&family=Barlow:wght@300;400;500;600&display=swap" rel="stylesheet">',
    ].join('\n')
    html = html.replace('</head>', fonts + '\n</head>')
  }

  // 14. Add padding-top to <main> in old-theme pages (compensate fixed nav)
  if (hadStyle && html.includes('<main') && !html.includes('padding-top')) {
    html = html.replace(/<main([^>]*)>/i, (_, attrs) => {
      if (attrs.includes('style=')) return `<main${attrs.replace(/style="/, 'style="padding-top:calc(var(--nav-h,80px) + 40px);')}>`
      return `<main${attrs} style="padding-top:calc(var(--nav-h,80px) + 40px)">`
    })
  }

  // 15. Clean up excess blank lines
  html = html.replace(/\n{3,}/g, '\n\n')

  return html !== original ? html : null
}

const files = collect(ROOT)
let changed = 0, skipped = 0, errors = 0

for (const file of files) {
  try {
    const src = fs.readFileSync(file, 'utf8')
    const result = clean(src)
    if (result === null) {
      skipped++
    } else {
      fs.writeFileSync(file, result, 'utf8')
      console.log('✓', path.relative(ROOT, file))
      changed++
    }
  } catch (err) {
    console.error('✗', path.relative(ROOT, file), err.message)
    errors++
  }
}

console.log(`\nDone: ${changed} cleaned, ${skipped} skipped, ${errors} errors`)
