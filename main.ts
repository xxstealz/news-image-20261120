// news-image-20261120 entry (Node 22, standard library only).
// The program copies the drawn entry.png beside this file to
// /output/entry.png. A plain copy is deterministic by construction:
// two runs write byte-identical bytes, and nothing is fetched at
// runtime. Outside the grader, MAKEFUN_OUTPUT_DIR stands in for
// /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const src = new URL('./entry.png', import.meta.url);
if (!existsSync(src)) {
  throw new Error('entry.png is missing next to main.ts; run draw_entry.py first');
}
// An empty MAKEFUN_OUTPUT_DIR falls back to /output instead of
// resolving to a relative "entry.png" in the working directory.
const outDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';
// The grader normally pre-creates /output, but a fresh directory
// must not fail the whole entry with an opaque ENOENT.
mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, 'entry.png'));
