import type { Entry, DiaryConfig } from "./types";

import configData from "@/content/config.json";
import entriesData from "@/content/entries.json";

export function getConfig(): DiaryConfig {
  return configData as DiaryConfig;
}

export function getEntries(): Entry[] {
  const entries = (entriesData as Entry[]).sort(
    (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()
  );
  return entries;
}

export function getEntry(id: string): Entry | undefined {
  return getEntries().find((e) => e.id === id);
}
