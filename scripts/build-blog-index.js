// Gera automaticamente os cards do blog/index.html a partir dos arquivos HTML em blog/
const fs   = require('fs')
const path = require('path')

const BASE    = path.join(__dirname, '..')
const BLOG    = path.join(BASE, 'blog')
const INDEX   = path.join(BLOG, 'index.html')
const SITEMAP = path.join(BASE, 'sitemap.xml')

const MONTHS = ['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez']

const CATS = [
  { re: /label-residencial|seguro[- ]residencial/i, cat: 'seguro-residencial', label: 'Seguro Residencial', css: 'label-residencial', emoji: '🏠' },
  { re: /label-auto|seguro[- ]auto/i,               cat: 'seguro-auto',        label: 'Seguro Auto',        css: 'label-auto',        emoji: '🚗' },
  { re: /label-saude|plano[- ]de[- ]saude/i,        cat: 'plano-de-saude',     label: 'Plano de Saúde',    css: 'label-saude',        emoji: '🩺' },
  { re: /label-empresarial|seguro[- ]empresarial/i, cat: 'seguro-empresarial', label: 'Seguro Empresarial', css: 'label-empresarial',  emoji: '🏢' },
  { re: /label-vida|seguro[- ]de[- ]vida/i,         cat: 'seguro-de-vida',     label: 'Seguro de Vida',    css: 'label-vida',         emoji: '❤️' },
]

const getTitle = html => {
  const m = html.match(/<title[^>]*>([^<]+)<\/title>/i)
  return m ? m[1].replace(/\s*\|[^|]*$/, '').trim() : ''
}

const getDesc = html => {
  const m = html.match(/<meta[^>]+name=["']description["'][^>]+content=["']([^"']+)["']/i)
           || html.match(/<meta[^>]+content=["']([^"']+)["'][^>]+name=["']description["']/i)
  return m ? m[1].trim() : ''
}

const getCat = (html, slug) => {
  // Pega o texto do primeiro span.label do artigo — é a categoria declarada no post
  const m = html.match(/<span[^>]+class="label[^"]*"[^>]*>([^<]+)<\/span>/i)
  if (m) {
    const text = m[1].trim()
    const byText = CATS.find(c => c.label === text)
    if (byText) return byText
  }
  // Fallback: slug
  return CATS.find(c => c.re.test(slug)) ?? CATS[CATS.length - 1]
}

const getDate = (slug, sitemap) => {
  const esc = slug.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  const m = sitemap.match(new RegExp(`<loc>[^<]*${esc}[^<]*<\\/loc>[^]*?<lastmod>([^<]+)<\\/lastmod>`, 'i'))
  return m ? m[1].trim() : null
}

const fmtDate = iso => {
  if (!iso) return ''
  const [y, mo, d] = iso.split('-').map(Number)
  return `${String(d).padStart(2,'0')} ${MONTHS[mo - 1]} ${y}`
}

function buildCard({ slug, title, desc, cat, dateStr }) {
  const href = `/blog/${slug}`
  const locs = []
  if (/rio|tijuca|copacabana|ipanema|barra|niteroi|flamengo|botafogo|leblon|lapa/i.test(title + slug)) locs.push('rio-de-janeiro')
  if (/sao[- ]paulo|\bsp\b|paulista/i.test(title + slug)) locs.push('sao-paulo')
  const dataCat = [cat.cat, ...locs].join(' ')

  return `    <article class="blog-card" data-cat="${dataCat}">
      <a href="${href}">
        <div class="blog-card-thumb">${cat.emoji}</div>
      </a>
      <div class="blog-card-body">
        <span class="label ${cat.css}">${cat.label}</span>
        <h3><a href="${href}">${title}</a></h3>
        <p>${desc}</p>
        <div class="blog-card-footer">
          <span class="blog-card-date">${dateStr}</span>
          <a href="${href}" class="blog-card-read">Ler →</a>
        </div>
      </div>
    </article>`
}

function main() {
  const sitemap = fs.existsSync(SITEMAP) ? fs.readFileSync(SITEMAP, 'utf8') : ''

  const posts = fs.readdirSync(BLOG)
    .filter(f => f.endsWith('.html') && f !== 'index.html')
    .map(f => {
      const slug    = f.replace('.html', '')
      const html    = fs.readFileSync(path.join(BLOG, f), 'utf8')
      const isoDate = getDate(slug, sitemap)
      return { slug, title: getTitle(html), desc: getDesc(html), cat: getCat(html, slug), dateStr: fmtDate(isoDate), ts: isoDate ? new Date(isoDate).getTime() : 0 }
    })
    .sort((a, b) => b.ts - a.ts)

  const cards = posts.map(buildCard).join('\n\n')

  const START = '  <!-- Grid -->\n  <div class="blog-grid">'
  const END   = '\n\n<!-- ==================== CTA'

  let index = fs.readFileSync(INDEX, 'utf8').replace(/\r\n/g, '\n')
  const si  = index.indexOf(START)
  const ei  = index.indexOf(END, si)

  if (si === -1 || ei === -1) {
    console.error('❌ Âncoras do grid não encontradas em blog/index.html')
    process.exit(1)
  }

  index = index.slice(0, si + START.length) + '\n' + cards + '\n\n  </div>\n</div>' + index.slice(ei)
  fs.writeFileSync(INDEX, index, 'utf8')

  console.log(`✅ blog/index.html — ${posts.length} artigos`)
  posts.forEach(p => console.log(`   ${p.dateStr || '          '}  /blog/${p.slug}`))
}

main()
