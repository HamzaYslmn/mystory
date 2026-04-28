// MARK: - Vite Plugin: Dev-only MDX Editor
// Exposes POST /__save-mdx that writes raw MDX back to disk.
// Only mounted in dev (apply: 'serve'); has zero effect in production builds.
//
// content/stories/ lives outside the frontend root, so Vite's default watcher
// does not see it. We add it explicitly and invalidate any modules using
// import.meta.glob('../../../content/stories/**') after each new-file write
// so newly-created chapters appear without restarting the dev server.

import { writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname, resolve } from 'path';
import type { Plugin, ViteDevServer } from 'vite';

const ENDPOINT = '/__save-mdx';
const SLUG_RE = /^[a-zA-Z0-9_-]+$/;
const SOURCE_RE = /\.[mc]?[jt]sx?$/;

type Body = { bookSlug?: unknown; pageSlug?: unknown; content?: unknown };

function readBody(req: import('http').IncomingMessage): Promise<string> {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', (c) => { body += c; });
    req.on('end', () => resolve(body));
    req.on('error', reject);
  });
}

function invalidateGlobConsumers(server: ViteDevServer, root: string): void {
  for (const mod of server.moduleGraph.idToModuleMap.values()) {
    if (mod.file && SOURCE_RE.test(mod.file) && mod.transformResult?.code?.includes(root)) {
      server.moduleGraph.invalidateModule(mod);
    }
  }
}

export default function mdxEditorPlugin(storiesDir: string): Plugin {
  const root = resolve(storiesDir);
  return {
    name: 'mdx-editor',
    apply: 'serve',
    configureServer(server) {
      server.watcher.add(root);

      server.middlewares.use(ENDPOINT, async (req, res) => {
        if (req.method !== 'POST') {
          res.statusCode = 405; res.end('Method Not Allowed'); return;
        }
        try {
          const { bookSlug, pageSlug, content } = JSON.parse(await readBody(req)) as Body;

          if (
            typeof bookSlug !== 'string' || typeof pageSlug !== 'string' || typeof content !== 'string' ||
            !SLUG_RE.test(bookSlug) || !SLUG_RE.test(pageSlug)
          ) {
            res.statusCode = 400; res.end('Invalid payload'); return;
          }

          // MARK: - Resolve into chapters/ subfolder if present, else book root
          const chaptersDir = resolve(join(root, bookSlug, 'chapters'));
          const bookDir = resolve(join(root, bookSlug));
          const targetDir = existsSync(chaptersDir) ? chaptersDir : bookDir;
          const filePath = resolve(join(targetDir, `${pageSlug}.mdx`));
          if (!filePath.startsWith(root)) {
            res.statusCode = 400; res.end('Invalid path'); return;
          }

          const isNew = !existsSync(filePath);
          if (isNew) mkdirSync(dirname(filePath), { recursive: true });
          writeFileSync(filePath, content, 'utf8');

          if (isNew) {
            server.watcher.emit('add', filePath);
            invalidateGlobConsumers(server, root);
            server.ws.send({ type: 'full-reload' });
          }

          res.setHeader('Content-Type', 'application/json');
          res.end(JSON.stringify({ ok: true, created: isNew }));
        } catch (err) {
          res.statusCode = 500;
          res.end(String(err));
        }
      });
    },
  };
}
