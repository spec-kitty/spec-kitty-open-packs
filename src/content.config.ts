import { defineCollection } from 'astro:content';
import {
  docKittyDocsSchema,
  docKittyDocsLoader,
  docKittyBibliographySchema,
  docKittyBibliographyLoader,
  docKittyToolsSchema,
  docKittyToolsLoader,
} from '@spec-kitty/doc-toolkit/schema';

export const collections = {
  docs: defineCollection({
    // `base` and `indexBasename` MUST match astro.config.mjs (config invariant).
    loader: docKittyDocsLoader({ base: 'docs', indexBasename: ['README', 'index'] }),
    schema: docKittyDocsSchema(),
  }),
  bibliography: defineCollection({
    loader: docKittyBibliographyLoader(),
    schema: docKittyBibliographySchema(),
  }),
  tools: defineCollection({
    loader: docKittyToolsLoader(),
    schema: docKittyToolsSchema(),
  }),
};
