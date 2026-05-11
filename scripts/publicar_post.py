#!/usr/bin/env python3
"""
publicar_post.py — Registra um artigo gerado no blog/index.html e no sitemap.xml
Start Corretora de Seguros

Uso (logo após gerar_conteudo.py):
  python scripts/publicar_post.py \\
    --slug seguro-de-vida-para-autonomo \\
    --titulo "Seguro de Vida para Autônomo: Como Proteger Sua Renda" \\
    --descricao "Guia completo: coberturas, custos e como contratar seguro de vida sendo autônomo ou MEI." \\
    --categoria vida \\
    --emoji 💼
"""

import re
import sys
import argparse
from datetime import datetime
from pathlib import Path

BASE_DIR    = Path(__file__).parent.parent
BLOG_INDEX  = BASE_DIR / "blog" / "index.html"
SITEMAP     = BASE_DIR / "sitemap.xml"
DOMAIN      = "https://startcorretoradeseguros.com.br"
TODAY       = datetime.now()

CAT_MAP = {
    "vida":        ("label-vida",        "Seguro de Vida",    "seguro-de-vida"),
    "auto":        ("label-auto",        "Seguro Auto",       "seguro-auto"),
    "saude":       ("label-saude",       "Plano de Saúde",    "plano-de-saude"),
    "residencial": ("label-residencial", "Seguro Residencial","seguro-residencial"),
    "empresarial": ("label-empresarial", "Seguro Empresarial","seguro-empresarial"),
    "geral":       ("label-geral",       "Seguros",           "todos"),
}

MONTH_PT = {
    1:"jan", 2:"fev", 3:"mar", 4:"abr", 5:"mai", 6:"jun",
    7:"jul", 8:"ago", 9:"set", 10:"out", 11:"nov", 12:"dez",
}


def data_curta() -> str:
    return f"{TODAY.day:02d} {MONTH_PT[TODAY.month]} {TODAY.year}"


def data_iso() -> str:
    return TODAY.strftime("%Y-%m-%d")


def adicionar_ao_blog_index(slug: str, titulo: str, descricao: str,
                             categoria: str, emoji: str) -> bool:
    cat_class, cat_label, data_cat = CAT_MAP.get(categoria, CAT_MAP["geral"])

    card = f"""
    <article class="blog-card" data-cat="{data_cat}">
      <a href="{slug}.html">
        <div class="blog-card-thumb">{emoji}</div>
      </a>
      <div class="blog-card-body">
        <span class="label {cat_class}">{cat_label}</span>
        <h3><a href="{slug}.html">{titulo}</a></h3>
        <p>{descricao}</p>
        <div class="blog-card-footer">
          <span class="blog-card-date">{data_curta()}</span>
          <a href="{slug}.html" class="blog-card-read">Ler →</a>
        </div>
      </div>
    </article>
"""

    content = BLOG_INDEX.read_text(encoding="utf-8")

    # Verifica se o slug já existe
    if f'href="{slug}.html"' in content:
        print(f"  ⚠️  Slug «{slug}» já existe em blog/index.html — pulando.")
        return False

    # Insere o novo card logo após o marcador <!-- Grid -->
    anchor = "<!-- Grid -->\n  <div class=\"blog-grid\">"
    if anchor not in content:
        print("  ❌  Marcador '<!-- Grid -->' não encontrado em blog/index.html.")
        return False

    updated = content.replace(
        anchor,
        anchor + card,
        1,
    )
    BLOG_INDEX.write_text(updated, encoding="utf-8")
    return True


def adicionar_ao_sitemap(slug: str) -> bool:
    url = f"{DOMAIN}/blog/{slug}"
    content = SITEMAP.read_text(encoding="utf-8")

    if url in content:
        print(f"  ⚠️  URL já existe no sitemap.xml — pulando.")
        return False

    entry = f"""  <url>
    <loc>{url}</loc>
    <lastmod>{data_iso()}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
"""

    # Insere antes do fechamento </urlset>
    updated = content.replace("</urlset>", entry + "</urlset>")
    SITEMAP.write_text(updated, encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Registra novo artigo em blog/index.html e sitemap.xml"
    )
    parser.add_argument("--slug",      required=True, help="Slug do arquivo HTML (sem .html)")
    parser.add_argument("--titulo",    required=True, help="Título do artigo (H1)")
    parser.add_argument("--descricao", required=True, help="Resumo para o card do blog (1-2 frases)")
    parser.add_argument("--categoria", required=True, choices=list(CAT_MAP.keys()),
                        help="Categoria do artigo")
    parser.add_argument("--emoji",     default="📄", help="Emoji para o card (padrão: 📄)")
    args = parser.parse_args()

    # Verifica se o arquivo do artigo existe
    art_path = BASE_DIR / "blog" / f"{args.slug}.html"
    if not art_path.exists():
        print(f"⚠️  Arquivo não encontrado: {art_path}")
        print("   Execute gerar_conteudo.py primeiro.")

    print(f"\n📋 Publicando: «{args.slug}»")

    ok_blog = adicionar_ao_blog_index(
        args.slug, args.titulo, args.descricao, args.categoria, args.emoji
    )
    ok_sitemap = adicionar_ao_sitemap(args.slug)

    print()
    if ok_blog:
        print(f"  ✅  blog/index.html atualizado")
    if ok_sitemap:
        print(f"  ✅  sitemap.xml atualizado")

    print(f"\n📌 Próximos passos:")
    print(f"   git add blog/{args.slug}.html blog/index.html sitemap.xml")
    print(f"   git commit -m \"feat: artigo SEO — {args.titulo[:60]}\"")
    print(f"   git push\n")


if __name__ == "__main__":
    main()
