#!/usr/bin/env python3
"""
daily_content.py — Orquestrador Diário de Conteúdo SEO
Start Corretora de Seguros

Executa automaticamente todo dia:
  1. Gera 1 artigo de blog (via gerar_conteudo.py + publicar_post.py)
  2. Gera 1 página de SEO local (via gerar_pagina_local.py)
  3. Faz git commit + push para o GitHub
  4. Registra o resultado no log do planejamento

Uso:
  python scripts/daily_content.py
  python scripts/daily_content.py --apenas-blog
  python scripts/daily_content.py --apenas-local
  python scripts/daily_content.py --sem-serp        (pula análise de SERP, mais rápido)
  python scripts/daily_content.py --sem-push        (não faz git push)
  python scripts/daily_content.py --dry-run         (simula sem gerar nada)

Requer:
  ANTHROPIC_API_KEY no arquivo .env na raiz do projeto
  git configurado com remote origin (GitHub)
"""

import os
import sys
import re
import json
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
except ImportError:
    pass

# ─── Constantes ───────────────────────────────────────────────────────────────
BASE_DIR     = Path(__file__).parent.parent
PLAN_FILE    = BASE_DIR / "scripts" / "planejamento-palavras-chave.json"
BLOG_DIR     = BASE_DIR / "blog"
SCRIPTS_DIR  = BASE_DIR / "scripts"
DOMAIN       = "https://startcorretoradeseguros.com.br"
TODAY        = datetime.now()
TODAY_ISO    = TODAY.strftime("%Y-%m-%d")

PRIORIDADE_ORDEM = {"alta": 0, "media": 1, "baixa": 2}

EMOJI_CATEGORIA = {
    "vida":        "❤️",
    "auto":        "🚗",
    "saude":       "🏥",
    "residencial": "🏠",
    "empresarial": "🏢",
    "geral":       "📋",
}


# ─── Fila ─────────────────────────────────────────────────────────────────────
def carregar_plano() -> dict:
    if not PLAN_FILE.exists():
        print(f"❌  Arquivo de planejamento não encontrado: {PLAN_FILE}")
        sys.exit(1)
    with open(PLAN_FILE, encoding="utf-8") as f:
        return json.load(f)


def salvar_plano(plano: dict):
    with open(PLAN_FILE, "w", encoding="utf-8") as f:
        json.dump(plano, f, ensure_ascii=False, indent=2)


def proximo_pendente(fila: list) -> dict | None:
    pendentes = [item for item in fila if item.get("status") == "pendente"]
    if not pendentes:
        return None
    return sorted(pendentes, key=lambda x: PRIORIDADE_ORDEM.get(x.get("prioridade", "baixa"), 2))[0]


# ─── Execução de Scripts ───────────────────────────────────────────────────────
def run(cmd: list, cwd=None, timeout=600) -> tuple[int, str, str]:
    """Executa um comando e retorna (returncode, stdout, stderr)."""
    result = subprocess.run(
        cmd,
        cwd=cwd or BASE_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


def extrair_do_output(stdout: str, campo: str) -> str:
    """Extrai um valor de linha formatada como '  Campo : valor'."""
    for line in stdout.splitlines():
        if campo.lower() in line.lower() and ":" in line:
            return line.split(":", 1)[1].strip()
    return ""


# ─── Geração de Blog ──────────────────────────────────────────────────────────
def gerar_artigo_blog(item: dict, sem_serp: bool, dry_run: bool) -> dict | None:
    keyword   = item["keyword"]
    categoria = item.get("categoria", "geral")
    emoji     = EMOJI_CATEGORIA.get(categoria, "📄")

    print(f"\n{'─'*60}")
    print(f"📝  BLOG: «{keyword}» [{categoria}]")
    print(f"{'─'*60}")

    if dry_run:
        print("  [dry-run] Pulando geração de artigo.")
        return {"slug": "dry-run-blog", "titulo": "Dry Run", "categoria": categoria}

    # Fase 1: gerar_conteudo.py
    cmd_gerar = [sys.executable, str(SCRIPTS_DIR / "gerar_conteudo.py"), keyword, "--categoria", categoria]
    if sem_serp:
        cmd_gerar.append("--sem-serp")

    print(f"  🔄  Executando gerar_conteudo.py...")
    code, stdout, stderr = run(cmd_gerar, timeout=600)

    if code != 0:
        print(f"  ❌  Falha ao gerar artigo (código {code})")
        print(f"  STDERR: {stderr[:300]}")
        return None

    print(stdout)

    # Extrai slug e título do output
    slug   = extrair_do_output(stdout, "Arquivo")
    titulo = extrair_do_output(stdout, "H1")

    # Slug do path: blog/seguro-de-vida-para-autonomo.html → seguro-de-vida-para-autonomo
    if slug and "blog/" in slug:
        slug = Path(slug).stem  # remove .html
    elif slug:
        slug = Path(slug).stem

    if not slug or not titulo:
        # Fallback: tenta encontrar o arquivo mais recente em blog/
        blog_files = sorted(BLOG_DIR.glob("*.html"), key=lambda p: p.stat().st_mtime, reverse=True)
        if blog_files:
            slug = blog_files[0].stem

    if not slug:
        print("  ❌  Não foi possível determinar o slug do artigo gerado.")
        return None

    # Fase 2: publicar_post.py
    descricao = titulo[:100] if titulo else keyword[:100]
    cmd_pub = [
        sys.executable, str(SCRIPTS_DIR / "publicar_post.py"),
        "--slug",      slug,
        "--titulo",    titulo or keyword,
        "--descricao", descricao,
        "--categoria", categoria,
        "--emoji",     emoji,
    ]

    print(f"  🔄  Executando publicar_post.py...")
    code2, stdout2, stderr2 = run(cmd_pub, timeout=60)
    if code2 != 0:
        print(f"  ⚠️  publicar_post.py retornou código {code2}")
        print(f"  {stderr2[:200]}")
    else:
        print(stdout2)

    return {"slug": slug, "titulo": titulo, "categoria": categoria}


# ─── Geração de Página Local ──────────────────────────────────────────────────
def gerar_pagina_local(item: dict, sem_serp: bool, dry_run: bool) -> dict | None:
    localizacao = item["localizacao"]
    uf          = item["uf"]
    cidade      = item.get("cidade", "")
    tipo        = item.get("tipo", "bairro")
    preposicao  = item.get("preposicao", "em")
    slug        = item["slug"]

    print(f"\n{'─'*60}")
    print(f"📍  LOCAL: {localizacao}/{uf} → /{slug}/")
    print(f"{'─'*60}")

    if dry_run:
        print("  [dry-run] Pulando geração de página local.")
        return {"slug": slug, "localizacao": localizacao}

    cmd = [
        sys.executable, str(SCRIPTS_DIR / "gerar_pagina_local.py"),
        "--localizacao", localizacao,
        "--uf",          uf,
        "--tipo",        tipo,
        "--preposicao",  preposicao,
        "--slug",        slug,
    ]
    if cidade:
        cmd += ["--cidade", cidade]
    if sem_serp:
        cmd.append("--sem-serp")

    print(f"  🔄  Executando gerar_pagina_local.py...")
    code, stdout, stderr = run(cmd, timeout=600)

    if code != 0:
        print(f"  ❌  Falha na geração da página local (código {code})")
        print(f"  STDERR: {stderr[:300]}")
        return None

    print(stdout)
    return {"slug": slug, "localizacao": localizacao}


# ─── Git ──────────────────────────────────────────────────────────────────────
def git_commit_push(resultados: dict, dry_run: bool, sem_push: bool):
    blog_info  = resultados.get("blog")
    local_info = resultados.get("local")

    if not blog_info and not local_info:
        print("\n⚠️  Nada gerado — pulando commit.")
        return

    # Monta mensagem de commit
    partes = []
    if blog_info:
        partes.append(f"blog: {blog_info.get('titulo', blog_info['slug'])[:60]}")
    if local_info:
        partes.append(f"local: {local_info['localizacao']}")

    msg = f"feat: conteúdo SEO diário {TODAY_ISO} — " + " + ".join(partes)

    print(f"\n{'─'*60}")
    print(f"🚀  GIT: {msg}")
    print(f"{'─'*60}")

    if dry_run:
        print("  [dry-run] Pulando git commit/push.")
        return

    # Monta lista de arquivos para adicionar
    files_to_add = []

    if blog_info:
        blog_slug = blog_info["slug"]
        blog_html = BLOG_DIR / f"{blog_slug}.html"
        if blog_html.exists():
            files_to_add.append(str(blog_html.relative_to(BASE_DIR)))
        blog_index = BLOG_DIR / "index.html"
        if blog_index.exists():
            files_to_add.append(str(blog_index.relative_to(BASE_DIR)))

    if local_info:
        local_dir = BASE_DIR / local_info["slug"]
        if local_dir.exists():
            files_to_add.append(str(local_dir.relative_to(BASE_DIR)))

    # sitemap.xml sempre
    files_to_add.append("sitemap.xml")

    # git add
    code, out, err = run(["git", "add"] + files_to_add)
    if code != 0:
        print(f"  ⚠️  git add falhou: {err[:200]}")
        # Tenta git add -A como fallback
        code, out, err = run(["git", "add", "-A"])

    # git commit
    code, out, err = run(["git", "commit", "-m", msg, "--no-gpg-sign"])
    if code != 0:
        if "nothing to commit" in out + err:
            print("  ⚠️  Nada novo para commitar.")
            return
        print(f"  ❌  git commit falhou: {err[:300]}")
        return

    print(f"  ✅  Commit realizado")
    print(f"  {out.strip()[:100]}")

    if sem_push:
        print("  ⏭️  Push ignorado (--sem-push).")
        return

    # git push
    code, out, err = run(["git", "push", "origin", "main"], timeout=120)
    if code != 0:
        print(f"  ❌  git push falhou: {err[:300]}")
        print("      Verifique suas credenciais ou rode manualmente: git push origin main")
    else:
        print(f"  ✅  Push concluído para origin/main")


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Orquestrador diário de conteúdo SEO da Start Corretora"
    )
    parser.add_argument("--apenas-blog",  action="store_true", help="Gera apenas artigo de blog")
    parser.add_argument("--apenas-local", action="store_true", help="Gera apenas página local")
    parser.add_argument("--sem-serp",     action="store_true", help="Pula análise de SERP em todos os geradores")
    parser.add_argument("--sem-push",     action="store_true", help="Commit sem push para o GitHub")
    parser.add_argument("--dry-run",      action="store_true", help="Simula sem gerar nada")
    args = parser.parse_args()

    api_key    = os.getenv("ANTHROPIC_API_KEY")
    auth_token = os.getenv("ANTHROPIC_AUTH_TOKEN")
    if not api_key and not auth_token and not args.dry_run:
        print("❌  ANTHROPIC_API_KEY ou ANTHROPIC_AUTH_TOKEN não encontrado.")
        print("    Crie o arquivo .env na raiz do projeto com:")
        print("    ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)

    print(f"\n{'═'*60}")
    print(f"  ORQUESTRADOR DE CONTEÚDO — {TODAY_ISO}")
    print(f"{'═'*60}")

    plano      = carregar_plano()
    resultados = {"date": TODAY_ISO, "blog": None, "local": None, "erros": []}

    # ── Blog ──────────────────────────────────────────────────────────────────
    if not args.apenas_local:
        blog_item = proximo_pendente(plano["blog_queue"])

        if not blog_item:
            print("\n⚠️  Fila de blog vazia — todos os artigos foram gerados!")
        else:
            print(f"\n  Próximo blog     : #{blog_item['id']} «{blog_item['keyword']}» [{blog_item['prioridade']}]")
            result = gerar_artigo_blog(blog_item, args.sem_serp, args.dry_run)
            if result:
                blog_item["status"]    = "publicado"
                blog_item["slug"]      = result["slug"]
                blog_item["titulo"]    = result["titulo"]
                blog_item["gerado_em"] = TODAY_ISO
                resultados["blog"]     = result
                salvar_plano(plano)
            else:
                resultados["erros"].append(f"blog:{blog_item['keyword']}")

    # ── Local ─────────────────────────────────────────────────────────────────
    if not args.apenas_blog:
        local_item = proximo_pendente(plano["local_queue"])

        if not local_item:
            print("\n⚠️  Fila de páginas locais vazia — todas as páginas foram geradas!")
        else:
            print(f"\n  Próxima local    : #{local_item['id']} {local_item['localizacao']}/{local_item['uf']} [{local_item['prioridade']}]")
            result = gerar_pagina_local(local_item, args.sem_serp, args.dry_run)
            if result:
                local_item["status"]    = "publicado"
                local_item["gerado_em"] = TODAY_ISO
                resultados["local"]     = result
                salvar_plano(plano)
            else:
                resultados["erros"].append(f"local:{local_item['localizacao']}")

    # ── Git ────────────────────────────────────────────────────────────────────
    git_commit_push(resultados, args.dry_run, args.sem_push)

    # ── Log ────────────────────────────────────────────────────────────────────
    plano["schedule_log"].append(resultados)
    salvar_plano(plano)

    # ── Resumo ─────────────────────────────────────────────────────────────────
    pendentes_blog  = len([x for x in plano["blog_queue"]  if x["status"] == "pendente"])
    pendentes_local = len([x for x in plano["local_queue"] if x["status"] == "pendente"])

    print(f"\n{'═'*60}")
    print(f"  RESUMO — {TODAY_ISO}")
    print(f"{'─'*60}")
    if resultados["blog"]:
        print(f"  ✅  Blog  : /blog/{resultados['blog']['slug']}")
    else:
        print(f"  ⏭️  Blog  : pulado ou com erro")
    if resultados["local"]:
        print(f"  ✅  Local : /{resultados['local']['slug']}/")
    else:
        print(f"  ⏭️  Local : pulado ou com erro")
    if resultados["erros"]:
        print(f"  ❌  Erros : {', '.join(resultados['erros'])}")
    print(f"{'─'*60}")
    print(f"  Fila restante  : {pendentes_blog} artigos de blog · {pendentes_local} páginas locais")
    print(f"{'═'*60}\n")


if __name__ == "__main__":
    main()
