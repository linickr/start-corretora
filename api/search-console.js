const { GoogleAuth } = require('google-auth-library');

const SITE_URL = 'sc-domain:startcorretoradeseguros.com.br';
const SITE_ORIGIN = 'https://startcorretoradeseguros.com.br';
const SC_API = `https://www.googleapis.com/webmasters/v3/sites/${encodeURIComponent(SITE_URL)}/searchAnalytics/query`;

function buildAuth() {
  const raw = process.env.GOOGLE_SA_KEY;
  if (!raw) throw new Error('GOOGLE_SA_KEY não definida');
  let credentials;
  try { credentials = JSON.parse(raw); }
  catch { credentials = JSON.parse(Buffer.from(raw, 'base64').toString('utf8')); }
  return new GoogleAuth({ credentials, scopes: ['https://www.googleapis.com/auth/webmasters.readonly'] });
}

function dateStr(d) { return d.toISOString().split('T')[0]; }
function daysAgo(n) { const d = new Date(); d.setDate(d.getDate() - n); return d; }

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 's-maxage=3600, stale-while-revalidate=600');

  try {
    const auth = buildAuth();
    const client = await auth.getClient();

    const query = (body) =>
      client.request({ url: SC_API, method: 'POST', data: body }).then(r => r.data);

    const endDate      = dateStr(daysAgo(1));
    const startDate    = dateStr(daysAgo(28));
    const prevEndDate  = dateStr(daysAgo(29));
    const prevStartDate = dateStr(daysAgo(56));

    const [current, previous, daily, queries, pages] = await Promise.all([
      query({ startDate, endDate, searchType: 'web' }),
      query({ startDate: prevStartDate, endDate: prevEndDate, searchType: 'web' }),
      query({ startDate, endDate, searchType: 'web', dimensions: ['date'], rowLimit: 28 }),
      query({ startDate, endDate, searchType: 'web', dimensions: ['query'], rowLimit: 10 }),
      query({ startDate, endDate, searchType: 'web', dimensions: ['page'], rowLimit: 5 }),
    ]);

    const cur = current.rows?.[0] ?? {};
    const prev = previous.rows?.[0] ?? {};

    const cliquesTotais  = Math.round(cur.clicks ?? 0);
    const impressoes     = Math.round(cur.impressions ?? 0);
    const ctrMedio       = parseFloat(((cur.ctr ?? 0) * 100).toFixed(2));
    const posicaoMedia   = parseFloat((cur.position ?? 0).toFixed(1));

    const prevCliques    = Math.round(prev.clicks ?? 0);
    const prevImpressoes = Math.round(prev.impressions ?? 0);
    const prevCtr        = parseFloat(((prev.ctr ?? 0) * 100).toFixed(2));
    const prevPosicao    = parseFloat((prev.position ?? 0).toFixed(1));

    const pct = (a, b) => b === 0 ? 0 : parseFloat(((a - b) / b * 100).toFixed(1));

    const deltaCliques    = pct(cliquesTotais, prevCliques);
    const deltaImpressoes = pct(impressoes, prevImpressoes);
    const deltaCtr        = parseFloat((ctrMedio - prevCtr).toFixed(2));     // pp
    const deltaPosicao    = parseFloat((prevPosicao - posicaoMedia).toFixed(1)); // + = melhorou

    const dailyRows = (daily.rows ?? []).sort((a, b) => a.keys[0].localeCompare(b.keys[0]));

    const labels = dailyRows.map(r => {
      const [, mm, dd] = r.keys[0].split('-');
      return `${dd}/${mm}`;
    });

    const serie = {
      clicks:      dailyRows.map(r => Math.round(r.clicks ?? 0)),
      impressions: dailyRows.map(r => Math.round(r.impressions ?? 0)),
      ctr:         dailyRows.map(r => parseFloat(((r.ctr ?? 0) * 100).toFixed(2))),
      position:    dailyRows.map(r => parseFloat((r.position ?? 0).toFixed(1))),
    };

    const keywords = (queries.rows ?? []).map(r => ({
      term:        r.keys[0],
      pos:         parseFloat((r.position ?? 0).toFixed(1)),
      clicks:      Math.round(r.clicks ?? 0),
      impressions: Math.round(r.impressions ?? 0),
      ctr:         parseFloat(((r.ctr ?? 0) * 100).toFixed(1)),
    }));

    const topPages = (pages.rows ?? []).map(r => ({
      page:   r.keys[0].replace(SITE_ORIGIN, '') || '/',
      clicks: Math.round(r.clicks ?? 0),
    }));

    return res.status(200).json({
      cliquesTotais, impressoes, ctrMedio, posicaoMedia,
      deltaCliques, deltaImpressoes, deltaCtr, deltaPosicao,
      labels, serie, keywords, pages: topPages,
    });

  } catch (err) {
    console.error('[search-console]', err.message);
    return res.status(500).json({ error: err.message });
  }
};
