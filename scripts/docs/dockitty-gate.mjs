#!/usr/bin/env node
// Run one of @spec-kitty/doc-toolkit's bare-Node gate scripts (validate-frontmatter,
// check-links, assert-no-broken-links) against this repo's docs/ tree or built dist/.
//
// The toolkit's gates only execute their CLI when invoked by their REAL path
// (they compare import.meta.url to argv[1]); pnpm installs the package behind a
// symlink, so `node node_modules/@spec-kitty/doc-toolkit/scripts/x.mjs` silently
// does nothing and exits 0. Resolve the real path first, then run it.
//
// Usage: node scripts/docs/dockitty-gate.mjs <validate-frontmatter|check-links|assert-no-broken-links> [args...]
import { realpathSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const [gate, ...args] = process.argv.slice(2);
if (!['validate-frontmatter', 'check-links', 'assert-no-broken-links'].includes(gate ?? '')) {
  console.error('usage: dockitty-gate.mjs <validate-frontmatter|check-links|assert-no-broken-links> [args...]');
  process.exit(2);
}
// The gates ship in the package's `files` but are not in its `exports` map, so
// they are located on disk rather than through module resolution.
const repoRoot = fileURLToPath(new URL('../..', import.meta.url));
const script = realpathSync(join(repoRoot, 'node_modules', '@spec-kitty', 'doc-toolkit', 'scripts', `${gate}.mjs`));
const result = spawnSync(process.execPath, [script, ...args], { stdio: 'inherit' });
process.exit(result.status ?? 1);
