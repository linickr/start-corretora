const { BetaAnalyticsDataClient } = require('@google-analytics/data');

const rawId = process.env.GA4_PROPERTY_ID ?? '';
const GA_PROPERTY_ID = rawId.startsWith('properties/') ? rawId : `properties/${rawId}`;

const PERIODS = {
  '7d':   { startDate: '7daysAgo',   chartDim: 'date' },
  '14d':  { startDate: '14daysAgo',  chartDim: 'date' },
  '30d':  { startDate: '30daysAgo',  chartDim: 'date' },
  '90d':  { startDate: '90daysAgo',  chartDim: 'yearMonth' },
  '180d': { startDate: '180daysAgo', chartDim: 'yearMonth' },
  '365d': { startDate: '365daysAgo', chartDim: 'yearMonth' },
};

const MONTHS = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'];

function buildClient() {
  const raw = process.env.GOOGLE_SA_KEY;
  if (!raw) throw new Error('GOOGLE_SA_KEY não definida');
  let credentials;
  try { credentials = JSON.parse(raw); }
  catch { credentials = JSON.parse(Buffer.from(raw, 'base64').toString('utf8')); }
  return new BetaAnalyticsDataClient({ credentials });
}

function formatLabel(value, dim) {
  if (dim === 'yearMonth') {
    // YYYYMM
    const year = value.slice(2, 4);
    const month = parseInt(value.slice(4, 6), 10) - 1;
    return `${MONTHS[month]}/${year}`;
  }
  // date: YYYYMMDD
  return `${value.slice(6, 8)}/${value.slice(4, 6)}`;
}

function intVal(row, idx) {
  return parseInt(row?.metricValues?.[idx]?.value ?? '0', 10);
}

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 's-maxage=1800, stale-while-revalidate=300');

  if (!rawId) {
    return res.status(500).json({ error: 'GA4_PROPERTY_ID não definida' });
  }

  const periodKey = PERIODS[req.query?.period] ? req.query.period : '30d';
  const { startDate, chartDim } = PERIODS[periodKey];

  try {
    const client = buildClient();

    const [
      [mainReport],
      [channelReport],
      [pagesReport],
      [chartReport],
    ] = await Promise.all([
      client.runReport({
        property: GA_PROPERTY_ID,
        dateRanges: [{ startDate, endDate: 'today' }],
        metrics: [
          { name: 'sessions' },
          { name: 'activeUsers' },
          { name: 'screenPageViews' },
          { name: 'conversions' },
        ],
      }),
      client.runReport({
        property: GA_PROPERTY_ID,
        dateRanges: [{ startDate, endDate: 'today' }],
        dimensions: [{ name: 'sessionDefaultChannelGroup' }],
        metrics: [{ name: 'sessions' }],
      }),
      client.runReport({
        property: GA_PROPERTY_ID,
        dateRanges: [{ startDate, endDate: 'today' }],
        dimensions: [{ name: 'pagePath' }],
        metrics: [{ name: 'screenPageViews' }],
        orderBys: [{ metric: { metricName: 'screenPageViews' }, desc: true }],
        limit: 5,
      }),
      client.runReport({
        property: GA_PROPERTY_ID,
        dateRanges: [{ startDate, endDate: 'today' }],
        dimensions: [{ name: chartDim }],
        metrics: [{ name: 'sessions' }],
        orderBys: [{ dimension: { dimensionName: chartDim } }],
      }),
    ]);

    const mainRow = mainReport.rows?.[0];
    const sessions    = intVal(mainRow, 0);
    const users       = intVal(mainRow, 1);
    const pageviews   = intVal(mainRow, 2);
    const conversions = intVal(mainRow, 3);

    let organicSessions = 0, paidSessions = 0;
    for (const row of channelReport.rows ?? []) {
      const channel = (row.dimensionValues?.[0]?.value ?? '').toLowerCase();
      const val = parseInt(row.metricValues?.[0]?.value ?? '0', 10);
      if (channel.includes('organic')) organicSessions += val;
      if (channel.includes('paid')) paidSessions += val;
    }

    const topPages = (pagesReport.rows ?? []).map(row => ({
      page: row.dimensionValues?.[0]?.value ?? '',
      views: parseInt(row.metricValues?.[0]?.value ?? '0', 10),
    }));

    const sessionsByPeriod = (chartReport.rows ?? []).map(row => ({
      label: formatLabel(row.dimensionValues?.[0]?.value ?? '', chartDim),
      sessions: parseInt(row.metricValues?.[0]?.value ?? '0', 10),
    }));

    return res.status(200).json({
      sessions, users, pageviews, conversions,
      organicSessions, paidSessions,
      topPages,
      sessionsByPeriod,
      period: periodKey,
    });
  } catch (err) {
    console.error('[analytics] Erro GA4:', err.message, err.stack);
    return res.status(500).json({ error: err.message, details: err.errors ?? null });
  }
};
