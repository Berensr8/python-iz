"use client";
import { useEffect, useReducer, useState } from "react";
import { loadedModule, loadModule } from "@/lib/content";

/** The full text of a module, fetched on first use. `module` is undefined while loading; `failed` means the fetch failed. */
export function useModule(id: number) {
  const [failedId, setFailedId] = useState<number | null>(null);
  const [, refresh] = useReducer((count: number) => count + 1, 0);
  const current = loadedModule(id);
  useEffect(() => {
    if (loadedModule(id)) return;
    let active = true;
    loadModule(id).then(
      () => { if (active) refresh(); },
      () => { if (active) setFailedId(id); },
    );
    return () => { active = false; };
  }, [id]);
  return { module: current, failed: !current && failedId === id };
}
