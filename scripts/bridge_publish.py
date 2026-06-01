#!/usr/bin/env python3
"""
bridge_publish.py — Publica conteúdo pré-gerado sem chamar a API Claude.

Uso:
  python scripts/bridge_publish.py blog   <content.json> [--slug SLUG] [--categoria CAT]
  python scripts/bridge_publish.py local  <content.json> --localizacao LOC --uf UF --cidade CID --preposicao PREP --slug SLUG
"""

import sys
import json
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(Path(__file__).parent))


def publish_blog(content_file: str, slug_override: str = None, categoria_override: str = None):
    from gerar_conteudo import montar_html, slugify, BLOG_DIR
    from datetime import datetime

    with open(content_file, encoding="utf-8") as f:
        conteudo = json.load(f)

    if categoria_override:
        conteudo["categoria"] = categoria_override

    keyword = conteudo.get("titulo_h1", "seguro")
    slug = slug_override or conteudo.get("slug") or slugify(keyword)
    serp = {}

    print(f"🏗️  Montando HTML para blog/{slug}.html ...")
    html = montar_html(keyword, slug, conteudo, serp)

    BLOG_DIR.mkdir(parents=True, exist_ok=True)
    output_path = BLOG_DIR / f"{slug}.html"
    output_path.write_text(html, encoding="utf-8")

    print(f"✅  Arquivo salvo: {output_path}")
    print(f"   H1      : {conteudo.get('titulo_h1', '')}")
    print(f"   Slug    : {slug}")
    print(f"   Categ.  : {conteudo.get('categoria', 'geral')}")
    return slug, conteudo


def publish_local(content_file: str, localizacao: str, uf: str, cidade: str,
                  preposicao: str, slug: str, tipo: str = "bairro"):
    from gerar_pagina_local import montar_html_local

    with open(content_file, encoding="utf-8") as f:
        conteudo = json.load(f)

    print(f"🏗️  Montando HTML local para /{slug}/index.html ...")
    html = montar_html_local(localizacao, slug, preposicao, uf, cidade, conteudo)

    out_dir = BASE_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / "index.html"
    output_path.write_text(html, encoding="utf-8")

    print(f"✅  Arquivo salvo: {output_path}")
    print(f"   Localização: {localizacao}/{uf}")
    print(f"   Slug       : {slug}")
    return slug, conteudo


def main():
    parser = argparse.ArgumentParser(description="Publica conteúdo pré-gerado")
    sub = parser.add_subparsers(dest="cmd")

    p_blog = sub.add_parser("blog")
    p_blog.add_argument("content_file")
    p_blog.add_argument("--slug")
    p_blog.add_argument("--categoria")

    p_local = sub.add_parser("local")
    p_local.add_argument("content_file")
    p_local.add_argument("--localizacao", required=True)
    p_local.add_argument("--uf", required=True)
    p_local.add_argument("--cidade", required=True)
    p_local.add_argument("--preposicao", required=True)
    p_local.add_argument("--slug", required=True)
    p_local.add_argument("--tipo", default="bairro")

    args = parser.parse_args()

    if args.cmd == "blog":
        publish_blog(args.content_file, args.slug, args.categoria)
    elif args.cmd == "local":
        publish_local(args.content_file, args.localizacao, args.uf, args.cidade,
                      args.preposicao, args.slug, args.tipo)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
