#!/usr/bin/env python3
"""
gerar_conteudo.py — Gerador de Conteúdo SEO com Análise de SERP
Start Corretora de Seguros

Uso:
  python scripts/gerar_conteudo.py "seguro de vida para autônomo"
  python scripts/gerar_conteudo.py "plano de saúde individual" --categoria saude
  python scripts/gerar_conteudo.py "seguro auto rj" --slug seguro-auto-rio-de-janeiro-guia --sem-serp

Requer:
  ANTHROPIC_API_KEY no arquivo .env (na raiz do projeto)
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

# ─── Constantes ────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
BLOG_DIR = BASE_DIR / "blog"
DOMAIN   = "https://startcorretoradeseguros.com.br"
WA       = "5521999992002"
GA       = "G-TLZ8DCN563"
TODAY    = datetime.now()

_MODELO_DEFAULT = "claude-opus-4-7"
MODELO_ANALISE  = os.getenv("ANTHROPIC_MODEL", _MODELO_DEFAULT)
MODELO_CONTEUDO = os.getenv("ANTHROPIC_MODEL", _MODELO_DEFAULT)

CATEGORIAS = {
    "vida":        ("label-vida",        "Seguro de Vida"),
    "auto":        ("label-auto",        "Seguro Auto"),
    "saude":       ("label-saude",       "Plano de Saúde"),
    "residencial": ("label-residencial", "Seguro Residencial"),
    "empresarial": ("label-empresarial", "Seguro Empresarial"),
    "geral":       ("label-geral",       "Seguros"),
}

POSTS_RELACIONADOS = {
    "vida": [
        ("quanto-custa-seguro-de-vida-500mil.html",            "💰", "Quanto Custa um Seguro de Vida de 500 Mil?",  "15 jan 2026"),
        ("beneficios-do-seguro-de-vida.html",                  "🛡️", "Benefícios do Seguro de Vida",               "10 dez 2025"),
        ("doenca-grave-seguro-de-vida.html",                   "🏥", "Doenças Graves no Seguro de Vida",           "05 nov 2025"),
    ],
    "auto": [
        ("seguro-auto-rj.html",                                "🚗", "Seguro Auto no Rio de Janeiro",              "20 jan 2026"),
        ("seguro-de-vida-por-que-investir-hoje.html",          "❤️", "Por Que Investir em Seguro de Vida?",        "03 set 2025"),
    ],
    "saude": [
        ("plano-de-saude-sp.html",                             "🏥", "Plano de Saúde em São Paulo",                "12 jan 2026"),
        ("seguro-de-vida-por-que-investir-hoje.html",          "❤️", "Por Que Investir em Seguro de Vida?",        "03 set 2025"),
    ],
    "geral": [
        ("seguro-de-vida-por-que-investir-hoje.html",          "❤️", "Por Que Investir em Seguro de Vida?",        "03 set 2025"),
        ("seguro-auto-rj.html",                                "🚗", "Seguro Auto no Rio de Janeiro",              "20 jan 2026"),
        ("plano-de-saude-sp.html",                             "🏥", "Plano de Saúde em São Paulo",                "12 jan 2026"),
    ],
}
POSTS_RELACIONADOS["residencial"] = POSTS_RELACIONADOS["geral"]
POSTS_RELACIONADOS["empresarial"] = POSTS_RELACIONADOS["geral"]

WA_ICON_SVG = """<svg width="28" height="28" viewBox="0 0 24 24" fill="white">
    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
    <path d="M12 0C5.373 0 0 5.373 0 12c0 2.124.556 4.118 1.526 5.843L.063 22.853c-.086.224-.027.476.148.64.124.115.284.175.444.175.071 0 .143-.012.213-.037l5.2-1.705A11.934 11.934 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.818c-1.992 0-3.837-.6-5.373-1.627l-.367-.229-3.799 1.247 1.225-3.669-.243-.393C2.427 15.598 1.818 13.864 1.818 12 1.818 6.367 6.367 1.818 12 1.818S22.182 6.367 22.182 12 17.633 21.818 12 21.818z"/>
  </svg>"""

WA_BTN_SVG = """<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.124.556 4.118 1.526 5.843L.063 22.853c-.086.224-.027.476.148.64.124.115.284.175.444.175.071 0 .143-.012.213-.037l5.2-1.705A11.934 11.934 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.818c-1.992 0-3.837-.6-5.373-1.627l-.367-.229-3.799 1.247 1.225-3.669-.243-.393C2.427 15.598 1.818 13.864 1.818 12 1.818 6.367 6.367 1.818 12 1.818S22.182 6.367 22.182 12 17.633 21.818 12 21.818z"/></svg>"""


# ─── Utilitários ──────────────────────────────────────────────────────
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
    # Tenta bloco de código ```json ... ```
    match = re.search(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", text)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    # Tenta o primeiro { ... } de nível raiz
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


def serp_defaults(keyword: str) -> dict:
    return {
        "intent": "mista",
        "formato_dominante": "artigo",
        "word_count_recomendado": 1800,
        "titulos_concorrentes": [],
        "h2s_frequentes": [],
        "topicos_obrigatorios": [],
        "topicos_oportunidade": [],
        "perguntas_paa": [
            f"O que é {keyword}?",
            f"Como funciona o {keyword}?",
            f"Quanto custa {keyword}?",
            f"Vale a pena contratar {keyword}?",
            f"Como contratar {keyword} online?",
        ],
        "lsi_keywords": [],
        "tom": "educativo",
    }


# ─── Fase 1: Análise de SERP ──────────────────────────────────────────────
def analisar_serp(keyword: str, client: anthropic.Anthropic) -> dict:
    print(f"🔍  Analisando SERP para: «{keyword}»  (aguarde ~30s)...")

    prompt = f"""Você é um especialista em SEO para o mercado brasileiro de seguros.

Analise a SERP (resultados de busca do Google Brasil) para a palavra-chave: "{keyword}"

Faça buscas para coletar dados sobre:
1. Os top 5-7 resultados orgânicos para "{keyword}" no Google Brasil
2. Perguntas frequentes relacionadas (People Also Ask / PAA)
3. Termos semânticos e LSI keywords relacionados

Após as buscas, retorne APENAS um objeto JSON válido, sem texto antes ou depois:

{{
  "intent": "informacional|transacional|navegacional|mista",
  "formato_dominante": "artigo|lista|guia|comparativo|landing_page",
  "word_count_recomendado": 1800,
  "titulos_concorrentes": [
    "título do 1º resultado",
    "título do 2º resultado",
    "título do 3º resultado"
  ],
  "h2s_frequentes": [
    "H2 que aparece nos top resultados 1",
    "H2 que aparece nos top resultados 2",
    "H2 que aparece nos top resultados 3",
    "H2 que aparece nos top resultados 4"
  ],
  "topicos_obrigatorios": [
    "tópico coberto em TODOS os top resultados 1",
    "tópico coberto em TODOS os top resultados 2",
    "tópico coberto em TODOS os top resultados 3"
  ],
  "topicos_oportunidade": [
    "tópico pouco coberto mas relevante 1",
    "tópico pouco coberto mas relevante 2"
  ],
  "perguntas_paa": [
    "pergunta frequente encontrada na SERP 1?",
    "pergunta frequente encontrada na SERP 2?",
    "pergunta frequente encontrada na SERP 3?",
    "pergunta frequente encontrada na SERP 4?",
    "pergunta frequente encontrada na SERP 5?"
  ],
  "lsi_keywords": [
    "palavra semanticamente relacionada 1",
    "palavra semanticamente relacionada 2",
    "palavra semanticamente relacionada 3",
    "palavra semanticamente relacionada 4",
    "palavra semanticamente relacionada 5"
  ],
  "tom": "educativo|consultivo|técnico|comercial"
}}"""

    try:
        response = client.messages.create(
            model=MODELO_ANALISE,
            max_tokens=4096,
            tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}],
            messages=[{"role": "user", "content": prompt}],
        )
        text = extrair_texto(response)
        data = extrair_json(text)
    except anthropic.BadRequestError as e:
        print(f"  ⚠️  Web search não disponível ({e}). Usando análise por conhecimento...")
        # Fallback sem web_search
        response = client.messages.create(
            model=MODELO_ANALISE,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        text = extrair_texto(response)
        data = extrair_json(text)

    if not data or "perguntas_paa" not in data:
        print("  ⚠️  JSON incompleto na resposta. Usando defaults.")
        data = serp_defaults(keyword)

    n_perguntas = len(data.get("perguntas_paa", []))
    n_h2s = len(data.get("h2s_frequentes", []))
    print(f"  ✅  SERP analisada — {n_perguntas} perguntas PAA · {n_h2s} H2s identificados")
    return data


# ─── Fase 2: Geração de Conteúdo ───────────────────────────────────────────────
def gerar_conteudo(keyword: str, serp: dict, client: anthropic.Anthropic) -> dict:
    print(f"✍️   Gerando conteúdo SEO (aguarde ~60s)...")

    h2s_str       = "\n".join(f"- {h}" for h in serp.get("h2s_frequentes", []))
    topicos_str   = "\n".join(f"- {t}" for t in serp.get("topicos_obrigatorios", []))
    opor_str      = "\n".join(f"- {t}" for t in serp.get("topicos_oportunidade", []))
    perguntas_str = "\n".join(f"- {p}" for p in serp.get("perguntas_paa", []))
    lsi_str       = ", ".join(serp.get("lsi_keywords", []))
    tom           = serp.get("tom", "educativo")
    wc            = serp.get("word_count_recomendado", 1800)

    prompt = f"""Você é um redator SEO especializado no mercado brasileiro de seguros.
Escreva um artigo completo para o blog da Start Corretora de Seguros.

═══ PALAVRA-CHAVE PRINCIPAL ═══
{keyword}

═══ ANÁLISE SERP ═══
Intenção do usuário: {serp.get('intent', 'mista')}
Formato ideal: {serp.get('formato_dominante', 'artigo')}
Meta de palavras: {wc}
Tom de voz: {tom}

H2s presentes nos top resultados:
{h2s_str or '(use seu conhecimento de seguros)'}

Tópicos obrigatórios (todos cobrem):
{topicos_str or '(use seu conhecimento de seguros)'}

Tópicos diferenciadores (pouco cobertos, oportunidade):
{opor_str or '(use sua criatividade)'}

LSI Keywords a incluir naturalmente:
{lsi_str or keyword}

Perguntas frequentes (PAA):
{perguntas_str}

═══ EMPRESA ═══
- Start Corretora de Seguros LTDA
- Andaraí, Rio de Janeiro/RJ · CNPJ 48.385.999/0001-69
- WhatsApp: (21) 99999-2002
- Atende: foco RJ e SP, todo o Brasil remotamente
- Diferencial: corretora INDEPENDENTE — compara todas as seguradoras

═══ REGRAS OBRIGATÓRIAS ═══
1. H1 único contendo a palavra-chave. 55-65 caracteres.
2. Meta description: 150-160 caracteres, inclui keyword + CTA
3. Estrutura de headings: H2 para seções principais, H3 para subseções
4. Palavra-chave na densidade de 1-2% (natural, sem keyword stuffing)
5. Inclua dados reais: SUSEP, ANS, IBGE, CNSeg, Fenaprevi
6. Inclua pelo menos UMA <table> comparativa ou de preços
7. Inclua pelo menos UM <div class="highlight-box"> com dado impactante
8. FAQ ao final com as perguntas PAA e respostas completas (3-5 parágrafos cada)
9. Último parágrafo: CTA mencionando a Start Corretora e WhatsApp
10. Tom {tom} mas acessível ao público leigo
11. Corpo em HTML semântico: <p>, <ul>, <ol>, <table>, <strong>, <em>
12. Use <h2> e <h3> mas NÃO use <h1> — o H1 vai no campo titulo_h1
13. NÃO inclua <html>, <head>, <body>, <nav>, <footer> — só o conteúdo do artigo

═══ FORMATO DE RESPOSTA ═══
Retorne APENAS um JSON válido, sem nenhum texto antes ou depois:

{{
  "titulo_h1": "H1 com a keyword (55-65 chars)",
  "meta_title": "Title tag SEO com keyword | Start Corretora (55-65 chars)",
  "meta_description": "Meta description de exatamente 150-160 chars incluindo keyword e CTA",
  "slug": "url-amigavel-baseada-na-keyword-sem-acentos",
  "categoria": "vida|auto|saude|residencial|empresarial|geral",
  "corpo_html": "<p>Parágrafo de abertura impactante...</p>\\n<h2>...</h2>...",
  "faq_items": [
    {{"pergunta": "Pergunta completa?", "resposta": "Resposta detalhada com 2-4 parágrafos."}},
    {{"pergunta": "Pergunta completa?", "resposta": "Resposta detalhada."}},
    {{"pergunta": "Pergunta completa?", "resposta": "Resposta detalhada."}},
    {{"pergunta": "Pergunta completa?", "resposta": "Resposta detalhada."}},
    {{"pergunta": "Pergunta completa?", "resposta": "Resposta detalhada."}}
  ],
  "imagem_alt": "Descrição da imagem de capa para atributo alt",
  "wa_mensagem": "Ol%C3%A1!%20Li%20o%20artigo%20sobre%20{keyword.replace(' ', '%20')}%20e%20gostaria%20de%20uma%20cota%C3%A7%C3%A3o."
}}"""

    messages = [{"role": "user", "content": prompt}]
    response = client.messages.create(
        model=MODELO_CONTEUDO,
        max_tokens=8192,
        messages=messages,
    )

    text = extrair_texto(response)

    # Se truncado, pedir para o modelo completar o JSON
    if response.stop_reason == "max_tokens":
        print("  ⚠️  Resposta truncada — solicitando continuação...")
        cont = client.messages.create(
            model=MODELO_CONTEUDO,
            max_tokens=4096,
            messages=messages + [
                {"role": "assistant", "content": text},
                {"role": "user", "content": "Continue exatamente de onde parou, completando o JSON até o fechamento final }."},
            ],
        )
        text = text + extrair_texto(cont)

    data = extrair_json(text)

    if not data or "titulo_h1" not in data:
        raise ValueError(
            "Claude não retornou JSON válido para o conteúdo.\n"
            f"Resposta recebida:\n{text[:500]}"
        )

    print(f"  ✅  Conteúdo gerado")
    print(f"       H1:   {data.get('titulo_h1', '')}")
    print(f"       Meta: {data.get('meta_description', '')[:80]}...")
    return data


# ─── Fase 3: Montagem do HTML ───────────────────────────────────────────────
def montar_html(keyword: str, slug: str, conteudo: dict, serp: dict) -> str:
    titulo_h1 = conteudo.get("titulo_h1", keyword)
    meta_title = conteudo.get("meta_title", titulo_h1)
    meta_desc  = conteudo.get("meta_description", "")
    corpo      = conteudo.get("corpo_html", "")
    faqs       = conteudo.get("faq_items", [])
    imagem_alt = conteudo.get("imagem_alt", titulo_h1)
    wa_msg     = conteudo.get("wa_mensagem", "Ol%C3%A1!%20Gostaria%20de%20uma%20cota%C3%A7%C3%A3o.")

    cat_key = conteudo.get("categoria", "geral")
    if cat_key not in CATEGORIAS:
        cat_key = "geral"
    cat_class, cat_label = CATEGORIAS[cat_key]

    data_pub  = conteudo.get("data_publicacao") or TODAY.strftime("%-d de %B de %Y")
    canonical = f"{DOMAIN}/blog/{slug}"
    art_url   = f"{canonical}.html"

    # Posts relacionados
    relacionados = POSTS_RELACIONADOS.get(cat_key, POSTS_RELACIONADOS["geral"])
    rel_html = ""
    for href, ico, tit, dt in relacionados[:3]:
        rel_html += f"""
            <div class="related-item">
              <div class="related-ico">{ico}</div>
              <div>
                <a href="{href}">{tit}</a>
                <time>{dt}</time>
              </div>
            </div>"""

    # FAQ HTML (dentro do artigo)
    faq_html = ""
    if faqs:
        faq_html = '<h2>Perguntas Frequentes</h2>\n<dl class="faq-list">\n'
        for item in faqs:
            faq_html += f'  <dt><strong>{item.get("pergunta", "")}</strong></dt>\n'
            faq_html += f'  <dd>{item.get("resposta", "")}</dd>\n'
        faq_html += "</dl>\n"

    # FAQ Schema JSON-LD
    faq_schema = ""
    if faqs:
        faq_entities = [
            {
                "@type": "Question",
                "name": item.get("pergunta", ""),
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": re.sub(r"<[^>]+>", "", item.get("resposta", "")),
                },
            }
            for item in faqs
        ]
        faq_schema_obj = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_entities,
        }
        faq_schema = (
            f'  <script type="application/ld+json">\n'
            f"  {json.dumps(faq_schema_obj, ensure_ascii=False, indent=2)}\n"
            f"  </script>"
        )

    # Share URLs (simples)
    enc_url   = art_url.replace(":", "%3A").replace("/", "%2F")
    enc_title = meta_title.replace(" ", "%20")
    share_wa  = f"https://wa.me/?text={enc_title}%20-%20{enc_url}"
    share_fb  = f"https://www.facebook.com/sharer/sharer.php?u={enc_url}"
    share_tw  = f"https://twitter.com/intent/tweet?url={enc_url}&text={enc_title}"

    article_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": titulo_h1,
        "author": {"@type": "Organization", "name": "Start Corretora de Seguros"},
        "publisher": {
            "@type": "Organization",
            "name": "Start Corretora de Seguros",
            "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/assets/images/logo.png"},
        },
        "datePublished": TODAY.strftime("%Y-%m-%d"),
        "dateModified":  TODAY.strftime("%Y-%m-%d"),
        "image": f"{DOMAIN}/assets/images/logo.png",
        "url": art_url,
    }, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{meta_title}</title>
  <meta name="description" content="{meta_desc}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{art_url}">
  <meta property="og:title" content="{meta_title}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:image" content="{DOMAIN}/assets/images/logo.png">
  <link rel="stylesheet" href="../assets/css/noturno.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": ["LocalBusiness", "InsuranceAgency"],
    "@id": "{DOMAIN}/#business",
    "name": "Start Corretora de Seguros LTDA",
    "url": "{DOMAIN}",
    "telephone": "+55-21-99999-2002",
    "image": "{DOMAIN}/assets/images/logo-start-corretora.png",
    "logo": {{
      "@type": "ImageObject",
      "url": "{DOMAIN}/assets/images/logo-start-corretora.png"
    }},
    "address": {{
      "@type": "PostalAddress",
      "streetAddress": "Rua Gastão Penalva, nº 15, Bloco 1, Apto. 215",
      "addressLocality": "Rio de Janeiro",
      "addressRegion": "RJ",
      "postalCode": "20540-220",
      "addressCountry": "BR"
    }},
    "openingHoursSpecification": [
      {{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "09:00", "closes": "18:00"}},
      {{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "09:00", "closes": "13:00"}}
    ],
    "areaServed": [
      {{"@type": "City", "name": "Rio de Janeiro"}},
      {{"@type": "City", "name": "São Paulo"}}
    ],
    "priceRange": "$",
    "currenciesAccepted": "BRL"
  }}
  </script>
  <script type="application/ld+json">
  {article_schema}
  </script>
{faq_schema}
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GA}');
  </script>
</head>
<body>

<nav class="nav" id="mainNav">
  <div class="nav-inner container">
    <a href="../index.html" class="nav-logo">
      <img src="../assets/images/logo-start-corretora.png" alt="Start Corretora de Seguros" style="height:44px;width:auto">
    </a>
    <ul class="nav-links">
      <li><a href="../seguro-de-vida.html">Seguro de Vida</a></li>
      <li><a href="../plano-de-saude.html">Plano de Saúde</a></li>
      <li><a href="../seguro-auto.html">Seguro Auto</a></li>
      <li><a href="index.html" class="active">Blog</a></li>
      <li><a href="../sobre.html">Sobre</a></li>
      <li><a href="../contato.html">Contato</a></li>
    </ul>
    <div class="nav-end">
      <a href="../contato.html" class="btn btn-outline">Contato</a>
      <a href="https://wa.me/{WA}?text=Ol%C3%A1!%20Gostaria%20de%20fazer%20uma%20cota%C3%A7%C3%A3o."
         class="btn btn-green" target="_blank" rel="noopener">
        {WA_BTN_SVG}
        Cotar agora
      </a>
    </div>
    <div class="nav-burger" id="burger" aria-label="Menu">
      <span></span><span></span><span></span>
    </div>
  </div>
</nav>

<div class="mobile-menu" id="mobileMenu">
  <a href="../index.html">Home</a>
  <a href="../seguro-de-vida.html">Seguro de Vida</a>
  <a href="../plano-de-saude.html">Plano de Saúde</a>
  <a href="../seguro-auto.html">Seguro Auto</a>
  <a href="../seguro-residencial.html">Seguro Residencial</a>
  <a href="../seguro-empresarial.html">Seguro Empresarial</a>
  <a href="index.html">Blog</a>
  <a href="../sobre.html">Sobre</a>
  <a href="../contato.html">Contato</a>
  <a href="https://wa.me/{WA}?text=Ol%C3%A1!%20Gostaria%20de%20fazer%20uma%20cota%C3%A7%C3%A3o."
     class="btn btn-green" target="_blank" rel="noopener">Cotar no WhatsApp</a>
</div>

<div class="breadcrumb-bar">
  <div class="container">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../index.html">Home</a>
      <span class="breadcrumb-sep">›</span>
      <a href="index.html">Blog</a>
      <span class="breadcrumb-sep">›</span>
      <span class="breadcrumb-curr">{cat_label}</span>
    </nav>
  </div>
</div>

<div class="main-wrap">
  <div class="container">
    <div class="page-layout">

      <article>
        <span class="label {cat_class}">{cat_label}</span>
        <h1 style="font-family:'DM Serif Display',serif;font-size:clamp(1.8rem,3.5vw,2.7rem);line-height:1.1;letter-spacing:-.5px;margin:16px 0 20px">{titulo_h1}</h1>
        <div class="post-meta">
          <span>📅 {data_pub}</span>
          <span>✍️ Start Corretora</span>
          <span class="reading-time">⏱️ Calculando...</span>
        </div>
        <div style="border-radius:var(--r-lg);overflow:hidden;margin:22px 0;width:100%;height:280px;background:var(--bg2);display:flex;align-items:center;justify-content:center">
          <img src="../assets/images/logo-start-corretora.png" alt="{imagem_alt}" style="max-width:280px;max-height:200px;object-fit:contain;display:block">
        </div>

        <div class="post-body">
          {corpo}

          {faq_html}

          <div class="share-bar">
            <span>Compartilhar:</span>
            <a class="share-btn share-btn-wa" href="{share_wa}" target="_blank" rel="noopener">📱 WhatsApp</a>
            <a class="share-btn" href="{share_fb}" target="_blank" rel="noopener">Facebook</a>
            <a class="share-btn" href="{share_tw}" target="_blank" rel="noopener">Twitter</a>
          </div>
        </div>
      </article>

      <aside class="sidebar">
        <div class="s-card s-card-cta">
          <h4>📲 Cotação Grátis</h4>
          <p>Fale com um especialista e receba as melhores propostas em minutos.</p>
          <a href="https://wa.me/{WA}?text={wa_msg}" class="btn btn-green" target="_blank" rel="noopener">Falar no WhatsApp</a>
        </div>
        <div class="s-card">
          <h4>📚 Posts Relacionados</h4>
          <div class="related-list">
            {rel_html}
          </div>
        </div>
        <div class="s-card">
          <h4>🌎 Atendemos Todo o Brasil</h4>
          <p>Sede no Andaraí, Rio de Janeiro. Atendimento remoto para todo o território nacional, com foco em RJ e SP.</p>
        </div>
      </aside>

    </div>
  </div>
</div>

<section class="cta-sec">
  <div class="container">
    <div class="cta-body">
      <div class="eyebrow">Cotação Gratuita</div>
      <h2 class="cta-title">Pronto para <em>proteger</em> o que importa?</h2>
      <p class="cta-desc">Fale com nossa equipe e receba as melhores propostas sem compromisso.</p>
      <div class="cta-btns">
        <a href="https://wa.me/{WA}?text={wa_msg}"
           class="btn btn-green btn-lg" target="_blank" rel="noopener">
          {WA_BTN_SVG}
          Falar no WhatsApp
        </a>
        <a href="../contato.html" class="btn btn-outline btn-lg">Enviar mensagem</a>
      </div>
      <div class="trust-row">
        <div class="trust-item">✓ Sem compromisso</div>
        <div class="trust-item">✓ Atendimento humanizado</div>
        <div class="trust-item">✓ 100% remoto</div>
      </div>
    </div>
  </div>
</section>

<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <img src="../assets/images/logo-start-corretora.png" alt="Start Corretora de Seguros" style="height:48px;width:auto;margin-bottom:16px">
        <p class="f-desc">Corretora independente especializada em seguros e planos de saúde. Atendemos pessoas físicas e jurídicas em todo o Brasil.</p>
        <div class="f-contact">
          <div class="f-contact-item">
            <svg class="f-contact-ico" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            <span>Rua Gastão Penalva, 15 — Andaraí, Rio de Janeiro/RJ</span>
          </div>
          <div class="f-contact-item">
            <svg class="f-contact-ico" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 13.5 19.79 19.79 0 0 1 1.61 4.9 2 2 0 0 1 3.59 2.69h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 9.49a16 16 0 0 0 6 6l.91-.91a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 21.5 17l.42-.08z"/></svg>
            <a href="https://wa.me/{WA}" style="color:var(--primary)">(21) 99999-2002</a>
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
          <li><a href="../seguro-de-vida.html">Seguro de Vida</a></li>
          <li><a href="../plano-de-saude.html">Plano de Saúde</a></li>
          <li><a href="../seguro-auto.html">Seguro Auto</a></li>
          <li><a href="../seguro-residencial.html">Seguro Residencial</a></li>
          <li><a href="../seguro-empresarial.html">Seguro Empresarial</a></li>
        </ul>
      </div>
      <div>
        <div class="f-col-head">Regiões</div>
        <ul class="f-links">
          <li><a href="../seguro-rio-de-janeiro.html">Rio de Janeiro</a></li>
          <li><a href="../seguro-sao-paulo.html">São Paulo</a></li>
          <li><a href="../index.html">Todo o Brasil</a></li>
        </ul>
      </div>
      <div>
        <div class="f-col-head">Empresa</div>
        <ul class="f-links">
          <li><a href="../sobre.html">Sobre a Start</a></li>
          <li><a href="index.html">Blog</a></li>
          <li><a href="../contato.html">Contato</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p class="f-copy">© {TODAY.year} Start Corretora de Seguros LTDA. Todos os direitos reservados.</p>
      <p class="f-copy">SUSEP · Todos os seguros são regulamentados pela SUSEP.</p>
    </div>
  </div>
</footer>

<a href="https://wa.me/{WA}?text=Ol%C3%A1!%20Vim%20pelo%20site%20e%20gostaria%20de%20uma%20cota%C3%A7%C3%A3o."
   class="wa-float" target="_blank" rel="noopener" aria-label="WhatsApp">
  {WA_ICON_SVG}
</a>

<script>
  const nav = document.getElementById('mainNav');
  window.addEventListener('scroll', () => {{
    nav.classList.toggle('scrolled', window.scrollY > 16);
  }}, {{ passive: true }});
  document.getElementById('burger').addEventListener('click', () => {{
    document.getElementById('mobileMenu').classList.toggle('open');
  }});
  document.querySelectorAll('#mobileMenu a').forEach(a => {{
    a.addEventListener('click', () => document.getElementById('mobileMenu').classList.remove('open'));
  }});
  const postBody = document.querySelector('.post-body');
  const rt = document.querySelector('.reading-time');
  if (postBody && rt) {{
    const words = postBody.innerText.trim().split(/\\s+/).length;
    rt.textContent = '⏱️ ' + Math.ceil(words / 200) + ' min de leitura';
  }}
</script>
</body>
</html>"""

    return html


# ─── Main ────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Gera artigo SEO para o blog da Start Corretora",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Exemplos:
  python scripts/gerar_conteudo.py "seguro de vida para autônomo"
  python scripts/gerar_conteudo.py "plano de saúde individual" --categoria saude
  python scripts/gerar_conteudo.py "seguro auto rj" --sem-serp --slug seguro-auto-rj-guia-completo
  python scripts/gerar_conteudo.py "corretora de seguros sp" --output blog/""",
    )
    parser.add_argument("keyword",     help="Palavra-chave alvo do artigo")
    parser.add_argument("--slug",      help="Slug personalizado (padrão: gerado da keyword)")
    parser.add_argument(
        "--categoria",
        choices=list(CATEGORIAS.keys()),
        default=None,
        help="Categoria (detectada automaticamente se omitida)",
    )
    parser.add_argument(
        "--sem-serp",
        action="store_true",
        help="Pula análise de SERP — usa apenas conhecimento do modelo (mais rápido)",
    )
    parser.add_argument(
        "--output",
        default=str(BLOG_DIR),
        help=f"Diretório de saída (padrão: {BLOG_DIR})",
    )
    args = parser.parse_args()

    # Verifica API key (suporta OAuth token via ANTHROPIC_AUTH_TOKEN)
    auth_token = os.getenv("ANTHROPIC_AUTH_TOKEN")
    api_key    = os.getenv("ANTHROPIC_API_KEY")
    if not auth_token and not api_key:
        print("❌  ANTHROPIC_API_KEY ou ANTHROPIC_AUTH_TOKEN não encontrado.")
        print("    Crie o arquivo .env na raiz do projeto com:")
        print("    ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)

    if auth_token:
        client = anthropic.Anthropic(auth_token=auth_token)
    else:
        client = anthropic.Anthropic(api_key=api_key)
    keyword  = args.keyword.strip()

    print(f"\n{'='*60}")
    print(f"  GERADOR DE CONTEÚDO SEO — START CORRETORA")
    print(f"{'='*60}")
    print(f"  Keyword: «{keyword}»")
    print(f"  Modelo:  {MODELO_CONTEUDO}")
    print(f"  SERP:    {'desativada (--sem-serp)' if args.sem_serp else 'ativada (web search)'}")
    print(f"{'--'*30}\n")

    # Fase 1 — SERP
    if args.sem_serp:
        print("⏭️   Pulando análise SERP")
        serp = serp_defaults(keyword)
    else:
        serp = analisar_serp(keyword, client)

    # Fase 2 — Conteúdo
    conteudo = gerar_conteudo(keyword, serp, client)

    # Força categoria se passada via CLI
    if args.categoria:
        conteudo["categoria"] = args.categoria

    # Slug final
    slug = args.slug or conteudo.get("slug") or slugify(keyword)

    # Fase 3 — HTML
    print(f"🏗️   Montando HTML...")
    html = montar_html(keyword, slug, conteudo, serp)

    # Salvar arquivo
    output_dir  = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{slug}.html"
    output_path.write_text(html, encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"  ✅  ARTIGO GERADO COM SUCESSO")
    print(f"{'--'*30}")
    print(f"  Arquivo : {output_path}")
    print(f"  URL     : {DOMAIN}/blog/{slug}")
    print(f"  H1      : {conteudo.get('titulo_h1', '')}")
    print(f"  Meta    : {conteudo.get('meta_description', '')[:70]}...")
    print(f"  Categoria: {conteudo.get('categoria', 'geral')}")
    print(f"{'='*60}\n")
    print("📌 Próximos passos:")
    print("   1. Revise e ajuste o conteúdo gerado")
    print("   2. Adicione uma imagem de capa em assets/images/")
    print("   3. Atualize blog/index.html com o novo post")
    print("   4. Atualize sitemap.xml")
    print("   5. Publique (git add · git commit · git push)\n")


if __name__ == "__main__":
    main()