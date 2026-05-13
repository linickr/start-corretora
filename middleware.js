export const config = {
  matcher: ['/((?!_vercel|api|assets).*)'],
}

const CSS_INJECT = [
  '<link rel="icon" type="image/png" href="/assets/images/favicon.png">',
  '<link rel="stylesheet" href="/assets/css/noturno.css">',
].join('\n  ')

const WA_ICON = `<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.124.556 4.118 1.526 5.843L.063 22.853c-.086.224-.027.476.148.64.124.115.284.175.444.175.071 0 .143-.012.213-.037l5.2-1.705A11.934 11.934 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.818c-1.992 0-3.837-.6-5.373-1.627l-.367-.229-3.799 1.247 1.225-3.669-.243-.393C2.427 15.598 1.818 13.864 1.818 12 1.818 6.367 6.367 1.818 12 1.818S22.182 6.367 22.182 12 17.633 21.818 12 21.818z"/></svg>`

function formHtml(id, okId) {
  return `
<div id="${id}-wrap" style="border-top:1px solid #1e1e1e;padding:40px 0 48px">
  <div style="max-width:520px;margin:0 auto">
    <div style="text-align:center;margin-bottom:24px">
      <div class="eyebrow">Cotação Grátis</div>
      <h2 style="font-size:clamp(1.25rem,3vw,1.65rem);font-weight:700;color:#fff;margin:8px 0 8px">
        Ficou com alguma dúvida?<br><em style="color:#00e676;font-style:normal">Receba sua cotação agora.</em>
      </h2>
      <p style="color:#777;font-size:.88rem">Resposta em até 2h. Sem compromisso.</p>
    </div>
    <form id="${id}" novalidate>
      <div class="form-row" style="margin-bottom:12px">
        <div class="form-field">
          <label class="form-label">Nome *</label>
          <input class="form-input" type="text" name="nome" placeholder="Seu nome" required>
        </div>
        <div class="form-field">
          <label class="form-label">WhatsApp *</label>
          <input class="form-input" type="tel" name="telefone" placeholder="(21) 99999-9999" required>
        </div>
      </div>
      <div class="form-field" style="margin-bottom:20px">
        <label class="form-label">Tipo de Seguro</label>
        <select class="form-select" name="seguro">
          <option value="">Selecione...</option>
          <option>Seguro de Vida</option>
          <option>Seguro Auto</option>
          <option>Plano de Saúde</option>
          <option>Seguro Residencial</option>
          <option>Seguro Empresarial</option>
        </select>
      </div>
      <button type="submit" class="btn btn-green btn-lg" style="width:100%;justify-content:center;gap:8px">
        ${WA_ICON} Quero minha cotação
      </button>
      <p class="form-note" style="text-align:center;margin-top:10px">Seus dados são confidenciais e não serão compartilhados.</p>
    </form>
    <div id="${okId}" style="display:none;text-align:center;padding:32px 0">
      <div style="font-size:2rem;margin-bottom:8px">✅</div>
      <h3 style="color:#00e676;margin-bottom:6px">Solicitação enviada!</h3>
      <p style="color:#888;font-size:.9rem">Nossa equipe entra em contato pelo WhatsApp em breve.</p>
    </div>
  </div>
</div>`
}

const FORM_DESKTOP = `
<style>
  #bcf-desktop-wrap { display: block; }
  #bcf-mobile-wrap  { display: none;  }
  @media (max-width: 1024px) {
    #bcf-desktop-wrap { display: none;  }
    #bcf-mobile-wrap  { display: block; }
  }
</style>
<section>
  <div class="container">
    ${formHtml('bcf-desktop', 'bcf-desktop-ok')}
  </div>
</section>`

const FORM_MOBILE = formHtml('bcf-mobile', 'bcf-mobile-ok')

const FORM_SCRIPT = `
<script>
(function() {
  var pairs = [['bcf-desktop','bcf-desktop-ok'],['bcf-mobile','bcf-mobile-ok']];
  pairs.forEach(function(p) {
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

  if (isBlogPost && !html.includes('bcf-desktop')) {
    // Desktop: before cta-sec or footer
    if (html.includes('<section class="cta-sec">')) {
      html = html.replace('<section class="cta-sec">', FORM_DESKTOP + '\n<section class="cta-sec">')
    } else if (html.includes('<footer')) {
      html = html.replace('<footer', FORM_DESKTOP + '\n<footer')
    }

    // Mobile: after </article>, before <aside>
    if (html.includes('</article>')) {
      html = html.replace('</article>', '</article>\n' + FORM_MOBILE)
    }

    // Script: before </body>
    html = html.replace('</body>', FORM_SCRIPT + '\n</body>')
  }

  const headers = new Headers(response.headers)
  headers.set('content-type', 'text/html; charset=utf-8')
  return new Response(html, { status: response.status, headers })
}
