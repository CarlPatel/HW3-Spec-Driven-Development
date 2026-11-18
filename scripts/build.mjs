import {mkdir, cp, rm, writeFile, readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const manifest = JSON.parse(await readFile('versions/v1/checksums.json', 'utf8'));
for (const [file, expected] of Object.entries(manifest.files)) {
  const actual = createHash('sha256').update(await readFile(`versions/v1/frontend/${file}`)).digest('hex');
  if (actual !== expected) throw new Error(`Frozen V1 changed: ${file}`);
}
await rm('dist', {recursive: true, force: true});
await mkdir('dist', {recursive: true});
await cp('versions/v1/frontend', 'dist/v1', {recursive: true});
await cp('frontend', 'dist/v2', {recursive: true});
await writeFile('dist/.nojekyll', '');
await writeFile('dist/index.html', `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Pressroom · Prototype versions</title>
<style>body{font:16px system-ui;color:#19332d;background:#f4f6f2;max-width:800px;padding:48px 24px;margin:auto}h1{font-size:36px}a{display:block;padding:24px;margin:20px 0;border:1px solid #b8c9bf;border-radius:10px;background:white;color:#1e5948;text-decoration:none}b{font-size:22px}small{display:block;margin-top:10px;line-height:1.6}p{line-height:1.6}</style></head>
<body><p>PRESSROOM / MAINTENANCE PROTOTYPES</p><h1>Compare V1 and V2</h1><p>Each version uses independent mock records and resets on reload.</p>
<a href="./v1/"><b>Prototype V1</b><small>Frozen baseline bef8e6c · original downtime, handover and verification rules</small></a>
<a href="./v2/"><b>Prototype V2</b><small>Complete isolation evidence · separate stop intervals · explicit handover · recorded operating-shift verification</small></a>
<p>Demo only. No physical safety control, authentication or live sensors.</p></body></html>`);
console.log('Built comparison site: dist/v1/ (frozen) and dist/v2/ (revised).');
