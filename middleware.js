export const config = {
  matcher: ['/((?!_vercel|api|assets).*)'],
}

const INJECT = [
  '<link rel="icon" type="image/png" href="/assets/images/favicon.png">',
  '<link rel="stylesheet" href="/assets/css/noturno.css">',
].join('\n  ')

export default async function middleware(request) {
  const response = await fetch(request)
  const contentType = response.headers.get('content-type') ?? ''

  if (!contentType.includes('text/html')) return response

  const html = await response.text()

  if (html.includes('noturno.css')) {
    return new Response(html, response)
  }

  const patched = html.includes('</head>')
    ? html.replace('</head>', `  ${INJECT}\n</head>`)
    : `<head>\n  ${INJECT}\n</head>\n` + html

  const headers = new Headers(response.headers)
  headers.set('content-type', 'text/html; charset=utf-8')
  return new Response(patched, { status: response.status, headers })
}
