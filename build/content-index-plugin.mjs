// Exposes the module index as `virtual:content-index`, built from content/module-*.json on every
// build and dev start, so it can never go stale and needs no generated file in the repository.
import path from "node:path";
import { buildContentIndex, moduleFiles } from "./content-index.mjs";

const virtualId = "virtual:content-index";
const resolvedId = "\0" + virtualId;

export function contentIndex() {
  let contentDir = "";
  return {
    name: "content-index",
    configResolved(config) { contentDir = path.join(config.root, "content"); },
    resolveId(id) { return id === virtualId ? resolvedId : null; },
    load(id) {
      if (id !== resolvedId) return null;
      for (const file of moduleFiles(contentDir)) this.addWatchFile(path.join(contentDir, file));
      return `export default ${JSON.stringify(buildContentIndex(contentDir))};`;
    },
  };
}
