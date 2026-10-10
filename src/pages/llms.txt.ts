import { llmsTxtRoute } from '@spec-kitty/doc-toolkit/routes';
export const GET = llmsTxtRoute({
  title: 'Spec Kitty Open Packs',
  description: 'Open, free Charter Packs for Spec Kitty: guides, pack catalog, and generated pack reference.',
  indexBasename: ['README', 'index'],
});
