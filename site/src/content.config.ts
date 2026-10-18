import { defineCollection } from 'astro:content';
import {
  docKittyDocsSchema,
  docKittyDocsLoader,
} from '@spec-kitty/doc-toolkit/schema';

export const collections = {
  docs: defineCollection({
    // The content root is the repository's docs/ tree, one level up from site/.
    // Index basenames are set once, on the integration in astro.config.mjs
    // (doc-toolkit >= 0.3.0 refuses a differing loader value).
    loader: docKittyDocsLoader({ base: '../docs' }),
    schema: docKittyDocsSchema(),
  }),
};
