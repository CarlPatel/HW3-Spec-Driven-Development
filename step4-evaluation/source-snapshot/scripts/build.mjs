import {mkdir,cp,rm} from 'node:fs/promises';
await rm('dist',{recursive:true,force:true});await mkdir('dist',{recursive:true});await cp('frontend','dist',{recursive:true});console.log('Built static V1 in dist/');

