const { BetaAnalyticsDataClient } = require('@google-analytics/data');

// Aceita "505846361" ou "properties/505846361"
const rawId = process.env.GA4_PROPERTY_ID ?? '';
const GA_PROPERTY_ID = rawId.startsWith('properties/') ? rawId : `properties/${rawId}`;

function buildClient() {
  const raw = process.env.GOOGLE_SA_KEY;
  if (!raw) throw new Error('GOOGLE_SA_KEY não definida');

  // Aceita JSON puro ou base64
  let credentials;
  try {
    credentials = JSON.parse(raw);
  } catch {
    credentials = JSON.parse(Buffer.from(raw, 'base64').toString('utf8'));
  }

  return new BetaAnalyticsDataClient({ credentials });
}

function yearMonthLabel(ym) {
  // ym = "YYYYMM"
  const months = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'];
  const year = ym.slice(2, 4);
  const month = parseInt(ym.slice(4, 6), 10) - 1;
  return `${months[month]}/${year}`;
}

function intVal(row, idx) {
  return parseInt(row?.metricValues?.[idx]?.value ?? '0', 10);
}

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 's-maxage=3600, stale-while-revalidate=600');

  if (!rawId) {
    return res.status(500).json({ error: 'GA4_PROPERTY_ID não definida' });
  }

  try {
    const client = buildClient();

    // Executa 4 relatórios em paralelo
    const [
      [mainReport],
      [channelReport],
      [pagesReport],
      [monthlyReport],
    ] = await Promise.all([
      // 1. Métricas agregadas — últimos 30 dias
      client.runReport({
        property: GA_PROPERTY_ID,
        dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
        metrics: [
          { name: 'sessions' },
          { name: 'activeUsers' },
          { name: 'screenPageViews' },
          { name: 'conversions' },
        ],
      }),

      // 2. Sessões por canal (orgânico / pago)
      client.runReport({
        property: GA_PROPERTY_ID,
        dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
        dimensions: [{ name: 'sessionDefaultChannelGroup' }],
        metrics: [{ name: 'sessions' }],
      }),

      // 3. Top 5 páginas por pageviews
      client.runReport({
        property: GA_PROPERTY_ID,
        dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
        dimensions: [{ name: 'pagePath' }],
        metrics: [{ name: 'screenPageViews' }],
        orderBys: [{ metric: { metricName: 'screenPageViews' }, desc: true }],
        limit: 5,
      }),

      // 4. Sessões por mês — últimos ~6 meses
      client.runReport({
        property: GA_PROPERTY_ID,
        dateRanges: [{ startDate: '180daysAgo', endDate: 'today' }],
        dimensions: [{ name: 'yearMonth' }],
        metrics: [{ name: 'sessions' }],
        orderBys: [{ dimension: { dimensionName: 'yearMonth' } }],
      }),
    ]);

    // --- Métricas principais ---
    const mainRow = mainReport.rows?.[0];
    const sessions   = intVal(mainRow, 0);
    const users      = intVal(mainRow, 1);
    const pageviews  = intVal(mainRow, 2);
    const conversions = intVal(mainRow, 3);

    // --- Orgânico / Pago ---
    let organicSessions = 0;
    let paidSessions = 0;
    for (const row of channelReport.rows ?? []) {
      const channel = (row.dimensionValues?.[0]?.value ?? '').toLowerCase();
      const val = parseInt(row.metricValues?.[0]?.value ?? '0', 10);
      if (channel.includes('organic')) organicSessions += val;
      if (channel.includes('paid') || channel === 'paid search' || channel === 'paid social') {
        paidSessions += val;
      }
    }

    // --- Top páginas ---
    const topPages = (pagesReport.rows ?? []).map(row => ({
      page: row.dimensionValues?.[0]?.value ?? '',
      views: parseInt(row.metricValues?.[0]?.value ?? '0', 10),
    }));

    // --- Sessões por mês (últimos 6) ---
    const sessionsByMonth = (monthlyReport.rows ?? [])
      .slice(-6)
      .map(row => ({
        month: yearMonthLabel(row.dimensionValues?.[0]?.value ?? ''),
        sessions: parseInt(row.metricValues?.[0]?.value ?? '0', 10),
      }));

    return res.status(200).json({
      sessions,
      users,
      pageviews,
      conversions,
      organicSessions,
      paidSessions,
      topPages,
      sessionsByMonth,
    });
  } catch (err) {
    console.error('[analytics] Erro GA4:', err.message);
    return res.status(500).json({ error: err.message });
  }
};
