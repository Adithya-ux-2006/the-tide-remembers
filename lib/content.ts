import type { Entry, Row, AppConfig } from "./types";

import configData from "@/content/config.json";
import entriesData from "@/content/entries.json";
import rowsData from "@/content/rows.json";

export function getConfig(): AppConfig {
  return configData as AppConfig;
}

export function getEntries(): Entry[] {
  return (entriesData as Entry[]).sort(
    (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()
  );
}

export function getEntry(id: string): Entry | undefined {
  return getEntries().find((e) => e.id === id);
}

export function getRows(): Row[] {
  return rowsData as Row[];
}

export function getEntriesBySeason(season: number): Entry[] {
  return getEntries().filter((e) => e.season === season);
}

export function getEntriesByTag(tag: string): Entry[] {
  return getEntries().filter((e) => e.tags.includes(tag));
}

export function getFeaturedEntries(): Entry[] {
  return getEntries().filter((e) => e.featured);
}

export function getTop10Entries(): Entry[] {
  return getEntries().filter((e) => e.top10);
}

export function getEntryIdsForRow(row: Row): Entry[] {
  const entries = getEntries();
  if (row.type === "season" && row.ref) {
    return entries.filter((e) => e.season === Number(row.ref));
  }
  if (row.type === "tag" && row.ref) {
    return entries.filter((e) => e.tags.includes(row.ref!));
  }
  if (row.type === "top10") {
    return entries.filter((e) => e.top10);
  }
  if (row.entryIds) {
    return row.entryIds
      .map((id) => entries.find((e) => e.id === id))
      .filter(Boolean) as Entry[];
  }
  return [];
}
