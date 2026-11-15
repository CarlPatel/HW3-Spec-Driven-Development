import {mkdir, cp, rm, writeFile} from 'node:fs/promises';
// Publish only the built app. Relative module/asset URLs work under repo/v1/.
await rm('_site', {recursive: true, force: true});
await mkdir('_site/v1', {recursive: true});
await cp('dist', '_site/v1', {recursive: true});
await writeFile('_site/.nojekyll', '');
await writeFile('_site/index.html', '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url=./v1/"><title>Pressroom prototypes</title></head><body><a href="./v1/">Open Prototype V1</a></body></html>');
console.log('GitHub Pages artifact ready in _site/; V1 lives at ./v1/');

