# BRIEFING — Start Corretora de Seguros | Site Completo

Construa o site completo da Start Corretora de Seguros do zero, em HTML/CSS/JS estático, pronto para subir no servidor. Crie todos os arquivos e pastas descritos abaixo.

---

## 1. DADOS DO CLIENTE

- **Empresa:** Start Corretora de Seguros LTDA
- **CNPJ:** 48.385.999/0001-69
- **Endereço:** Rua Gastão Penalva, nº 15, Bloco 1, Apto. 215 — Andaraí, Rio de Janeiro/RJ — CEP 20540-220
- **WhatsApp:** (21) 99999-2002
- **Link WhatsApp:** `https://wa.me/5521999992002?text=Olá!%20Vim%20pelo%20site%20e%20gostaria%20de%20fazer%20uma%20cotação%20de%20seguro.`
- **Serviços:** Seguro Auto, Seguro de Vida, Plano de Saúde, Seguro Residencial, Seguro Empresarial
- **Atuação:** Todo o Brasil, foco inicial em Rio de Janeiro e São Paulo

---

## 2. IDENTIDADE VISUAL

### Cores (CSS variables)
```css
--primary: #00e676;
--primary-dark: #00b359;
--primary-glow: rgba(0, 230, 118, 0.15);
--bg: #0a0a0a;
--bg2: #111111;
--bg3: #1a1a1a;
--bg4: #222222;
--text: #ffffff;
--text-muted: #999999;
--border: #2a2a2a;
```

### Fontes
Google Fonts: `Barlow Condensed` (800 — títulos) + `Barlow` (400/500 — corpo)

### Logo
Arquivo: `assets/images/logo.png` — use em todas as páginas.
Abaixo do logo, sempre o subtítulo: **CORRETORA DE SEGUROS** (fonte display, letra espaçada, cor --text-muted)

### Tom
Profissional, direto, moderno. Linguagem acessível. NUNCA use Lorem Ipsum.

### Layout
Portal de notícias/blog estilo dark: hero grande + sidebar + grid de cards. Ticker de notícias animado no topo da home.

---

## 3. ESTRUTURA DE ARQUIVOS

```
/
├── index.html
├── sobre.html
├── contato.html
├── seguro-de-vida.html
├── plano-de-saude.html
├── seguro-auto.html
├── seguro-residencial.html
├── seguro-empresarial.html
├── seguro-rio-de-janeiro.html
├── seguro-sao-paulo.html
├── sitemap.xml
├── robots.txt
├── assets/
│   ├── css/style.css
│   ├── js/main.js
│   └── images/logo.png
├── blog/
│   ├── index.html
│   ├── seguro-de-vida-por-que-investir-hoje.html
│   ├── quem-recebe-seguro-de-vida-falecido.html
│   ├── quantas-pessoas-seguro-de-vida.html
│   ├── quanto-custa-seguro-de-vida-500mil.html
│   ├── beneficios-do-seguro-de-vida.html
│   ├── doenca-grave-seguro-de-vida.html
│   ├── seguro-auto-rj.html
│   └── plano-de-saude-sp.html
└── admin/
    ├── index.html
    ├── posts.html
    ├── novo-post.html
    ├── agendamento.html
    ├── palavras-chave.html
    └── gsc.html
```

---

## 4. COMPONENTES GLOBAIS (em todas as páginas)

### Header
- Logo centralizado no topo
- Nav escura: Home | Seguro de Vida | Plano de Saúde | Seguro Auto | Para Empresas | Residencial | Blog | Contato
- Botão verde "📲 Cotação Grátis" no canto direito — link WhatsApp
- Menu hamburguer no mobile

### Footer
- Grid 4 colunas: logo + NAP completo | Seguros | Regiões | Empresa
- NAP idêntico em todas as páginas: nome, endereço, CEP, telefone, CNPJ
- Nota "SUSEP · Todos os seguros são regulamentados pela SUSEP"
- Copyright 2025

### WhatsApp Float
- Botão fixo bottom-right, circular, cor #25d366
- Ícone SVG oficial do WhatsApp
- Animação pulse CSS suave
- Link WhatsApp com mensagem pré-definida

### Schema NAP (em todas as páginas)
```json
{
  "@type": "InsuranceAgency",
  "name": "Start Corretora de Seguros LTDA",
  "telephone": "+55-21-99999-2002",
  "address": {
    "streetAddress": "Rua Gastão Penalva, nº 15, Bloco 1, Apto. 215",
    "addressLocality": "Rio de Janeiro",
    "addressRegion": "RJ",
    "postalCode": "20540-220",
    "addressCountry": "BR"
  }
}
```

---

## 5. REGRAS SEO (obrigatórias em todas as páginas)

- Title tag com palavra-chave principal
- Meta description 150-160 caracteres
- `meta robots: index, follow` (exceto /admin/ → noindex, nofollow)
- Canonical URL
- OG tags: title, description, image, url, type
- 1x H1, H2 para seções, H3 para subseções
- Schema markup específico por tipo de página (ver abaixo)
- Breadcrumbs com BreadcrumbList em páginas internas
- Lazy loading em todas as imagens

---

## 6. HOME (index.html)

**Title:** `Corretora de Seguros no Rio de Janeiro e São Paulo | Start Corretora`
**Meta description:** `Start Corretora de Seguros: seguro auto, vida, saúde, residencial e empresarial no Rio de Janeiro e São Paulo. Cotação rápida, atendimento humanizado e as melhores seguradoras do Brasil.`
**Schema:** InsuranceAgency completo

### Seções na ordem:
1. Header
2. Ticker animado com títulos dos posts mais recentes
3. Hero grid (2 colunas):
   - Esquerda: post destaque grande com imagem de fundo, overlay escuro, categoria, título em verde, data
   - Direita: 2 posts menores empilhados + card CTA WhatsApp verde
4. Strip de serviços: 5 cards (Auto, Vida, Saúde, Residencial, Empresarial) com ícone emoji, nome e descrição de 1 linha
5. Seção "Últimos Artigos": grid 3 colunas, 6 cards com thumbnail, categoria, título, excerpt, "Ler →"
6. Banner CTA: fundo escuro com brilho verde, título "Faça sua Cotação Grátis Agora", botão WhatsApp + botão "Enviar Mensagem"
7. Footer

---

## 7. PÁGINAS DE SERVIÇO

Criar: `seguro-de-vida.html`, `plano-de-saude.html`, `seguro-auto.html`, `seguro-residencial.html`, `seguro-empresarial.html`

Cada uma deve ter (conteúdo real, mínimo 600 palavras):
- H1 com palavra-chave + "no Rio de Janeiro e São Paulo"
- Seção "O que é [serviço]" — 150 palavras
- Seção "Para quem é indicado" — lista com ícones
- Seção "O que está incluído na cobertura" — cards ou lista
- Seção "Como funciona" — passo a passo numerado (4 etapas)
- FAQ com 4 perguntas reais + schema FAQPage
- CTA com botão WhatsApp + formulário simplificado (nome, telefone, select do serviço)
- Schema: Service com provider (InsuranceAgency) e areaServed

**Titles sugeridos:**
- Seguro de Vida: "Seguro de Vida no Rio de Janeiro e São Paulo | Start Corretora"
- Plano de Saúde: "Plano de Saúde RJ e SP: cotação gratuita | Start Corretora"
- Seguro Auto: "Seguro Auto no Rio de Janeiro e São Paulo | Start Corretora"
- Residencial: "Seguro Residencial RJ e SP: proteja seu lar | Start Corretora"
- Empresarial: "Seguro Empresarial para PME no RJ e SP | Start Corretora"

---

## 8. PÁGINAS REGIONAIS

Criar: `seguro-rio-de-janeiro.html` e `seguro-sao-paulo.html`

Cada uma deve ter:
- H1: "Corretora de Seguros no [Cidade]: cotação rápida e atendimento especializado"
- Parágrafo sobre o mercado de seguros na cidade (real, 200 palavras)
- Grid com todos os 5 serviços disponíveis na região
- Seção "Por que contratar uma corretora em [cidade]?"
- CTA + formulário
- Schema: LocalBusiness com areaServed = cidade

---

## 9. BLOG

### blog/index.html
- H1: "Blog Start Corretora: Guias e Dicas sobre Seguros"
- Filtros por categoria (botões): Todos | Seguro de Vida | Plano de Saúde | Seguro Auto | Empresarial | Rio de Janeiro | São Paulo
- Grid 3 colunas com cards: thumbnail, categoria badge, título, excerpt 2 linhas, data, "Ler →"
- Filtros funcionando via JS (mostrar/ocultar cards por data-categoria)

### Post individual (template para todos os posts)
Layout 2 colunas (70/30):
- **Coluna principal:** breadcrumb → categoria badge → H1 → meta (data + autor + tempo leitura) → imagem hero → conteúdo → barra de compartilhamento (WhatsApp, Facebook, Twitter)
- **Sidebar:** card CTA WhatsApp | Posts relacionados (3) | Card "Atendemos todo o Brasil"
- Tempo de leitura calculado em JS (palavras / 200)
- Schema Article com headline, author, datePublished, dateModified, image

### Posts a criar com conteúdo completo (800+ palavras cada, real e útil):

**1. seguro-de-vida-por-que-investir-hoje.html**
- Title: "Seguro de Vida: Por Que Investir Hoje Pode Garantir o Futuro da Sua Família"
- Tópicos: o que é, para quem é, coberturas (morte, invalidez, doenças graves, funeral), quanto custa por faixa de idade, como escolher, por que usar corretora
- Data: 2025-09-03

**2. quem-recebe-seguro-de-vida-falecido.html**
- Title: "Quem Recebe o Seguro de Vida do Falecido? Entenda as Regras e a Ordem de Recebimento"
- Tópicos: beneficiários designados, o que acontece sem designação, ordem legal, como acionar, prazo para recebimento
- Data: 2026-02-12

**3. quantas-pessoas-seguro-de-vida.html**
- Title: "Quantas Pessoas Posso Colocar no Seguro de Vida? Entenda as Regras e Limitações"
- Tópicos: número máximo de beneficiários, como dividir percentuais, dependentes x terceiros, como atualizar beneficiários
- Data: 2026-01-20

**4. quanto-custa-seguro-de-vida-500mil.html**
- Title: "Quanto Custa um Seguro de Vida de 500 Mil? Descubra Quanto Você Realmente Pagaria"
- Tópicos: fatores que influenciam (idade, saúde, profissão), tabela simulada por faixa etária, coberturas inclusas, custo-benefício
- Data: 2026-01-15

**5. beneficios-do-seguro-de-vida.html**
- Title: "Quais os Benefícios do Seguro de Vida: Proteção, Tranquilidade e Segurança para o Futuro"
- Tópicos: proteção financeira, cobertura de invalidez, assistência funeral, doenças graves, paz de espírito, deduções no IR
- Data: 2025-12-10

**6. doenca-grave-seguro-de-vida.html**
- Title: "O que é Considerado Doença Grave para Seguro de Vida"
- Tópicos: lista das principais doenças cobertas (câncer, AVC, infarto, transplantes), como funciona o acionamento, carência, diferença entre planos
- Data: 2025-11-05

**7. seguro-auto-rj.html**
- Title: "Seguro Auto no Rio de Janeiro: Como Escolher a Cobertura Certa para o Seu Perfil"
- Tópicos: índices de roubo no RJ, tipos de cobertura (básica, compreensiva, total), franquia, assistência 24h, carro reserva, dicas para baratear
- Data: 2026-01-08

**8. plano-de-saude-sp.html**
- Title: "Plano de Saúde em São Paulo: Como Contratar Sem Pagar Caro"
- Tópicos: individual vs coletivo vs empresarial, principais operadoras em SP, rede credenciada, carência, o que a ANS garante, como comparar
- Data: 2026-01-02

---

## 10. SOBRE (sobre.html)

- Title: "Quem Somos | Start Corretora de Seguros – Rio de Janeiro"
- Layout: hero com título + texto + imagem | Cards de valores (3) | Números (anos, parceiros, cobertura) | CTA
- Conteúdo: missão, visão, valores, diferencial (atendimento humanizado, sem robôs, transparência total)

---

## 11. CONTATO (contato.html)

- Title: "Contato e Cotação Gratuita | Start Corretora – (21) 99999-2002"
- Layout 2 colunas: formulário (esquerda) + informações de contato (direita)
- Formulário: nome*, telefone/WhatsApp*, email, tipo de seguro (select), estado, mensagem, botão "Enviar Cotação"
- Coluna direita: card WhatsApp (destaque), telefone, endereço, horário, área de atuação
- Embed Google Maps: Andaraí, Rio de Janeiro
- Schema ContactPage + InsuranceAgency
- Formulário com validação JS e mensagem de sucesso

---

## 12. ADMIN (visual idêntico ao site — mesmo CSS)

### admin/index.html — Dashboard
- Sidebar fixa (240px): logo + nav com ícones
- Nav: Dashboard | Ver Site | Posts | Novo Post | Calendário | Palavras-chave | Search Console
- Cards métricas: Total Posts | Publicados | Agendados | Palavras-chave
- Gráfico barras (Chart.js CDN): publicações por mês
- Tabela últimos posts com status badges
- Lista próximas publicações

### admin/posts.html
- Tabela: thumbnail miniatura | título | categoria | status | data | ações
- Status badges: Publicado (verde) | Agendado (amarelo) | Rascunho (cinza)
- Filtros por status e categoria
- Botão "Novo Post" no topo

### admin/novo-post.html
- Editor Quill.js (CDN)
- Campos: título, slug (auto-gerado do título), meta title (contador 60 chars, barra indicadora), meta description (contador 160 chars)
- Palavra-chave foco
- Categoria (select) + tags
- Upload imagem destacada com preview
- Preview snippet Google em tempo real (como aparece no resultado de busca)
- Status: Rascunho | Agendar (mostra campo data/hora) | Publicar agora
- Botões: Salvar Rascunho | Publicar/Agendar
- Dados salvos em localStorage

### admin/agendamento.html
- Calendário mensal navegável (JS puro)
- Posts agendados marcados nos dias com ponto verde
- Clique no dia: modal para criar novo post agendado
- Lista lateral "Próximas publicações" ordenada por data

### admin/palavras-chave.html
Tabela filtrável com as 22 palavras-chave abaixo:

| # | Palavra-chave | Intenção | Prioridade | Sugestão de título | Status |
|---|---|---|---|---|---|
| 1 | corretora de seguros rio de janeiro | Transacional | Alta | Corretora de Seguros no Rio de Janeiro: cotação rápida e atendimento humanizado | Pendente |
| 2 | corretora de seguros são paulo | Transacional | Alta | Corretora de Seguros em São Paulo: compare e contrate online | Pendente |
| 3 | seguro de vida rio de janeiro | Local | Alta | Seguro de Vida no Rio de Janeiro: como contratar e quanto custa | Pendente |
| 4 | seguro auto rj | Local | Alta | Seguro Auto no RJ: cotação, coberturas e as melhores seguradoras | Em produção |
| 5 | seguro de vida vale a pena | Informacional | Alta | Seguro de Vida Vale a Pena? Análise honesta para você decidir | Publicado |
| 6 | quanto custa seguro de vida | Informacional | Alta | Quanto Custa um Seguro de Vida em 2025? Simulação completa | Publicado |
| 7 | plano de saúde são paulo | Local | Alta | Plano de Saúde em São Paulo: como encontrar o melhor custo-benefício | Em produção |
| 8 | seguro empresarial para pequenas empresas | Transacional | Alta | Seguro Empresarial para PME: o que sua empresa precisa ter coberto | Pendente |
| 9 | quem recebe seguro de vida falecido | Informacional | Média | Quem Recebe o Seguro de Vida do Falecido? Regras e ordem | Publicado |
| 10 | o que é franquia no seguro auto | Informacional | Média | O que é Franquia no Seguro Auto e como ela afeta seu bolso | Pendente |
| 11 | seguro residencial vale a pena | Informacional | Média | Seguro Residencial: por que contratar e o que ele cobre | Pendente |
| 12 | diferença plano saúde individual e coletivo | Informacional | Média | Plano de Saúde Individual vs Coletivo: qual é o melhor para você? | Pendente |
| 13 | cotação seguro de vida online | Transacional | Média | Cotação de Seguro de Vida Online: como funciona e o que comparar | Pendente |
| 14 | seguro de vida zona sul rio de janeiro | Local | Média | Seguro de Vida na Zona Sul do Rio: cotação e atendimento especializado | Pendente |
| 15 | plano de saúde zona norte sp | Local | Média | Plano de Saúde na Zona Norte de São Paulo: opções e preços | Pendente |
| 16 | seguro auto roubado o que fazer | Informacional | Média | Carro Roubado e Tenho Seguro: o que fazer passo a passo | Pendente |
| 17 | doença grave seguro de vida | Informacional | Baixa | O que é Considerado Doença Grave no Seguro de Vida? | Publicado |
| 18 | seguro de vida para autônomo | Informacional | Baixa | Seguro de Vida para Autônomos e MEI: por que é ainda mais importante | Pendente |
| 19 | como acionar seguro de vida | Informacional | Baixa | Como Acionar o Seguro de Vida: passo a passo completo | Pendente |
| 20 | seguro residencial incêndio cobertura | Informacional | Baixa | Seguro Residencial Cobre Incêndio? Veja tudo sobre coberturas | Pendente |
| 21 | seguro saúde para empresa pequena | Transacional | Alta | Plano de Saúde para Pequenas Empresas: como contratar a partir de 2 vidas | Pendente |
| 22 | benefícios seguro de vida | Informacional | Média | Quais os Benefícios do Seguro de Vida: proteção, tranquilidade e segurança | Publicado |

Filtros por intenção (Transacional / Informacional / Local) e prioridade (Alta / Média / Baixa).
Status com dots coloridos: cinza = Pendente, amarelo = Em produção, azul = Publicado, verde = Posicionado.
Botão "Criar Post" nos pendentes.

### admin/gsc.html
- Instruções passo a passo para verificar o site no Google Search Console
- Campo para colar a meta tag de verificação
- Gráficos simulados (Chart.js): cliques, impressões, CTR, posição média nos últimos 28 dias
- Instrução para enviar sitemap: `https://startcorretoradeseguros.com.br/sitemap.xml`

---

## 13. SITEMAP.XML

Incluir todas as URLs com `changefreq` e `priority`:
- Home: priority 1.0, weekly
- Páginas de serviço: priority 0.9, monthly
- Páginas regionais: priority 0.85, monthly
- Contato e Sobre: priority 0.8, monthly
- Blog index: priority 0.8, weekly
- Posts individuais: priority 0.7, monthly com lastmod

---

## 14. ROBOTS.TXT

```
User-agent: *
Allow: /
Disallow: /admin/

Sitemap: https://startcorretoradeseguros.com.br/sitemap.xml
```

---

## 15. CDNs PERMITIDOS

- Google Fonts
- Chart.js: `https://cdn.jsdelivr.net/npm/chart.js`
- Quill.js: `https://cdn.quilljs.com`
- Sem React, Vue ou outros frameworks

---

## 16. REGRAS FINAIS

- NUNCA use Lorem Ipsum — todo texto deve ser real e útil
- Todo conteúdo deve ser sobre seguros no Brasil (foco RJ e SP)
- Mobile-first e responsivo em 100% das páginas
- Lazy loading em todas as imagens (`loading="lazy"`)
- Admin usa localStorage para persistência dos dados
- Admin tem sidebar fixa com o mesmo visual do site
- Todos os links de WhatsApp devem usar a URL com mensagem pré-definida
- O NAP deve ser idêntico em todas as páginas do site
