from pathlib import Path

root = Path(__file__).resolve().parent.parent / 'local'


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


def redirect_html(new_url: str) -> str:
    return f"""<!DOCTYPE html>
<html lang=\"pt-BR\">
<head>
  <meta charset=\"UTF-8\">
  <meta http-equiv=\"refresh\" content=\"0;url={new_url}\">
  <link rel=\"canonical\" href=\"{new_url}\" />
  <title>Redirecionando...</title>
</head>
<body>
  <p>Redirecionando para <a href=\"{new_url}\">{new_url}</a>.</p>
</body>
</html>
"""


def update_page_urls(page_path: Path, old_url: str, new_url: str):
    text = page_path.read_text(encoding='utf-8')
    if old_url in text:
        text = text.replace(old_url, new_url)
        page_path.write_text(text, encoding='utf-8')


def list_category_items(category: str) -> list[str]:
    category_dir = root / category
    return sorted([p.name for p in category_dir.iterdir() if p.is_dir()])


def rename_and_redirect(category: str):
    category_dir = root / category
    items = list_category_items(category)
    mapping = {item: f'corretora-de-seguros-{slug(item)}' for item in items}

    for old_slug, new_slug in mapping.items():
        old_dir = category_dir / old_slug
        new_dir = category_dir / new_slug
        if old_dir.exists() and not new_dir.exists():
            old_dir.rename(new_dir)

    for old_slug, new_slug in mapping.items():
        old_dir = category_dir / old_slug
        if not old_dir.exists():
            old_dir.mkdir(parents=True, exist_ok=True)
        redirect_url = f'/local/{category}/{new_slug}/'
        old_dir.joinpath('index.html').write_text(redirect_html(redirect_url), encoding='utf-8')

    index_path = category_dir / 'index.html'
    if index_path.exists():
        text = index_path.read_text(encoding='utf-8')
        for old_slug, new_slug in mapping.items():
            text = text.replace(f'/local/{category}/{old_slug}/', f'/local/{category}/{new_slug}/')
        index_path.write_text(text, encoding='utf-8')

    for old_slug, new_slug in mapping.items():
        page_path = category_dir / new_slug / 'index.html'
        if page_path.exists():
            update_page_urls(page_path,
                             f'https://startcorretoradeseguros.com.br/local/{category}/{old_slug}/',
                             f'https://startcorretoradeseguros.com.br/local/{category}/{new_slug}/')
            update_page_urls(page_path,
                             f'/local/{category}/{old_slug}/',
                             f'/local/{category}/{new_slug}/')

    return mapping


city_mapping = rename_and_redirect('cidades')
neighborhood_mapping = rename_and_redirect('bairros')

print('Updated city slugs:')
for old, new in city_mapping.items():
    print(f'{old} -> {new}')
print('Updated neighborhood slugs:')
for old, new in neighborhood_mapping.items():
    print(f'{old} -> {new}')
