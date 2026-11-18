import http from 'node:http';
import {readFile, stat} from 'node:fs/promises';
import {resolve, extname, sep} from 'node:path';
import './build.mjs';
const root = resolve('dist'), port = Number(process.env.PORT || 4183);
http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, 'http://localhost');
    let path = resolve(root, '.' + decodeURIComponent(url.pathname));
    if (path !== root && !path.startsWith(root + sep)) throw Error();
    if ((await stat(path)).isDirectory()) {
      if (!url.pathname.endsWith('/')) {res.writeHead(302, {Location: url.pathname + '/'});res.end();return;}
      path = resolve(path, 'index.html');
    }
    const data = await readFile(path);
    res.writeHead(200, {'Content-Type': ({'.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css'})[extname(path)] || 'application/octet-stream', 'Cache-Control': 'no-store'});
    res.end(data);
  } catch {res.writeHead(404);res.end('Not found');}
}).listen(port, '127.0.0.1', () => console.log(`Compare: http://localhost:${port}/ | V2: http://localhost:${port}/v2/`));
