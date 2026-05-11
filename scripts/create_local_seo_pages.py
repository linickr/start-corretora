from pathlib import Path

cities = [
    'São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Brasília', 'Salvador',
    'Fortaleza', 'Curitiba', 'Porto Alegre', 'Recife', 'Manaus',
    'Belém', 'Goiânia', 'Campinas', 'Vitória', 'Florianópolis',
    'Ribeirão Preto', 'Santos', 'Niterói', 'São Bernardo do Campo', 'Santo André'
]

neighborhoods = [
    'Copacabana', 'Ipanema', 'Barra da Tijuca', 'Leblon', 'Botafogo',
    'Tijuca', 'Barra Funda', 'Moema', 'Pinheiros', 'Vila Madalena',
    'Jardins', 'Itaim Bibi', 'Brooklin', 'Vila Olímpia', 'Santana',
    'Perdizes', 'Bexiga', 'Lapa', 'Centro SP', 'Centro RJ'
]

root = Path(__file__).resolve().parent.parent / 'local'
root.mkdir(parents=True, exist_ok=True)


def slug(text: str) -> str:
    replacements = {
        'ã': 'a', 'á': 'a', 'â': 'a', 'à': 'a',
        'é': 'e', 'ê': 'e', 'í': 'i', 'ó': 'o',
        'ô': 'o', 'õ': 'o', 'ú': 'u', 'ç': 'c',
        'Ã': 'a', 'Á': 'a', 'Â': 'a', 'À': 'a',
        'É': 'e', 'Ê': 'e', 'Í': 'i', 'Ó': 'o',
        'Ô': 'o', 'Õ': 'o', 'Ú': 'u', 'Ç': 'c'
    }
    s = text
    for orig, repl in replacements.items():
        s = s.replace(orig, repl)
    s = s.replace(' ', '-').replace('/', '-').replace('.', '').replace('(', '').replace(')', '')
    s = ''.join(ch for ch in s if ch.isalnum() or ch == '-')
    while '--' in s:
        s = s.replace('--', '-')
    return s.strip('-')

page_template = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Corretora de Seguros em {location} | Start Corretora de Seguros</title>
  <meta name="description" content="Corretora de seguros em {location}. Atendimento local, cotação personalizada e suporte especializado para sua cidade ou bairro.">
  <meta name="keywords" content="corretora de seguros, corretora de seguros {location}, seguro em {location}">
  <link rel="canonical" href="https://startcorretoradeseguros.com.br/local/{category}/{slug}/">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://startcorretoradeseguros.com.br/local/{category}/{slug}/">
  <meta property="og:title" content="Corretora de Seguros em {location} | Start Corretora">
  <meta property="og:description" content="Corretora de seguros em {location}. Atendimento local, cotação personalizada e suporte especializado.">
  <meta property="og:image" content="https://startcorretoradeseguros.com.br/assets/images/logo.png">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'Barlow', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
    header {{ background: white; padding: 20px 0; border-bottom: 1px solid #ddd; }}
    .container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; }}
    nav {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }}
    nav a {{ text-decoration: none; color: #333; margin: 0 12px; font-weight: 500; }}
    nav a:hover {{ color: #00e676; }}
    .services {{ display: flex; gap: 16px; flex-wrap: wrap; }}
    .services a {{ text-decoration: none; color: #666; font-size: 14px; }}
    .services a:hover {{ color: #00e676; }}
    main {{ padding: 60px 0; }}
    h1 {{ font-size: 2.4rem; margin-bottom: 20px; color: #1a5f7a; }}
    p {{ margin-bottom: 15px; line-height: 1.8; }}
    .cta-box {{ background: linear-gradient(135deg, #1a5f7a 0%, #2980b9 100%); color: white; padding: 30px; border-radius: 8px; text-align: center; margin: 40px 0; }}
    .cta-box a {{ display: inline-block; background: #00e676; color: #333; padding: 15px 40px; border-radius: 4px; text-decoration: none; font-weight: 600; margin-top: 15px; }}
    .cta-box a:hover {{ background: #00b359; }}
    footer {{ background: #333; color: white; padding: 30px 0; margin-top: 60px; text-align: center; }}
    .breadcrumb {{ margin-bottom: 20px; font-size: 14px; }}
    .breadcrumb a {{ color: #00e676; text-decoration: none; }}
    .breadcrumb a:hover {{ text-decoration: underline; }}
    .section-nav {{ background: white; padding: 20px; border-radius: 8px; margin: 30px 0; }}
    .section-nav h3 {{ margin-bottom: 15px; }}
    .section-nav ul {{ list-style: none; }}
    .section-nav li {{ margin: 8px 0; }}
    .section-nav a {{ color: #00e676; text-decoration: none; }}
    .section-nav a:hover {{ text-decoration: underline; }}
    .local-links {{ background: #fff; padding: 18px; border-radius: 8px; margin-top: 30px; }}
    .local-links ul {{ list-style: none; display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; }}
    .local-links li {{ margin: 0; }}
    .local-links a {{ color: #1a5f7a; text-decoration: none; }}
    .local-links a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
<header>
  <div class="container">
    <nav>
      <a href="/" style="font-weight: 700; font-size: 18px;">🏠 Start Corretora</a>
      <div class="services">
        <a href="/">Home</a>
        <a href="/local/">SEO Local</a>
        <a href="/local/cidades/">Cidades</a>
        <a href="/local/bairros/">Bairros</a>
        <a href="/blog/">Blog</a>
      </div>
    </nav>
  </div>
</header>
<main>
  <div class="container">
    <div class="breadcrumb">
      <a href="/">Home</a> > <a href="/local/">SEO Local</a> > <strong>{location}</strong>
    </div>
    <h1>Corretora de Seguros em {location}</h1>
    <p>Encontre a melhor corretora de seguros em {location}. Atendimento local, cotação rápida e propostas adaptadas à sua necessidade.</p>
    <div class="section-nav">
      <h3>📑 Conteúdo desta página:</h3>
      <ul>
        <li><a href="#introducao">Introdução</a></li>
        <li><a href="#porque-contratar">Por que contratar</a></li>
        <li><a href="#como-contratar">Como contratar</a></li>
        <li><a href="#faq">Perguntas Frequentes</a></li>
      </ul>
    </div>
    <section id="introducao">
      <h2>Introdução</h2>
      <p><strong>[Conteúdo a ser preenchido]</strong></p>
      <p>Descreva os principais benefícios de utilizar uma corretora de seguros em {location} para proteger seu carro, casa, vida ou empresa.</p>
    </section>
    <section id="porque-contratar">
      <h2>Por que contratar uma corretora de seguros em {location}?</h2>
      <p><strong>[Conteúdo a ser preenchido]</strong></p>
      <ul>
        <li>Atendimento local e conhecimento da região</li>
        <li>Propostas personalizadas para {location}</li>
        <li>Suporte em caso de sinistro</li>
      </ul>
    </section>
    <section id="como-contratar">
      <h2>Como contratar</h2>
      <p><strong>[Conteúdo a ser preenchido]</strong></p>
      <p>Explique os passos para solicitar cotação, comparar planos e fechar a melhor apólice em {location}.</p>
    </section>
    <section id="faq">
      <h2>Perguntas Frequentes</h2>
      <p><strong>[Conteúdo a ser preenchido]</strong></p>
    </section>
    <div class="cta-box">
      <h2>Solicite uma cotação local</h2>
      <p>Fale com nossa equipe e receba a melhor proposta para {location}.</p>
      <a href="https://wa.me/5521999992002?text=Olá!%20Gostaria%20de%20cotar%20uma%20apólice%20de%20seguro%20para%20{location}">Cotar em {location}</a>
    </div>
    <div class="local-links">
      <h2>Mais SEO Local</h2>
      <ul>
        <li><a href="/local/cidades/">Todas as cidades</a></li>
        <li><a href="/local/bairros/">Todos os bairros</a></li>
        <li><a href="/local/">Página principal de SEO local</a></li>
      </ul>
    </div>
  </div>
</main>
<footer>
  <div class="container">
    <p>&copy; 2026 Start Corretora de Seguros. Todos os direitos reservados.</p>
  </div>
</footer>
</body>
</html>'''

index_template = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SEO Local de Corretora de Seguros | Start Corretora</title>
  <meta name="description" content="Páginas de SEO local para corretora de seguros nas principais cidades e bairros do Brasil.">
  <link rel="canonical" href="https://startcorretoradeseguros.com.br/local/">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://startcorretoradeseguros.com.br/local/">
  <meta property="og:title" content="SEO Local de Corretora de Seguros | Start Corretora">
  <meta property="og:description" content="Páginas de SEO local para corretora de seguros nas principais cidades e bairros do Brasil.">
  <meta property="og:image" content="https://startcorretoradeseguros.com.br/assets/images/logo.png">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'Barlow', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
    header {{ background: white; padding: 20px 0; border-bottom: 1px solid #ddd; }}
    .container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; }}
    nav {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }}
    nav a {{ text-decoration: none; color: #333; margin: 0 12px; font-weight: 500; }}
    nav a:hover {{ color: #00e676; }}
    .services {{ display: flex; gap: 16px; flex-wrap: wrap; }}
    .services a {{ text-decoration: none; color: #666; font-size: 14px; }}
    .services a:hover {{ color: #00e676; }}
    main {{ padding: 60px 0; }}
    h1 {{ font-size: 2.5rem; margin-bottom: 20px; color: #1a5f7a; }}
    p {{ margin-bottom: 15px; line-height: 1.8; }}
    .grid {{ display: grid; gap: 24px; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); margin-top: 30px; }}
    .card {{ background: white; padding: 20px; border-radius: 12px; border: 1px solid #e5e5e5; }}
    .card h2 {{ margin-bottom: 12px; color: #1a5f7a; font-size: 1.1rem; }}
    .card a {{ color: #00e676; text-decoration: none; }}
    .card a:hover {{ text-decoration: underline; }}
    footer {{ background: #333; color: white; padding: 30px 0; margin-top: 60px; text-align: center; }}
  </style>
</head>
<body>
<header>
  <div class="container">
    <nav>
      <a href="/" style="font-weight: 700; font-size: 18px;">🏠 Start Corretora</a>
      <div class="services">
        <a href="/">Home</a>
        <a href="/local/">SEO Local</a>
        <a href="/local/cidades/">Cidades</a>
        <a href="/local/bairros/">Bairros</a>
        <a href="/blog/">Blog</a>
      </div>
    </nav>
  </div>
</header>
<main>
  <div class="container">
    <h1>SEO Local: Corretora de Seguros no Brasil</h1>
    <p>Fortaleça sua presença online com páginas otimizadas para corretora de seguros nas principais cidades e bairros do Brasil.</p>
    <div class="grid">
      <div class="card">
        <h2>Cidades</h2>
        <p>Páginas locais para as principais cidades do Brasil.</p>
        <a href="/local/cidades/">Ver cidades</a>
      </div>
      <div class="card">
        <h2>Bairros</h2>
        <p>Segmentação local para bairros com alta demanda.</p>
        <a href="/local/bairros/">Ver bairros</a>
      </div>
    </div>
  </div>
</main>
<footer>
  <div class="container">
    <p>&copy; 2026 Start Corretora de Seguros. Todos os direitos reservados.</p>
  </div>
</footer>
</body>
</html>'''

category_template = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | SEO Local | Start Corretora</title>
  <meta name="description" content="Páginas de SEO local para corretora de seguros em {title}. Confira as URLs criadas para cidades e bairros.">
  <link rel="canonical" href="https://startcorretoradeseguros.com.br/local/{category}/">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://startcorretoradeseguros.com.br/local/{category}/">
  <meta property="og:title" content="{title} | SEO Local | Start Corretora">
  <meta property="og:description" content="Páginas de SEO local para corretora de seguros em {title}. Confira as URLs criadas para cidades e bairros.">
  <meta property="og:image" content="https://startcorretoradeseguros.com.br/assets/images/logo.png">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'Barlow', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; }}
    header {{ background: white; padding: 20px 0; border-bottom: 1px solid #ddd; }}
    .container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; }}
    nav {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }}
    nav a {{ text-decoration: none; color: #333; margin: 0 12px; font-weight: 500; }}
    nav a:hover {{ color: #00e676; }}
    .services {{ display: flex; gap: 16px; flex-wrap: wrap; }}
    .services a {{ text-decoration: none; color: #666; font-size: 14px; }}
    .services a:hover {{ color: #00e676; }}
    main {{ padding: 60px 0; }}
    h1 {{ font-size: 2.5rem; margin-bottom: 20px; color: #1a5f7a; }}
    p {{ margin-bottom: 15px; line-height: 1.8; }}
    .grid {{ display: grid; gap: 16px; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); margin-top: 30px; }}
    .card {{ background: white; padding: 20px; border-radius: 12px; border: 1px solid #e5e5e5; }}
    .card h2 {{ margin-bottom: 12px; color: #1a5f7a; font-size: 1.1rem; }}
    .card a {{ color: #00e676; text-decoration: none; }}
    .card a:hover {{ text-decoration: underline; }}
    footer {{ background: #333; color: white; padding: 30px 0; margin-top: 60px; text-align: center; }}
  </style>
</head>
<body>
<header>
  <div class="container">
    <nav>
      <a href="/" style="font-weight: 700; font-size: 18px;">🏠 Start Corretora</a>
      <div class="services">
        <a href="/">Home</a>
        <a href="/local/">SEO Local</a>
        <a href="/local/cidades/">Cidades</a>
        <a href="/local/bairros/">Bairros</a>
        <a href="/blog/">Blog</a>
      </div>
    </nav>
  </div>
</header>
<main>
  <div class="container">
    <h1>{title}</h1>
    <p>Confira as páginas de SEO local criadas para {title}.</p>
    <div class="grid">
      {links}
    </div>
  </div>
</main>
<footer>
  <div class="container">
    <p>&copy; 2026 Start Corretora de Seguros. Todos os direitos reservados.</p>
  </div>
</footer>
</body>
</html>'''

for category, items in [('cidades', cities), ('bairros', neighborhoods)]:
    category_dir = root / category
    category_dir.mkdir(parents=True, exist_ok=True)
    cards = []
    for item in items:
        item_slug = slug(item)
        page_dir = category_dir / item_slug
        page_dir.mkdir(parents=True, exist_ok=True)
        page_path = page_dir / 'index.html'
        page_path.write_text(page_template.format(location=item, category=category, slug=item_slug), encoding='utf-8')
        cards.append(f'<div class="card"><h2>{item}</h2><a href="/local/{category}/{item_slug}/">Ver página</a></div>')
    category_index = category_dir / 'index.html'
    category_index.write_text(category_template.format(title=category.capitalize(), category=category, links='\n      '.join(cards)), encoding='utf-8')

root_index = root / 'index.html'
root_index.write_text(index_template, encoding='utf-8')
print(f'Created {len(cities) + len(neighborhoods)} SEO local pages in {root}')
