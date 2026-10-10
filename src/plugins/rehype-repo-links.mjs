/**
 * rehype-repo-links — make the docs tree's GitHub-native relative links work on
 * the built DocKitty site, without rewriting any authored Markdown.
 *
 * The `docs/` tree is read in two places: on GitHub (where `../guides/x.md` is
 * the correct, working link) and on the based Pages site (where Starlight emits
 * that href verbatim and it 404s — doc-kitty's consumer-setup guide documents
 * this caveat). Rather than churn every ADR and research page into
 * root-absolute routes, this plugin rewrites hrefs at render time:
 *
 *   - a relative link to a `.md`/`.mdx` page or a folder INSIDE the docs root
 *     becomes its based, root-absolute site route (`index.md` / `README.md`
 *     collapse to the folder route), keeping any `#fragment` — relative routes
 *     would otherwise resolve against the page's own trailing-slash URL;
 *   - a relative link that leaves the docs root (`../../SECURITY.md`,
 *     `../../packs/`) becomes a GitHub URL on the default branch, because those
 *     files are not part of the site;
 *   - a relative link to a non-page file under docs/, or to anything under the
 *     reserved docs/_meta/, becomes a GitHub URL too, since only pages are served;
 *   - malformed percent-encoding leaves the link untouched; route and URL path
 *     segments are re-encoded, and `?query` / `#fragment` are carried over;
 *   - everything else (external, root-absolute, anchors)
 *     is left untouched.
 *
 * Emitted routes already carry the base, so the toolkit's own
 * base-absolute-links pass (which skips already-based hrefs) is a no-op on them.
 */
import path from 'node:path';

const SCHEME = /^[a-z][a-z0-9+.-]*:/i;
const PAGE_EXT = /\.mdx?$/i;
const INDEX_BASENAMES = new Set(['index', 'readme']);

/**
 * @param {{ repoRoot: string, docsDir?: string, base?: string, repoUrl: string, branch?: string }} options
 */
export default function rehypeRepoLinks(options) {
  const repoRoot = path.resolve(options.repoRoot);
  const docsRoot = path.resolve(repoRoot, options.docsDir ?? 'docs');
  const base = (options.base ?? '').replace(/\/+$/, '');
  const blobBase = `${options.repoUrl.replace(/\/+$/, '')}/blob/${options.branch ?? 'main'}`;
  const treeBase = `${options.repoUrl.replace(/\/+$/, '')}/tree/${options.branch ?? 'main'}`;

  /** Percent-encode each path segment (the source href is decoded first). */
  const encodePath = (rel) => rel.split('/').map((seg) => encodeURIComponent(seg)).join('/');

  /** @param {string} href @param {string} sourceFile */
  function rewrite(href, sourceFile) {
    if (!href || href.startsWith('#') || href.startsWith('/') || SCHEME.test(href)) return null;
    // Split off `?query` and `#fragment`; both are carried over verbatim.
    const cut = href.search(/[?#]/);
    const rawPath = cut === -1 ? href : href.slice(0, cut);
    const suffix = cut === -1 ? '' : href.slice(cut);
    if (!rawPath) return null;
    let decoded;
    try {
      decoded = decodeURI(rawPath);
    } catch {
      return null; // malformed percent-encoding (`bad%zz.md`): leave the link as authored
    }
    const target = path.resolve(path.dirname(sourceFile), decoded);
    const insideDocs = target === docsRoot || target.startsWith(docsRoot + path.sep);
    const isFolder = rawPath.endsWith('/') || !path.extname(target);
    const relRepo = path.relative(repoRoot, target).split(path.sep).join('/');

    if (insideDocs) {
      const rel = path.relative(docsRoot, target).split(path.sep).join('/');
      // docs/_meta/ is reserved (not part of the site), and only pages are served:
      // point both at GitHub instead.
      if (rel === '_meta' || rel.startsWith('_meta/') || (!isFolder && !PAGE_EXT.test(target))) {
        return `${isFolder ? treeBase : blobBase}/${encodePath(relRepo)}${suffix}`;
      }
      const parts = rel.replace(PAGE_EXT, '').split('/').filter(Boolean);
      if (!isFolder && parts.length && INDEX_BASENAMES.has(parts[parts.length - 1].toLowerCase())) parts.pop();
      const route = encodePath(parts.join('/'));
      return `${base}/${route ? `${route}/` : ''}${suffix}`;
    }

    const insideRepo = target.startsWith(repoRoot + path.sep);
    if (!insideRepo) return null;
    return `${isFolder ? treeBase : blobBase}/${encodePath(relRepo)}${suffix}`;
  }

  /** @param {any} node @param {string} sourceFile */
  function walk(node, sourceFile) {
    if (node.type === 'element' && node.tagName === 'a' && typeof node.properties?.href === 'string') {
      const next = rewrite(node.properties.href, sourceFile);
      if (next !== null) node.properties.href = next;
    }
    for (const child of node.children ?? []) walk(child, sourceFile);
  }

  return (tree, file) => {
    const source = file?.path ?? file?.history?.[0];
    if (!source) return;
    const sourceFile = path.resolve(String(source).startsWith('file:') ? new URL(String(source)).pathname : String(source));
    if (!sourceFile.startsWith(docsRoot + path.sep)) return;
    walk(tree, sourceFile);
  };
}
