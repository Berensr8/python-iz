// Builds the static site for GitHub Pages into dist/client.
// PAGES_BASE_PATH defaults to "/python-iz"; set it to "" for a user site or custom domain.
import { spawnSync } from "node:child_process";
import { existsSync, readFileSync, renameSync, rmSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const basePath = process.env.PAGES_BASE_PATH ?? "/python-iz";
const out = path.join(root, "dist-pages", "client");

// vinext always writes to dist/, which the Cloudflare build shares. Start clean and move the
// result to dist-pages/ afterwards; run `npm run build` again to regenerate the Sites build.
rmSync(path.join(root, "dist"), { recursive: true, force: true });
rmSync(path.join(root, "dist-pages"), { recursive: true, force: true });
const build = spawnSync(process.execPath, [path.join(root, "node_modules", "vinext", "dist", "cli.js"), "build"], {
  cwd: root,
  stdio: "inherit",
  env: { ...process.env, PAGES_BUILD: "1", PAGES_BASE_PATH: basePath },
});
if (build.error) throw build.error;

// On Windows Node can exit non-zero while shutting down after a finished build; judge by the output.
if (!existsSync(path.join(root, "dist", "client", "index.html"))) throw new Error(`Derleme index.html üretmedi (çıkış kodu ${build.status}).`);
renameSync(path.join(root, "dist"), path.join(root, "dist-pages"));
const indexPath = path.join(out, "index.html");

// Every asset URL must carry the base path, or the site breaks under /repo-name/.
const html = readFileSync(indexPath, "utf8");
const bare = [...html.matchAll(/(?:href|src)="(\/[^"]*)"/g)].map(match => match[1]).filter(url => !url.startsWith(`${basePath}/`));
if (bare.length) throw new Error(`Önek olmayan adresler var: ${[...new Set(bare)].join(", ")}`);

// GitHub Pages runs Jekyll unless told otherwise, and Jekyll hides the _next folder.
writeFileSync(path.join(out, ".nojekyll"), "");
console.log(`Hazır: ${out} (taban yol: "${basePath}")`);
