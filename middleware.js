export const config = {
  matcher: ['/((?!_vercel|api|assets).*)'],
}

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
<section style="padding:56px 0">
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

export default async function middleware(request) {
  const { pathname } = new URL(request.url)
  const isBlogPost = /^\/blog\/[^/]+/.test(pathname)

  const response = await fetch(request)
  const contentType = response.headers.get('content-type') ?? ''

  if (!contentType.includes('text/html')) return response

  let html = await response.text()

  if (!html.includes('noturno.css')) {
    html = html.includes('</head>')
      ? html.replace('</head>', `  ${CSS_INJECT}\n</head>`)
      : `<head>\n  ${CSS_INJECT}\n</head>\n` + html
  }

  if (isBlogPost && !html.includes('bcf-desk')) {
    // Desktop: antes do cta-sec ou footer
    if (html.includes('<section class="cta-sec">')) {
      html = html.replace('<section class="cta-sec">', FORM_DESKTOP + '\n<section class="cta-sec">')
    } else if (html.includes('<footer')) {
      html = html.replace('<footer', FORM_DESKTOP + '\n<footer')
    }

    // Mobile: após </article>, antes do aside
    if (html.includes('</article>')) {
      html = html.replace('</article>', '</article>\n' + FORM_MOBILE)
    }

    html = html.replace('</body>', FORM_SCRIPT + '\n</body>')
  }

  const headers = new Headers(response.headers)
  headers.set('content-type', 'text/html; charset=utf-8')
  return new Response(html, { status: response.status, headers })
}
