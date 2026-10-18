// @ts-check
import { defineConfig } from 'astro/config';
import { defineDocKittyIntegrations } from '@spec-kitty/doc-toolkit/config';
import { specKittyTheme } from '@spec-kitty/doc-toolkit/themes/spec-kitty/index.ts';

// The docs tree lives at the repository root (../docs); this site/ project only
// renders it. GitHub Pages serves a project site under /<repo>, so BASE is that
// path. SITE and BASE can be overridden for a local preview at the domain root.
const SITE = process.env.DK_SITE ?? 'https://spec-kitty.github.io';
const BASE = process.env.DK_BASE ?? '/spec-kitty-open-packs';

export default defineConfig({
  site: SITE,
  base: BASE,
  integrations: defineDocKittyIntegrations({
    title: 'spec-kitty-open-packs',
    description: 'Open Charter Packs for Spec Kitty (Brain Kitty): the pack catalog, artefact and contract reference, organisational support, and usage and authoring guides.',
    // MUST equal the site `base` above.
    base: BASE,
    // MUST equal the loader `base` in src/content.config.ts. Without it the toolkit
    // looks for site/docs, ignores docs/_meta/sections.yaml and lists drafts in the sitemap.
    docsDir: '../docs',
    // Brain Kitty brand mark (olive bow tie) and olive colourway over the Spec Kitty theme.
    theme: {
      extends: specKittyTheme,
      assets: { logo: './src/assets/brain-kitty.png' },
      customCss: ['./src/styles/brain-kitty.css'],
    },
    markua: true,
    // Mermaid fences render in the browser (doc-kitty's client renderer); no PlantUML
    // or Chromium is needed at build time. PlantUML diagrams are committed as SVGs.
    diagrams: true,
    // The single source of index basenames (the loader and the dockitty-* CLI
    // read it from here). The docs tree uses index.md as the section landing page.
    indexBasename: ['index', 'README'],
  }),
});
