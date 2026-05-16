export const config = {
  matcher: ['/((?!_vercel|api|assets).*)'],
}

const FONTS = [
  '<link rel="preconnect" href="https://fonts.googleapis.com">',
  '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
  '<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Barlow+Condensed:wght@700;800;900&family=Barlow:wght@300;400;500;600&display=swap" rel="stylesheet">',
].join('\n  ')

const GA = `<script async src="https://www.googletagmanager.com/gtag/js?id=G-TLZ8DCN563"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-TLZ8DCN563');</script>`

const CSS_INJECT = [
  '<link rel="icon" type="image/png" href="/assets/images/favicon.png">',
  '<link rel="stylesheet" href="/assets/css/noturno.css">',
].join('\n  ')

function quoteBlock(formId, successId) {
  return `<div class="quote-block">
  <div class="quote-block-head">
    <div class="eyebrow">Cotação grátis</div>
    <h2>Ficou com alguma dúvida?</h2>
    <p class="quote-sub">Resposta em até 2h. Sem compromisso.</p>
  </div>
  <form class="quote-form" id="${formId}" novalidate>
    <div class="form-field"><label class="form-label">Nome</label><input class="form-input" type="text" name="nome" placeholder="Seu nome" required></div>
    <div class="form-field"><label class="form-label">WhatsApp</label><input class="form-input" type="tel" name="telefone" placeholder="(21) 99999-9999" required></div>
    <div class="form-field"><label class="form-label">Tipo</label><select class="form-select" name="seguro"><option value="">Selecione...</option><option>Seguro de Vida</option><option>Seguro Auto</option><option>Plano de Saúde</option><option>Seguro Residencial</option><option>Seguro Empresarial</option></select></div>
    <button type="submit" class="btn btn-green" style="height:44px;align-self:end">Cotar →</button>
  </form>
  <div class="quote-success" id="${successId}" style="display:none">✓ <strong>Solicitação recebida!</strong> Nossa equipe entrará em contato em breve.</div>
  <div class="quote-wa">Prefere falar agora? <a href="https://wa.me/5521999992002?text=Ol%C3%A1!%20Vim%20pelo%20blog%20e%20gostaria%20de%20uma%20cota%C3%A7%C3%A3o." target="_blank" rel="noopener">Falar direto no WhatsApp →</a></div>
</div>`
}

const FORM_DESKTOP = `
<style>
  #bcf-desk { display: block; }
  #bcf-mob  { display: none;  }
  @media (max-width: 1024px) {
    #bcf-desk { display: none;  }
    #bcf-mob  { display: block; }
  }
</style>
<section id="bcf-desk" style="padding:56px 0">
  <div class="container">
    ${quoteBlock('bcf-desk-form', 'bcf-desk-ok')}
  </div>
</section>`

const FORM_MOBILE = `<div id="bcf-mob" style="margin-top:32px">
  ${quoteBlock('bcf-mob-form', 'bcf-mob-ok')}
</div>`

const FORM_SCRIPT = `<script>
(function() {
  [['bcf-desk-form','bcf-desk-ok'],['bcf-mob-form','bcf-mob-ok']].forEach(function(p) {
    var form = document.getElementById(p[0]);
    if (!form) return;
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      var nome = this.nome.value.trim();
      var tel  = this.telefone.value.trim();
      var seg  = this.seguro.value || 'seguro';
      if (!nome || !tel) { alert('Preencha nome e WhatsApp para continuar.'); return; }
      var msg = encodeURIComponent('Olá! Me chamo ' + nome + ' e vim pelo blog. Gostaria de uma cotação de ' + seg + '.');
      window.open('https://wa.me/5521999992002?text=' + msg, '_blank');
      this.style.display = 'none';
      document.getElementById(p[1]).style.display = 'block';
    });
  });
})();
</script>`

function buildFragmentPage(fragment, pathname) {
  const h1Match = fragment.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i)
  const rawTitle = h1Match ? h1Match[1].replace(/<[^>]+>/g, '').trim() : ''
  const pageTitle = rawTitle ? `${rawTitle} | Start Corretora` : 'Start Corretora de Seguros'

  const pMatch = fragment.match(/<p[^>]*>([\s\S]*?)<\/p>/i)
  const rawDesc = pMatch
    ? pMatch[1].replace(/<[^>]+>/g, '').trim().slice(0, 160)
    : 'Start Corretora de Seguros — cotação online, atendimento humanizado.'

  const canonical = `https://startcorretoradeseguros.com.br${pathname.replace(/\.html$/, '')}`

  // Detect article-format fragments (blog/SEO posts with post-body structure)
  const isArticle = fragment.includes('class="post-body"') || fragment.includes('class="post-meta"')

  let bodyContent
  if (isArticle) {
    // Build a friendly location badge from the URL slug
    const slug = pathname.replace(/^\/+|\.html$/g, '').split('/').pop()
    const location = slug
      .replace(/^corretora-de-seguros[-–]?(em[-–]?|no[-–]?|na[-–]?|nos[-–]?|nas[-–]?)?/i, '')
      .replace(/-/g, ' ')
      .trim()
      .replace(/\b\w/g, l => l.toUpperCase()) || 'Rio de Janeiro'

    // Strip label, h1 and post-meta from fragment — they go into the hero
    const articleContent = fragment
      .replace(/<span[^>]*class="label[^"]*"[^>]*>[\s\S]*?<\/span>\s*/i, '')
      .replace(/<h1[^>]*>[\s\S]*?<\/h1>\s*/i, '')
      .replace(/<div[^>]*class="post-meta"[^>]*>[\s\S]*?<\/div>\s*/i, '')

    bodyContent = `<div class="fragment-hero">
  <div class="container">
    <div class="hero-badge">📍 ${location}</div>
    <h1 class="fragment-hero-title">${rawTitle}</h1>
    <div class="hero-actions">
      <a href="https://wa.me/5521999992002?text=Ol%C3%A1!%20Vim%20pelo%20site%20e%20gostaria%20de%20uma%20cota%C3%A7%C3%A3o." class="btn-primary" target="_blank" rel="noopener">Cotar pelo WhatsApp →</a>
      <a href="tel:+5521999992002" class="btn-outline">📞 (21) 99999-2002</a>
    </div>
  </div>
</div>
<section style="padding:64px 0 80px">
  <div class="container" style="max-width:820px">
${articleContent}
  </div>
</section>`
  } else {
    bodyContent = `<section style="padding-top:calc(var(--nav-h) + var(--ticker-h) + 56px);padding-bottom:80px">
  <div class="container" style="max-width:820px">
${fragment}
  </div>
</section>`
  }

  return `<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <link rel="icon" type="image/png" href="/assets/images/favicon.png">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${pageTitle}</title>
  <meta name="description" content="${rawDesc.replace(/"/g, '&quot;')}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="${canonical}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="${canonical}">
  <meta property="og:title" content="${pageTitle.replace(/"/g, '&quot;')}">
  <meta property="og:description" content="${rawDesc.replace(/"/g, '&quot;')}">
  <meta property="og:image" content="https://startcorretoradeseguros.com.br/assets/images/logo-start-corretora.png">
  ${FONTS}
  <link rel="stylesheet" href="/assets/css/noturno.css">
  ${GA}
</head>
<body>
${bodyContent}
${FORM_DESKTOP}
<script src="/assets/js/layout.js"></script>
<script src="/assets/js/main.js"></script>
${FORM_SCRIPT}
</body>
</html>`
}

export default async function middleware(request) {
  const { pathname } = new URL(request.url)
  const isBlogPost = /^\/blog\/[^/]+/.test(pathname)

  const response = await fetch(request)
  const contentType = response.headers.get('content-type') ?? ''

  if (!contentType.includes('text/html')) return response

  let html = await response.text()

  const trimmed = html.trimStart()
  const isFragment = !trimmed.startsWith('<!') && !trimmed.startsWith('<html') && !trimmed.startsWith('<HTML')

  if (isFragment) {
    html = buildFragmentPage(html, pathname)
  } else {
    if (!html.includes('noturno.css')) {
      html = html.includes('</head>')
        ? html.replace('</head>', `  ${CSS_INJECT}\n</head>`)
        : `<head>\n  ${CSS_INJECT}\n</head>\n` + html
    }

    if (!html.includes('G-TLZ8DCN563') && html.includes('</head>')) {
      html = html.replace('</head>', `  ${GA}\n</head>`)
    }

    if (!html.includes('layout.js') && html.includes('</body>')) {
      html = html.replace('</body>', '<script src="/assets/js/layout.js"></script>\n<script src="/assets/js/main.js"></script>\n</body>')
    }

    if (isBlogPost && !html.includes('bcf-desk')) {
      if (html.includes('<section class="cta-sec">')) {
        html = html.replace('<section class="cta-sec">', FORM_DESKTOP + '\n<section class="cta-sec">')
      } else if (html.includes('<footer')) {
        html = html.replace('<footer', FORM_DESKTOP + '\n<footer')
      }

      if (html.includes('</article>')) {
        html = html.replace('</article>', '</article>\n' + FORM_MOBILE)
      }

      html = html.replace('</body>', FORM_SCRIPT + '\n</body>')
    }
  }

  const headers = new Headers(response.headers)
  headers.set('content-type', 'text/html; charset=utf-8')
  return new Response(html, { status: response.status, headers })
}
