// MARK: - Vite Plugin: MDX File Modification Times
// Scans content/stories/**/*.mdx and exposes a virtual module
// with a map of { "bookSlug/pageSlug" → "YYYY-MM-DD" }.

import { statSync, readdirSync } from 'fs';
import { join, basename, extname } from 'path';
import type { Plugin } from 'vite';

const VIRTUAL_ID = 'virtual:mdx-mtime';
const RESOLVED_ID = '\0' + VIRTUAL_ID;

// MARK: - Skip folders that hold docs, not chapters
const SKIP_DIRS = new Set(['docs', 'library', 'assets']);

function collectMtimes(storiesDir: string): Record<string, string> {
  const result: Record<string, string> = {};

  // MARK: - Walk books (recursive into chapters/ etc.)
  for (const bookDir of readdirSync(storiesDir, { withFileTypes: true })) {
    if (!bookDir.isDirectory() || bookDir.name.startsWith('.')) continue;
    walkDir(join(storiesDir, bookDir.name), bookDir.name, result);
  }
  return result;
}

function walkDir(dir: string, bookSlug: string, out: Record<string, string>): void {
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      if (SKIP_DIRS.has(entry.name) || entry.name.startsWith('.')) continue;
      walkDir(join(dir, entry.name), bookSlug, out);
    } else if (entry.isFile() && extname(entry.name) === '.mdx') {
      const pageSlug = basename(entry.name, '.mdx');
      const key = `${bookSlug}/${pageSlug}`;
      const stat = statSync(join(dir, entry.name));
      out[key] = stat.mtime.toISOString().slice(0, 10);
    }
  }
}

export default function mdxMtimePlugin(storiesDir: string): Plugin {
  return {
    name: 'mdx-mtime',
    resolveId(id) {
      if (id === VIRTUAL_ID) return RESOLVED_ID;
    },
    load(id) {
      if (id !== RESOLVED_ID) return;
      const mtimes = collectMtimes(storiesDir);
      return `export default ${JSON.stringify(mtimes)};`;
    },
    // MARK: - HMR: re-scan on mdx file changes
    handleHotUpdate({ file, server }) {
      if (file.endsWith('.mdx')) {
        const mod = server.moduleGraph.getModuleById(RESOLVED_ID);
        if (mod) server.moduleGraph.invalidateModule(mod);
      }
    },
  };
}
