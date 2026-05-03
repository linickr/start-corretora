/**
 * layout.js — Start Corretora
 * Injeta nav, ticker, footer e wa-float em todas as páginas.
 * Scripts compartilhados (scroll, hamburger, animações) também ficam aqui.
 *
 * Personalização do ticker por página (opcional, definir ANTES deste script):
 *   window.TICKER_CONFIG = { label: 'Artigo', items: ['texto 1', 'texto 2'] }
 */

(function () {

  /* ── Configuração do ticker ── */
  const ticker = window.TICKER_CONFIG || {
    label: 'Artigos',
    items: [
      'Seguro de vida: por que investir hoje',
      'Quem recebe o seguro após o falecimento',
      'Quantas pessoas podem ser cobertas',
      'Quanto custa um seguro de vida de R$500 mil',
      'Benefícios do seguro de vida',
      'Seguro de vida e doenças graves',
      'Seguro auto no Rio de Janeiro',
      'Plano de saúde: qual o melhor para seu perfil',
    ]
  };

  /* ── HTML ── */
  const WA_HREF = 'https://wa.me/5521999992002?text=Ol%C3%A1!%20Vim%20pelo%20site%20e%20gostaria%20de%20uma%20cota%C3%A7%C3%A3o.';
  const WA_SVG  = `<svg width="28" height="28" viewBox="0 0 24 24" fill="white"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.124.556 4.118 1.526 5.843L.063 22.853c-.086.224-.027.476.148.64.124.115.284.175.444.175.071 0 .143-.012.213-.037l5.2-1.705A11.934 11.934 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.818c-1.992 0-3.837-.6-5.373-1.627l-.367-.229-3.799 1.247 1.225-3.669-.243-.393C2.427 15.598 1.818 13.864 1.818 12 1.818 6.367 6.367 1.818 12 1.818S22.182 6.367 22.182 12 17.633 21.818 12 21.818z"/></svg>`;
  const WA_SMALL = `<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.124.556 4.118 1.526 5.843L.063 22.853c-.086.224-.027.476.148.64.124.115.284.175.444.175.071 0 .143-.012.213-.037l5.2-1.705A11.934 11.934 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.818c-1.992 0-3.837-.6-5.373-1.627l-.367-.229-3.799 1.247 1.225-3.669-.243-.393C2.427 15.598 1.818 13.864 1.818 12 1.818 6.367 6.367 1.818 12 1.818S22.182 6.367 22.182 12 17.633 21.818 12 21.818z"/></svg>`;

  const tickerItems = [...ticker.items, ...ticker.items]
    .map(t => `<span class="ticker-item">${t}</span>`).join('');

  const NAV_HTML = `
<nav class="nav" id="mainNav">
  <div class="nav-inner container" style="padding:0 28px;max-width:1200px;margin:0 auto;width:100%">
    <a href="/" class="nav-logo">
      <img src="/assets/images/logo-start-corretora.png" alt="Start Corretora de Seguros" style="height:44px;width:auto">
    </a>
    <ul class="nav-links">
      <li><a href="/seguro-de-vida.html">Seguro de Vida</a></li>
      <li><a href="/plano-de-saude.html">Plano de Saúde</a></li>
      <li><a href="/seguro-auto.html">Seguro Auto</a></li>
      <li><a href="/blog/">Blog</a></li>
      <li><a href="/sobre.html">Sobre</a></li>
      <li><a href="/contato.html">Contato</a></li>
    </ul>
    <div class="nav-end">
      <a href="/contato.html" class="btn btn-outline">Contato</a>
      <a href="${WA_HREF}" class="btn btn-green" target="_blank" rel="noopener">
        ${WA_SMALL} Cotar agora
      </a>
    </div>
    <div class="nav-burger" id="burger" aria-label="Menu">
      <span></span><span></span><span></span>
    </div>
  </div>
</nav>

<div class="mobile-nav" id="mobileNav">
  <a href="/seguro-de-vida.html">Seguro de Vida</a>
  <a href="/plano-de-saude.html">Plano de Saúde</a>
  <a href="/seguro-auto.html">Seguro Auto</a>
  <a href="/seguro-residencial.html">Seguro Residencial</a>
  <a href="/seguro-empresarial.html">Seguro Empresarial</a>
  <a href="/blog/">Blog</a>
  <a href="/sobre.html">Sobre</a>
  <a href="/contato.html">Contato</a>
  <a href="https://wa.me/5521999992002" class="btn btn-green btn-lg" target="_blank" rel="noopener" style="margin-top:32px;max-width:260px;justify-content:center">
    Cotar no WhatsApp
  </a>
</div>

<div class="ticker">
  <span class="ticker-pill">${ticker.label}</span>
  <div class="ticker-scroll">
    <div class="ticker-track">${tickerItems}</div>
  </div>
</div>`;

  const FOOTER_HTML = `
<section class="cta-sec">
  <div class="container">
    <div class="cta-body">
      <div class="eyebrow">Proteção agora</div>
      <h2 class="cta-title">
        Pronto para proteger<br>o que <em>mais importa?</em>
      </h2>
      <p class="cta-desc">
        Fale com um corretor agora mesmo. Sem robôs, sem enrolação.<br>
        Cotação em minutos, diretamente no WhatsApp.
      </p>
      <div class="cta-btns">
        <a href="${WA_HREF}" class="btn btn-green btn-lg" target="_blank" rel="noopener">
          ${WA_SMALL} Falar no WhatsApp
        </a>
        <a href="/contato.html" class="btn btn-outline btn-lg">Ou envie uma mensagem</a>
      </div>
      <div class="trust-row">
        <div class="trust-item">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#00C853" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
          Sem compromisso
        </div>
        <div class="trust-item">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#00C853" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
          Resposta em 24h
        </div>
        <div class="trust-item">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#00C853" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
          Atendimento humano
        </div>
      </div>
    </div>
  </div>
</section>

<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <img src="/assets/images/logo-start-corretora.png" alt="Start Corretora de Seguros" style="height:48px;width:auto;margin-bottom:16px">
        <p class="f-desc">
          Corretora independente especializada em seguros e planos de saúde.
          Atendemos pessoas físicas e jurídicas em todo o Brasil, com foco.
        </p>
        <div class="f-contact">
          <div class="f-contact-item">
            <svg class="f-contact-ico" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            <span>Rua Gastão Penalva, 15 — Andaraí</span>
          </div>
          <div class="f-contact-item">
            <svg class="f-contact-ico" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 13.5 19.79 19.79 0 0 1 1.61 4.9 2 2 0 0 1 3.59 2.69h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 9.49a16 16 0 0 0 6 6l.91-.91a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 21.5 17l.42-.08z"/></svg>
            <a href="https://wa.me/5521999992002" style="color:var(--primary)">(21) 99999-2002</a>
          </div>
          <div class="f-contact-item">
            <svg class="f-contact-ico" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
            <span>CNPJ: 48.385.999/0001-69</span>
          </div>
        </div>
      </div>
      <div>
        <div class="f-col-head">Seguros</div>
        <ul class="f-links">
          <li><a href="/seguro-de-vida.html">Seguro de Vida</a></li>
          <li><a href="/plano-de-saude.html">Plano de Saúde</a></li>
          <li><a href="/seguro-auto.html">Seguro Auto</a></li>
          <li><a href="/seguro-residencial.html">Seguro Residencial</a></li>
          <li><a href="/seguro-empresarial.html">Seguro Empresarial</a></li>
        </ul>
      </div>
      <div>
        <div class="f-col-head">Regiões</div>
        <ul class="f-links">
          <li><a href="/">Todo o Brasil</a></li>
        </ul>
      </div>
      <div>
        <div class="f-col-head">Empresa</div>
        <ul class="f-links">
          <li><a href="/sobre.html">Sobre a Start</a></li>
          <li><a href="/blog/">Blog</a></li>
          <li><a href="/contato.html">Contato</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p class="f-copy">© 2025 Start Corretora de Seguros LTDA. Todos os direitos reservados.</p>
      <p class="f-copy">Desenvolvido para proteger quem você ama.</p>
    </div>
  </div>
</footer>

<a href="${WA_HREF}" class="wa-float" target="_blank" rel="noopener" aria-label="WhatsApp">
  ${WA_SVG}
</a>`;

  /* ── Injeção ── */
  document.body.insertAdjacentHTML('afterbegin', NAV_HTML);
  document.body.insertAdjacentHTML('beforeend', FOOTER_HTML);

  /* ── Scripts compartilhados ── */

  // Nav scroll
  const navEl = document.getElementById('mainNav');
  window.addEventListener('scroll', () => {
    navEl.classList.toggle('scrolled', window.scrollY > 16);
  }, { passive: true });

  // Hamburger
  const burger   = document.getElementById('burger');
  const mobileNav = document.getElementById('mobileNav');
  burger.addEventListener('click', () => mobileNav.classList.toggle('open'));
  mobileNav.querySelectorAll('a').forEach(a =>
    a.addEventListener('click', () => mobileNav.classList.remove('open'))
  );

  // Intersection Observer para .anim
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
    });
  }, { threshold: 0.08 });
  document.querySelectorAll('.anim').forEach(el => io.observe(el));

  // Marca link ativo na nav
  const path = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(a => {
    const href = new URL(a.href, location.origin).pathname;
    if (href !== '/' && path.startsWith(href)) a.classList.add('active');
  });

})();
