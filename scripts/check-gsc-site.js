// Roda: node scripts/check-gsc-site.js
// Lista as propriedades do GSC visíveis pela service account
const fs = require('fs');
// Lê .env.local manualmente (sem depender de dotenv)
fs.readFileSync('.env.local', 'utf8').split('\n').forEach(line => {
  const [k, ...v] = line.split('=');
  if (k && v.length) process.env[k.trim()] = v.join('=').trim();
});
const { GoogleAuth } = require('google-auth-library');

async function main() {
  const raw = process.env.GOOGLE_SA_KEY;
  if (!raw) { console.error('GOOGLE_SA_KEY não encontrada em .env.local'); process.exit(1); }

  let credentials;
  try { credentials = JSON.parse(raw); }
  catch { credentials = JSON.parse(Buffer.from(raw, 'base64').toString('utf8')); }

  const auth = new GoogleAuth({ credentials, scopes: ['https://www.googleapis.com/auth/webmasters.readonly'] });
  const client = await auth.getClient();
  const res = await client.request({ url: 'https://www.googleapis.com/webmasters/v3/sites', method: 'GET' });

  const sites = res.data.siteEntry ?? [];
  if (sites.length === 0) {
    console.log('\n❌ Nenhuma propriedade encontrada para esta service account.');
    console.log('   Verifique se adicionou o e-mail no GSC com permissão.');
    return;
  }

  console.log('\n✅ Propriedades encontradas:\n');
  sites.forEach(s => console.log(`  siteUrl: "${s.siteUrl}"  |  nível: ${s.permissionLevel}`));
  console.log('\n→ Copie o siteUrl correto e use em api/search-console.js (linha 3)\n');
}

main().catch(err => {
  console.error('\n❌ Erro:', err.message);
  if (err.message.includes('401') || err.message.includes('403')) {
    console.error('   A API pode não estar ativada ou a service account não tem permissão.');
  }
});
