import {cp, rm} from 'node:fs/promises';
// Only static apps and comparison index; no transcripts/specs/evaluation files.
await rm('_site', {recursive: true, force: true});
await cp('dist', '_site', {recursive: true});
console.log('Pages artifact ready: /v1/ and /v2/ preserved together.');
