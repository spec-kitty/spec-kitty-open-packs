// @ts-check
// DocKitty docsite for spec-kitty-open-packs (ADR 2026-10-10-5). Wired exactly as
// doc-kitty's consumer-setup guide prescribes: the repo root is the Astro project
// and the repo-root `docs/` tree is the content root, so no file moves.
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';
import { defineDocKittyIntegrations } from '@spec-kitty/doc-toolkit/config';
import { specKittyTheme } from '@spec-kitty/doc-toolkit/themes/spec-kitty/index.ts';
import rehypeRepoLinks from './src/plugins/rehype-repo-links.mjs';

// GitHub Pages project site: https://<owner>.github.io/<repo>/
const OWNER = 'spec-kitty';
const REPO = 'spec-kitty-open-packs';
const SITE = `https://${OWNER}.github.io`;
const BASE = `/${REPO}`;
const REPO_URL = `https://github.com/${OWNER}/${REPO}`;

// The existing tree uses `index.md` section indexes (Common Docs default). Both
// basenames are accepted; this list MUST match the loader in src/content.config.ts.
const INDEX_BASENAME = ['README', 'index'];

export default defineConfig({
  site: SITE,
  base: BASE,
  markdown: {
    rehypePlugins: [
      [
        rehypeRepoLinks,
        { repoRoot: fileURLToPath(new URL('.', import.meta.url)), docsDir: 'docs', base: BASE, repoUrl: REPO_URL },
      ],
    ],
  },
  integrations: defineDocKittyIntegrations({
    title: 'Spec Kitty Open Packs',
    description:
      'Open, free Charter Packs for Spec Kitty: usage and authoring guides, the pack catalog, and generated pack reference.',
    // MUST equal the Astro `base` above (sitemap draft filter + feed URLs).
    base: BASE,
    social: { github: REPO_URL },
    theme: specKittyTheme,
    markua: false,
    diagrams: false,
    indexBasename: INDEX_BASENAME,
  }),
});
