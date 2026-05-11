#!/usr/bin/env python3
"""
gerar_pagina_local.py — Gerador de Páginas de SEO Local com Análise de SERP
Start Corretora de Seguros

Uso:
  python scripts/gerar_pagina_local.py --localizacao "Tijuca" --uf RJ
  python scripts/gerar_pagina_local.py --localizacao "Pinheiros" --uf SP --cidade "São Paulo" --tipo bairro
  python scripts/gerar_pagina_local.py --localizacao "Petrópolis" --uf RJ --tipo cidade --sem-serp
  python scripts/gerar_pagina_local.py --slug "corretora-de-seguros-na-tijuca" --localizacao "Tijuca" --uf RJ

Requer:
  ANTHROPIC_API_KEY no arquivo .env na raiz do projeto
"""

import os
import sys
import re
import json
import argparse
import unicodedata
from datetime import datetime
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
except ImportError:
    pass

try:
    import anthropic
except ImportError:
    print("❌ Pacote 'anthropic' não encontrado. Execute: pip install anthropic python-dotenv")
    sys.exit(1)

# ─── Constantes ───────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
DOMAIN   = "https://startcorretoradeseguros.com.br"
WA       = "5521999992002"
GA       = "G-TLZ8DCN563"
TODAY    = datetime.now()
MODELO   = "claude-opus-4-7"

WA_SVG_PATH = "M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"

CSS_LOCAL = """
    :root{--primary:#00e676;--primary-dark:#00b359;--primary-glow:rgba(0,230,118,0.15);--bg:#0a0a0a;--bg2:#111111;--bg3:#1a1a1a;--bg4:#222222;--text:#ffffff;--text-muted:#999999;--border:#2a2a2a;}
    *{margin:0;padding:0;box-sizing:border-box;}
    body{font-family:'Barlow',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:var(--bg);color:var(--text);line-height:1.7;font-size:16px;}
    header{background:var(--bg2);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100;}
    .header-inner{max-width:1200px;margin:0 auto;padding:0 20px;display:flex;align-items:center;justify-content:space-between;height:64px;}
    .logo{display:flex;align-items:center;gap:10px;text-decoration:none;}
    .logo img{height:36px;width:auto;}
    nav{display:flex;align-items:center;gap:4px;}
    nav a{color:var(--text-muted);text-decoration:none;padding:6px 12px;border-radius:6px;font-size:.9rem;font-weight:500;transition:color .2s,background .2s;}
    nav a:hover{color:var(--primary);background:var(--primary-glow);}
    .btn-cta{background:var(--primary);color:#000!important;font-weight:600!important;border-radius:8px!important;padding:8px 16px!important;}
    .btn-cta:hover{background:var(--primary-dark)!important;}
    .hamburger{display:none;flex-direction:column;gap:5px;cursor:pointer;background:none;border:none;padding:4px;}
    .hamburger span{display:block;width:22px;height:2px;background:var(--text);border-radius:2px;}
    .mobile-nav{display:none;background:var(--bg2);border-bottom:1px solid var(--border);padding:16px 20px;}
    .mobile-nav a{display:block;color:var(--text-muted);text-decoration:none;padding:10px 0;font-size:.95rem;border-bottom:1px solid var(--border);}
    .mobile-nav a:last-child{border-bottom:none;}
    .mobile-nav.open{display:block;}
    .breadcrumb-bar{background:var(--bg3);padding:10px 0;border-bottom:1px solid var(--border);}
    .breadcrumb-bar .container{max-width:1200px;margin:0 auto;padding:0 20px;}
    .breadcrumb-bar nav{display:flex;flex-wrap:wrap;align-items:center;gap:6px;font-size:.85rem;color:var(--text-muted);}
    .breadcrumb-bar nav a{color:var(--primary);text-decoration:none;}
    .hero{background:linear-gradient(135deg,var(--bg2) 0%,var(--bg3) 100%);padding:64px 0 48px;border-bottom:1px solid var(--border);}
    .hero .container{max-width:1200px;margin:0 auto;padding:0 20px;}
    .hero-badge{display:inline-flex;align-items:center;gap:8px;background:var(--primary-glow);border:1px solid rgba(0,230,118,.3);color:var(--primary);padding:6px 14px;border-radius:20px;font-size:.82rem;font-weight:600;letter-spacing:.5px;margin-bottom:20px;}
    h1{font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:clamp(2rem,5vw,3rem);line-height:1.1;margin-bottom:20px;}
    h1 em{color:var(--primary);font-style:normal;}
    .hero-desc{font-size:1.1rem;color:var(--text-muted);max-width:620px;margin-bottom:32px;line-height:1.7;}
    .hero-actions{display:flex;gap:14px;flex-wrap:wrap;}
    .btn-primary{display:inline-flex;align-items:center;gap:8px;background:var(--primary);color:#000;font-weight:700;padding:14px 28px;border-radius:8px;text-decoration:none;font-size:1rem;transition:background .2s,transform .15s;}
    .btn-primary:hover{background:var(--primary-dark);transform:translateY(-1px);}
    .btn-outline{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--border);color:var(--text);padding:14px 28px;border-radius:8px;text-decoration:none;font-size:1rem;transition:border-color .2s,color .2s;}
    .btn-outline:hover{border-color:var(--primary);color:var(--primary);}
    .container{max-width:1200px;margin:0 auto;padding:0 20px;}
    main{padding:60px 0;}
    .section{margin-bottom:56px;}
    h2{font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:clamp(1.4rem,3vw,1.9rem);margin-bottom:16px;}
    h2 .accent{color:var(--primary);}
    p{color:#ccc;margin-bottom:16px;}
    .local-context{background:var(--bg3);border-left:4px solid var(--primary);padding:28px 32px;border-radius:0 12px 12px 0;}
    .local-context p{color:var(--text);margin:0 0 12px;font-size:1.05rem;line-height:1.8;}
    .local-context p:last-child{margin:0;}
    .seguros-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px;}
    .seguro-card{background:var(--bg3);border:1px solid var(--border);border-radius:12px;padding:24px;transition:border-color .2s,transform .2s;}
    .seguro-card:hover{border-color:var(--primary);transform:translateY(-2px);}
    .seguro-icon{font-size:2rem;margin-bottom:12px;}
    .seguro-card h3{font-weight:700;font-size:1.05rem;margin-bottom:8px;}
    .seguro-card p{color:var(--text-muted);font-size:.9rem;margin:0;line-height:1.6;}
    .diferenciais-list{display:flex;flex-direction:column;gap:20px;}
    .diferencial{display:flex;gap:20px;align-items:flex-start;background:var(--bg3);border:1px solid var(--border);border-radius:12px;padding:24px;}
    .diferencial-num{font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:2.5rem;color:var(--primary);line-height:1;min-width:48px;}
    .diferencial h3{font-weight:700;font-size:1.05rem;margin-bottom:6px;}
    .diferencial p{color:var(--text-muted);font-size:.93rem;margin:0;}
    .faq-item{background:var(--bg3);border:1px solid var(--border);border-radius:10px;overflow:hidden;margin-bottom:8px;}
    .faq-question{width:100%;background:none;border:none;color:var(--text);padding:20px 24px;text-align:left;cursor:pointer;font-family:inherit;font-size:1rem;font-weight:600;display:flex;justify-content:space-between;align-items:center;gap:16px;}
    .faq-question:hover{background:var(--bg4);}
    .faq-chevron{flex-shrink:0;color:var(--primary);font-size:1.2rem;}
    .faq-answer{padding:0 24px;max-height:0;overflow:hidden;transition:max-height .35s ease,padding .35s;}
    .faq-answer.open{max-height:500px;padding-bottom:20px;}
    .faq-answer p{color:#ccc;font-size:.95rem;margin:0;}
    .cta-banner{background:linear-gradient(135deg,#003d20 0%,#004d27 50%,#002d17 100%);border:1px solid rgba(0,230,118,.2);border-radius:16px;padding:52px 40px;text-align:center;position:relative;overflow:hidden;}
    .cta-banner::before{content:'';position:absolute;inset:0;background:radial-gradient(circle at 50% 0,rgba(0,230,118,.12) 0%,transparent 70%);pointer-events:none;}
    .cta-banner h2{font-size:clamp(1.5rem,4vw,2.2rem);margin-bottom:12px;}
    .cta-banner p{color:rgba(255,255,255,.7);max-width:520px;margin:0 auto 28px;}
    .cta-actions{display:flex;justify-content:center;gap:14px;flex-wrap:wrap;}
    footer{background:var(--bg2);border-top:1px solid var(--border);padding:48px 0 24px;}
    .footer-grid{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:40px;margin-bottom:40px;}
    .footer-brand .logo-text{font-family:'Barlow Condensed',sans-serif;font-weight:800;font-size:1.3rem;color:var(--text);}
    .footer-brand .tagline{font-size:.8rem;letter-spacing:2px;color:var(--text-muted);text-transform:uppercase;margin-bottom:16px;display:block;}
    .footer-brand .nap{font-size:.88rem;color:var(--text-muted);line-height:1.8;}
    .footer-brand .nap strong{color:var(--text);}
    .footer-col h4{font-weight:700;font-size:.85rem;letter-spacing:1px;text-transform:uppercase;color:var(--text-muted);margin-bottom:14px;}
    .footer-col a{display:block;color:var(--text-muted);text-decoration:none;font-size:.9rem;margin-bottom:8px;transition:color .2s;}
    .footer-col a:hover{color:var(--primary);}
    .footer-bottom{border-top:1px solid var(--border);padding-top:20px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;font-size:.82rem;color:var(--text-muted);}
    .whatsapp-float{position:fixed;bottom:28px;right:28px;z-index:999;}
    .whatsapp-float a{display:flex;align-items:center;justify-content:center;width:58px;height:58px;background:#25d366;border-radius:50%;box-shadow:0 4px 20px rgba(37,211,102,.45);animation:pulse-wa 2.4s infinite;transition:transform .2s;}
    .whatsapp-float a:hover{transform:scale(1.1);}
    @keyframes pulse-wa{0%,100%{box-shadow:0 4px 20px rgba(37,211,102,.45);}50%{box-shadow:0 4px 30px rgba(37,211,102,.7);}}
    @media(max-width:768px){nav{display:none;}.hamburger{display:flex;}.footer-grid{grid-template-columns:1fr 1fr;}.hero{padding:40px 0 32px;}.cta-banner{padding:36px 20px;}.diferencial{flex-direction:column;gap:10px;}}
    @media(max-width:480px){.footer-grid{grid-template-columns:1fr;}.hero-actions{flex-direction:column;}.cta-actions{flex-direction:column;align-items:center;}}
"""

JS_LOCAL = """
  document.getElementById('hamburger').addEventListener('click',function(){document.getElementById('mobileNav').classList.toggle('open');});
  function toggleFaq(btn){var a=btn.nextElementSibling,c=btn.querySelector('.faq-chevron'),o=a.classList.contains('open');document.querySelectorAll('.faq-answer.open').forEach(function(x){x.classList.remove('open');});document.querySelectorAll('.faq-chevron').forEach(function(x){x.textContent='+';});document.querySelectorAll('.faq-question').forEach(function(x){x.setAttribute('aria-expanded','false');});if(!o){a.classList.add('open');c.textContent='−';btn.setAttribute('aria-expanded','true');}}
"""


# ─── Utilitários ──────────────────────────────────────────────────────────────
def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-")


def extrair_texto(response) -> str:
    parts = []
    for block in response.content:
        if hasattr(block, "text") and block.text:
            parts.append(block.text)
    return "\n".join(parts)


def extrair_json(text: str) -> dict:
    match = re.search(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", text)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    depth = 0
    start = None
    for i, ch in enumerate(text):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                try:
                    return json.loads(text[start : i + 1])
                except json.JSONDecodeError:
                    start = None
    return {}


# ─── Fase 1: Análise de SERP Local ────────────────────────────────────────────
def analisar_serp_local(localizacao: str, uf: str, client: anthropic.Anthropic) -> dict:
    print(f"🔍  Analisando SERP local para: «corretora de seguros em {localizacao}»  (aguarde ~30s)...")

    keyword = f"corretora de seguros em {localizacao}"

    prompt = f"""Você é um especialista em SEO local para o mercado brasileiro de seguros.

Analise a SERP do Google Brasil para a keyword: "{keyword}"

Busque e colete dados sobre:
1. Perfil econômico e demográfico de {localizacao} ({uf}) — características relevantes para seguros
2. Principais riscos locais (índices de roubo de veículos, inundações, incêndios, densidade populacional)
3. Tipos de seguro mais procurados nessa localização
4. O que os principais resultados da SERP abordam sobre seguros em {localizacao}
5. Perguntas que moradores de {localizacao} fazem sobre seguros

Após as buscas, retorne APENAS JSON válido:

{{
  "perfil_local": "2-3 frases sobre perfil socioeconômico e características de {localizacao} relevantes para seguros",
  "riscos_locais": ["risco específico 1", "risco específico 2", "risco específico 3"],
  "seguros_demandados": ["seguro auto", "seguro residencial", "plano de saúde"],
  "diferenciais_locais": ["característica local que afeta o mercado 1", "característica 2"],
  "perguntas_locais": [
    "Pergunta específica de moradores de {localizacao} sobre seguros?",
    "Segunda pergunta?",
    "Terceira pergunta?",
    "Quarta pergunta?"
  ]
}}"""

    try:
        response = client.messages.create(
            model=MODELO,
            max_tokens=2048,
            tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 4}],
            messages=[{"role": "user", "content": prompt}],
        )
        text = extrair_texto(response)
        data = extrair_json(text)
    except anthropic.BadRequestError as e:
        print(f"  ⚠️  Web search indisponível ({e}). Usando análise por conhecimento...")
        response = client.messages.create(
            model=MODELO,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
        )
        text = extrair_texto(response)
        data = extrair_json(text)

    if not data or "perfil_local" not in data:
        print("  ⚠️  JSON incompleto. Usando defaults.")
        data = {
            "perfil_local": f"{localizacao} é uma região com mercado ativo de seguros.",
            "riscos_locais": ["roubo de veículos", "danos a imóveis", "riscos climáticos"],
            "seguros_demandados": ["seguro auto", "seguro residencial", "plano de saúde"],
            "diferenciais_locais": ["alta densidade urbana", "mix comercial e residencial"],
            "perguntas_locais": [
                f"Qual seguro auto é mais indicado para {localizacao}?",
                f"Seguro residencial em {localizacao}: o que é preciso saber?",
                f"Como contratar plano de saúde em {localizacao}?",
                f"Corretora de seguros em {localizacao} atende por WhatsApp?",
            ],
        }

    print(f"  ✅  SERP local analisada")
    return data


# ─── Fase 2: Geração de Conteúdo Local ────────────────────────────────────────
def gerar_conteudo_local(
    localizacao: str, uf: str, cidade: str, tipo: str, preposicao: str, serp: dict, client: anthropic.Anthropic
) -> dict:
    print(f"✍️   Gerando conteúdo para {localizacao}/{uf}  (aguarde ~60s)...")

    keyword = f"corretora de seguros {preposicao} {localizacao}"
    prep_cap = preposicao.capitalize()

    perguntas_str = "\n".join(f"- {p}" for p in serp.get("perguntas_locais", []))
    riscos_str    = ", ".join(serp.get("riscos_locais", []))
    demanda_str   = ", ".join(serp.get("seguros_demandados", []))

    prompt = f"""Você é um redator SEO especializado em SEO local para o mercado brasileiro de seguros.

Crie conteúdo completo para uma página de landing page local da Start Corretora de Seguros.

═══ LOCALIZAÇÃO ═══
Nome: {localizacao}
Preposição correta: {preposicao} {localizacao}
Tipo: {tipo} (bairro/cidade)
Cidade referência: {cidade}
Estado: {uf}
Keyword principal: {keyword}

═══ DADOS SERP ═══
Perfil local: {serp.get("perfil_local", "")}
Riscos locais: {riscos_str}
Seguros mais procurados: {demanda_str}

Perguntas frequentes de moradores:
{perguntas_str}

═══ EMPRESA ═══
- Start Corretora de Seguros LTDA
- Andaraí, Rio de Janeiro/RJ · CNPJ 48.385.999/0001-69
- WhatsApp: (21) 99999-2002
- Atende: foco RJ e SP, todo o Brasil remotamente
- Diferencial: corretora INDEPENDENTE — compara todas as seguradoras

═══ INSTRUÇÕES ═══
1. NUNCA use Lorem Ipsum — todo conteúdo deve ser real e específico para {localizacao}
2. meta_title: 55-65 chars com keyword + | Start Corretora
3. meta_description: 150-160 chars com keyword local e CTA
4. hero_desc: 1-2 frases impactantes sobre o mercado de seguros em {localizacao}
5. local_context: 3-4 parágrafos HTML (<p>...</p>) com análise real do perfil local, riscos, mercado imobiliário, trânsito, etc.
6. 5-6 seguros com descrição personalizada referenciando {localizacao}
7. 3 diferenciais da Start Corretora específicos para essa localização
8. 3-4 FAQs com respostas detalhadas e específicas para {localizacao}

Retorne APENAS JSON válido:

{{
  "meta_title": "Corretora de Seguros {prep_cap} {localizacao} | Start Corretora de Seguros",
  "meta_description": "meta description de 150-160 chars com keyword local e CTA",
  "hero_desc": "1-2 frases sobre o mercado de seguros em {localizacao}",
  "local_context": "<p>Parágrafo 1...</p><p>Parágrafo 2...</p><p>Parágrafo 3...</p>",
  "seguros": [
    {{"emoji": "🚗", "titulo": "Seguro Auto", "descricao": "texto específico para {localizacao}"}},
    {{"emoji": "❤️", "titulo": "Seguro de Vida", "descricao": "..."}},
    {{"emoji": "🏠", "titulo": "Seguro Residencial", "descricao": "..."}},
    {{"emoji": "🏢", "titulo": "Seguro Empresarial", "descricao": "..."}},
    {{"emoji": "🏥", "titulo": "Plano de Saúde", "descricao": "..."}},
    {{"emoji": "✈️", "titulo": "Seguro Viagem", "descricao": "..."}}
  ],
  "diferenciais": [
    {{"titulo": "diferencial 1 específico para {localizacao}", "descricao": "..."}},
    {{"titulo": "diferencial 2", "descricao": "..."}},
    {{"titulo": "diferencial 3", "descricao": "..."}}
  ],
  "faq_items": [
    {{"pergunta": "Pergunta específica sobre seguros em {localizacao}?", "resposta": "Resposta detalhada com dados reais."}},
    {{"pergunta": "Pergunta 2?", "resposta": "..."}},
    {{"pergunta": "Pergunta 3?", "resposta": "..."}},
    {{"pergunta": "Pergunta 4?", "resposta": "..."}}
  ]
}}"""

    response = client.messages.create(
        model=MODELO,
        max_tokens=6144,
        messages=[{"role": "user", "content": prompt}],
    )

    text = extrair_texto(response)
    data = extrair_json(text)

    if not data or "meta_title" not in data:
        raise ValueError(
            f"Claude não retornou JSON válido para o conteúdo local.\n"
            f"Resposta recebida:\n{text[:500]}"
        )

    print(f"  ✅  Conteúdo gerado")
    print(f"       Title: {data.get('meta_title', '')}")
    print(f"       Meta:  {data.get('meta_description', '')[:80]}...")
    return data


# ─── Fase 3: Montagem do HTML ─────────────────────────────────────────────────
def montar_html_local(
    localizacao: str, slug: str, preposicao: str, uf: str, cidade: str, conteudo: dict
) -> str:
    meta_title    = conteudo.get("meta_title", f"Corretora de Seguros em {localizacao} | Start Corretora")
    meta_desc     = conteudo.get("meta_description", "")
    hero_desc     = conteudo.get("hero_desc", "")
    local_context = conteudo.get("local_context", "")
    seguros       = conteudo.get("seguros", [])
    diferenciais  = conteudo.get("diferenciais", [])
    faq_items     = conteudo.get("faq_items", [])

    canonical  = f"{DOMAIN}/{slug}/"
    wa_link    = f"https://wa.me/{WA}?text=Ol%C3%A1!%20Gostaria%20de%20cotar%20um%20seguro%20{preposicao.replace(' ', '%20')}%20{localizacao.replace(' ', '%20')}."
    wa_float   = f"https://wa.me/{WA}?text=Ol%C3%A1!%20Vim%20pelo%20site%20e%20gostaria%20de%20fazer%20uma%20cota%C3%A7%C3%A3o%20de%20seguro."
    badge_text = f"📍 {localizacao} · {uf}"
    prep_title = f"{preposicao.capitalize()} {localizacao}"

    # JSON-LD schemas
    local_schema = {
        "@context": "https://schema.org",
        "@type": ["LocalBusiness", "InsuranceAgency"],
        "@id": canonical,
        "name": "Start Corretora de Seguros",
        "telephone": "+55-21-99999-2002",
        "image": f"{DOMAIN}/assets/images/logo.png",
        "url": canonical,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Rua Gastão Penalva, nº 15, Bloco 1, Apto. 215",
            "addressLocality": "Rio de Janeiro",
            "addressRegion": "RJ",
            "postalCode": "20540-220",
            "addressCountry": "BR",
        },
        "areaServed": {"@type": "Place", "name": localizacao},
        "priceRange": "$$",
        "openingHours": "Mo-Fr 09:00-18:00",
    }

    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
            {
                "@type": "ListItem",
                "position": 2,
                "name": f"Corretora de Seguros {prep_title}",
                "item": canonical,
            },
        ],
    }

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item.get("pergunta", ""),
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": re.sub(r"<[^>]+>", "", item.get("resposta", "")),
                },
            }
            for item in faq_items
        ],
    }

    schema_local_str      = json.dumps(local_schema, ensure_ascii=False)
    schema_breadcrumb_str = json.dumps(breadcrumb_schema, ensure_ascii=False)
    schema_faq_str        = json.dumps(faq_schema, ensure_ascii=False)

    # Seguros grid
    seguros_html = ""
    for s in seguros[:6]:
        seguros_html += (
            f'<div class="seguro-card">'
            f'<div class="seguro-icon">{s.get("emoji", "🛡️")}</div>'
            f'<h3>{s.get("titulo", "")}</h3>'
            f'<p>{s.get("descricao", "")}</p>'
            f"</div>\n        "
        )

    # Diferenciais
    diferenciais_html = ""
    for i, d in enumerate(diferenciais[:3], 1):
        num = f"0{i}"
        diferenciais_html += (
            f'<div class="diferencial">'
            f'<div class="diferencial-num">{num}</div>'
            f"<div>"
            f'<h3>{d.get("titulo", "")}</h3>'
            f'<p>{d.get("descricao", "")}</p>'
            f"</div>"
            f"</div>\n        "
        )

    # FAQ
    faq_html = ""
    for item in faq_items:
        faq_html += (
            f'<div class="faq-item">'
            f'<button class="faq-question" onclick="toggleFaq(this)" aria-expanded="false">'
            f'<span>{item.get("pergunta", "")}</span>'
            f'<span class="faq-chevron">+</span>'
            f"</button>"
            f'<div class="faq-answer">'
            f'<p>{item.get("resposta", "")}</p>'
            f"</div>"
            f"</div>\n        "
        )

    wa_svg = f'<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="{WA_SVG_PATH}"/></svg>'
    wa_svg_float = f'<svg width="28" height="28" viewBox="0 0 24 24" fill="#fff"><path d="{WA_SVG_PATH}"/></svg>'

    year = TODAY.year

    html = (
        "<!DOCTYPE html>\n"
        '<html lang="pt-BR">\n'
        "<head>\n"
        '  <meta charset="UTF-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f"  <title>{meta_title}</title>\n"
        f'  <meta name="description" content="{meta_desc}">\n'
        f'  <link rel="canonical" href="{canonical}">\n'
        '  <meta name="robots" content="index, follow">\n'
        f'  <meta property="og:title" content="{meta_title}">\n'
        f'  <meta property="og:description" content="{meta_desc}">\n'
        f'  <meta property="og:url" content="{canonical}">\n'
        '  <meta property="og:type" content="website">\n'
        f'  <meta property="og:image" content="{DOMAIN}/assets/images/logo.png">\n'
        '  <link rel="icon" type="image/png" href="/assets/images/favicon.png">\n'
        '  <link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '  <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@800&family=Barlow:wght@400;500;600&display=swap" rel="stylesheet">\n'
        '  <script type="application/ld+json">\n'
        f"  {schema_local_str}\n"
        "  </script>\n"
        '  <script type="application/ld+json">\n'
        f"  {schema_breadcrumb_str}\n"
        "  </script>\n"
        '  <script type="application/ld+json">\n'
        f"  {schema_faq_str}\n"
        "  </script>\n"
        f'  <script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>\n'
        "  <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());"
        f"gtag('config','{GA}');</script>\n"
        "  <style>\n"
        + CSS_LOCAL +
        "  </style>\n"
        "</head>\n"
        "<body>\n"
        "<header>\n"
        '  <div class="header-inner">\n'
        f'    <a href="/" class="logo"><img src="/assets/images/logo.png" alt="Start Corretora de Seguros" loading="lazy"></a>\n'
        "    <nav>\n"
        '      <a href="/">Home</a>\n'
        '      <a href="/seguro-de-vida">Seguro de Vida</a>\n'
        '      <a href="/plano-de-saude">Plano de Saúde</a>\n'
        '      <a href="/seguro-auto">Seguro Auto</a>\n'
        '      <a href="/seguro-empresarial">Empresarial</a>\n'
        '      <a href="/blog">Blog</a>\n'
        f'      <a href="{wa_link}" class="btn-cta" target="_blank" rel="noopener">📲 Cotação Grátis</a>\n'
        "    </nav>\n"
        '    <button class="hamburger" id="hamburger" aria-label="Menu"><span></span><span></span><span></span></button>\n'
        "  </div>\n"
        '  <div class="mobile-nav" id="mobileNav">\n'
        '    <a href="/">Home</a><a href="/seguro-de-vida">Seguro de Vida</a><a href="/plano-de-saude">Plano de Saúde</a>'
        '<a href="/seguro-auto">Seguro Auto</a><a href="/seguro-empresarial">Para Empresas</a>'
        '<a href="/seguro-residencial">Residencial</a><a href="/blog">Blog</a><a href="/contato">Contato</a>\n'
        f'    <a href="{wa_link}" target="_blank" rel="noopener" style="color:#00e676;font-weight:600;">📲 Cotação Grátis via WhatsApp</a>\n'
        "  </div>\n"
        "</header>\n\n"
        '<div class="breadcrumb-bar">\n'
        '  <div class="container">\n'
        '    <nav aria-label="breadcrumb">\n'
        f'      <a href="/">Home</a><span>›</span><span>Corretora de Seguros {prep_title}</span>\n'
        "    </nav>\n"
        "  </div>\n"
        "</div>\n\n"
        '<section class="hero">\n'
        '  <div class="container">\n'
        f'    <div class="hero-badge">{badge_text}</div>\n'
        f'    <h1>Corretora de Seguros<br><em>{prep_title}</em></h1>\n'
        f'    <p class="hero-desc">{hero_desc}</p>\n'
        '    <div class="hero-actions">\n'
        f'      <a href="{wa_link}" class="btn-primary" target="_blank" rel="noopener">\n'
        f"        {wa_svg}\n"
        "        Solicitar Cotação Grátis\n"
        "      </a>\n"
        '      <a href="tel:+5521999992002" class="btn-outline">📞 (21) 99999-2002</a>\n'
        "    </div>\n"
        "  </div>\n"
        "</section>\n\n"
        "<main>\n"
        '  <div class="container">\n\n'
        '    <section class="section">\n'
        f'      <h2>Seguros <span class="accent">{prep_title}</span>: entenda o cenário local</h2>\n'
        '      <div class="local-context">\n'
        f"        {local_context}\n"
        "      </div>\n"
        "    </section>\n\n"
        '    <section class="section">\n'
        f'      <h2>Seguros disponíveis <span class="accent">{prep_title}</span></h2>\n'
        f'      <p style="margin-bottom:28px;">Trabalhamos com as principais seguradoras para encontrar a melhor cobertura para moradores e empresas {prep_title}.</p>\n'
        '      <div class="seguros-grid">\n'
        f"        {seguros_html}"
        "      </div>\n"
        "    </section>\n\n"
        '    <section class="section">\n'
        '      <h2>Por que escolher a <span class="accent">Start Corretora</span>?</h2>\n'
        '      <div class="diferenciais-list">\n'
        f"        {diferenciais_html}"
        "      </div>\n"
        "    </section>\n\n"
        '    <section class="section">\n'
        f'      <h2>Perguntas frequentes sobre <span class="accent">seguros {prep_title}</span></h2>\n'
        '      <div class="faq-list">\n'
        f"        {faq_html}"
        "      </div>\n"
        "    </section>\n\n"
        '    <section class="section">\n'
        '      <div class="cta-banner">\n'
        f'        <h2>Faça sua Cotação Grátis {prep_title}</h2>\n'
        f'        <p>Atendimento rápido pelo WhatsApp. Resposta em até 2 horas com as melhores propostas do mercado.</p>\n'
        '        <div class="cta-actions">\n'
        f'          <a href="{wa_link}" class="btn-primary" target="_blank" rel="noopener">\n'
        f"            {wa_svg}\n"
        "            Cotar pelo WhatsApp\n"
        "          </a>\n"
        '          <a href="/contato" class="btn-outline">Enviar Mensagem</a>\n'
        "        </div>\n"
        "      </div>\n"
        "    </section>\n\n"
        "  </div>\n"
        "</main>\n\n"
        "<footer>\n"
        '  <div class="container">\n'
        '    <div class="footer-grid">\n'
        '      <div class="footer-brand">\n'
        '        <div class="logo-text">START</div>\n'
        '        <span class="tagline">Corretora de Seguros</span>\n'
        '        <div class="nap"><strong>Start Corretora de Seguros LTDA</strong><br>'
        "Rua Gastão Penalva, nº 15, Bloco 1, Apto. 215<br>"
        "Andaraí — Rio de Janeiro/RJ — CEP 20540-220<br>"
        "CNPJ: 48.385.999/0001-69<br>"
        "<strong>WhatsApp: (21) 99999-2002</strong></div>\n"
        "      </div>\n"
        '      <div class="footer-col"><h4>Seguros</h4>'
        '<a href="/seguro-de-vida">Seguro de Vida</a>'
        '<a href="/plano-de-saude">Plano de Saúde</a>'
        '<a href="/seguro-auto">Seguro Auto</a>'
        '<a href="/seguro-residencial">Residencial</a>'
        '<a href="/seguro-empresarial">Empresarial</a></div>\n'
        '      <div class="footer-col"><h4>Regiões</h4>'
        '<a href="/corretora-de-seguros-em-copacabana">Copacabana</a>'
        '<a href="/corretora-de-seguros-em-ipanema">Ipanema</a>'
        '<a href="/corretora-de-seguros-no-leblon">Leblon</a>'
        '<a href="/corretora-de-seguros-na-barra-da-tijuca">Barra da Tijuca</a>'
        '<a href="/corretora-de-seguros-em-niteroi">Niterói</a></div>\n'
        '      <div class="footer-col"><h4>Empresa</h4>'
        '<a href="/sobre">Quem Somos</a>'
        '<a href="/contato">Contato</a>'
        '<a href="/blog">Blog</a></div>\n'
        "    </div>\n"
        '    <div class="footer-bottom">'
        "<span>SUSEP · Todos os seguros são regulamentados pela SUSEP</span>"
        f"<span>&copy; {year} Start Corretora de Seguros. Todos os direitos reservados.</span>"
        "</div>\n"
        "  </div>\n"
        "</footer>\n\n"
        '<div class="whatsapp-float">\n'
        f'  <a href="{wa_float}" target="_blank" rel="noopener" aria-label="Falar no WhatsApp">\n'
        f"    {wa_svg_float}\n"
        "  </a>\n"
        "</div>\n"
        "<script>\n"
        + JS_LOCAL +
        "</script>\n"
        "</body>\n"
        "</html>"
    )

    return html


# ─── Sitemap ──────────────────────────────────────────────────────────────────
def adicionar_ao_sitemap(slug: str) -> bool:
    sitemap_path = BASE_DIR / "sitemap.xml"
    url = f"{DOMAIN}/{slug}/"
    content = sitemap_path.read_text(encoding="utf-8")

    if url in content:
        print(f"  ⚠️  URL já existe no sitemap.xml — pulando.")
        return False

    entry = (
        f"  <url>\n"
        f"    <loc>{url}</loc>\n"
        f"    <lastmod>{TODAY.strftime('%Y-%m-%d')}</lastmod>\n"
        f"    <changefreq>monthly</changefreq>\n"
        f"    <priority>0.85</priority>\n"
        f"  </url>\n"
    )
    updated = content.replace("</urlset>", entry + "</urlset>")
    sitemap_path.write_text(updated, encoding="utf-8")
    return True


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Gera página de SEO local para a Start Corretora",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Exemplos:
  python scripts/gerar_pagina_local.py --localizacao "Tijuca" --uf RJ
  python scripts/gerar_pagina_local.py --localizacao "Pinheiros" --uf SP --cidade "São Paulo"
  python scripts/gerar_pagina_local.py --localizacao "Petrópolis" --uf RJ --tipo cidade --sem-serp
""",
    )
    parser.add_argument("--localizacao", required=True, help="Nome do bairro ou cidade (ex: 'Tijuca', 'Petrópolis')")
    parser.add_argument("--uf",          required=True, help="Estado (ex: RJ, SP)")
    parser.add_argument("--cidade",      default=None,  help="Cidade (padrão: Rio de Janeiro para RJ, São Paulo para SP)")
    parser.add_argument("--tipo",        default="bairro", choices=["bairro", "cidade"], help="Tipo de localização")
    parser.add_argument("--preposicao",  default=None,  help="Preposição (em/na/no/nos) — detectada automaticamente se omitida")
    parser.add_argument("--slug",        default=None,  help="Slug personalizado (gerado automaticamente se omitido)")
    parser.add_argument("--sem-serp",    action="store_true", help="Pula análise de SERP (mais rápido)")
    args = parser.parse_args()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌  ANTHROPIC_API_KEY não encontrada.")
        print("    Crie o arquivo .env na raiz do projeto com:")
        print("    ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)

    client       = anthropic.Anthropic(api_key=api_key)
    localizacao  = args.localizacao.strip()
    uf           = args.uf.strip().upper()

    cidade_default = {"RJ": "Rio de Janeiro", "SP": "São Paulo"}.get(uf, localizacao if args.tipo == "cidade" else "")
    cidade         = args.cidade or cidade_default or localizacao

    # Determina preposição automaticamente se não fornecida
    if args.preposicao:
        preposicao = args.preposicao
    else:
        lc = localizacao.lower()
        if lc.startswith(("a ", "andar", "angra", "armação")):
            preposicao = "no"
        elif lc in ("tijuca", "gávea", "gavea", "glória", "gloria", "lagoa", "lapa", "penha", "mooca", "urca", "vila madalena", "ilha do governador"):
            preposicao = "na"
        elif lc.startswith("vila "):
            preposicao = "na"
        elif lc in ("jardins",):
            preposicao = "nos"
        elif lc in ("flamengo", "catete", "leme", "meier", "méier", "maracanã", "morumbi", "brooklin", "recreio dos bandeirantes", "tatuapé", "andarai", "andaraí", "grajaú", "grajau", "humaitá", "humaita", "leblon", "jardim botânico", "jardim botanico", "itaim bibi"):
            preposicao = "no"
        else:
            preposicao = "em"

    # Slug
    slug = args.slug
    if not slug:
        prep_slug = {
            "em": "em", "na": "na", "no": "no", "nos": "nos",
            "em ": "em", "na ": "na", "no ": "no",
        }.get(preposicao, "em")
        loc_slug = slugify(localizacao)
        slug = f"corretora-de-seguros-{prep_slug}-{loc_slug}"

    # Verifica se já existe
    output_dir = BASE_DIR / slug
    if output_dir.exists() and (output_dir / "index.html").exists():
        print(f"⚠️  Página já existe: {output_dir}/index.html — abortando (use --slug diferente para forçar).")
        sys.exit(0)

    print(f"\n{'═'*60}")
    print(f"  GERADOR DE PÁGINA LOCAL — START CORRETORA")
    print(f"{'═'*60}")
    print(f"  Localização : {localizacao} ({uf})")
    print(f"  Preposição  : {preposicao}")
    print(f"  Slug        : {slug}")
    print(f"  SERP        : {'desativada' if args.sem_serp else 'ativada'}")
    print(f"{'─'*60}\n")

    # Fase 1 — SERP
    if args.sem_serp:
        print("⏭️   Pulando análise SERP")
        serp = {
            "perfil_local": f"{localizacao} é uma região com mercado ativo de seguros no estado de {uf}.",
            "riscos_locais": ["roubo de veículos", "danos a imóveis", "riscos climáticos"],
            "seguros_demandados": ["seguro auto", "seguro residencial", "plano de saúde"],
            "diferenciais_locais": [],
            "perguntas_locais": [
                f"Qual seguro auto é recomendado para moradores de {localizacao}?",
                f"O seguro residencial em {localizacao} cobre roubo de bens?",
                f"Como contratar plano de saúde em {localizacao}?",
                f"A Start Corretora atende por WhatsApp para moradores de {localizacao}?",
            ],
        }
    else:
        serp = analisar_serp_local(localizacao, uf, client)

    # Fase 2 — Conteúdo
    conteudo = gerar_conteudo_local(localizacao, uf, cidade, args.tipo, preposicao, serp, client)

    # Fase 3 — HTML
    print(f"🏗️   Montando HTML...")
    html = montar_html_local(localizacao, slug, preposicao, uf, cidade, conteudo)

    # Salvar
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "index.html"
    output_path.write_text(html, encoding="utf-8")

    # Atualizar sitemap
    print(f"🗺️   Atualizando sitemap.xml...")
    adicionar_ao_sitemap(slug)

    print(f"\n{'═'*60}")
    print(f"  ✅  PÁGINA LOCAL GERADA COM SUCESSO")
    print(f"{'─'*60}")
    print(f"  Arquivo : {output_path}")
    print(f"  URL     : {DOMAIN}/{slug}/")
    print(f"  Title   : {conteudo.get('meta_title', '')}")
    print(f"{'═'*60}\n")
    print("📌 Próximos passos:")
    print(f"   git add {slug}/")
    print(f"   git add sitemap.xml")
    print(f"   git commit -m \"feat: página local SEO — {localizacao}\"")
    print(f"   git push\n")


if __name__ == "__main__":
    main()
