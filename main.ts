// news-image-20261120 entry (Node 22, standard library only).
// The program copies the drawn entry.png beside this file to
// /output/entry.png. A plain copy is deterministic by construction:
// two runs write byte-identical bytes, and nothing is fetched at
// runtime. Outside the grader, MAKEFUN_OUTPUT_DIR stands in for
// /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
