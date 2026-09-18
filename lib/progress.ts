import { tryGet, trySet } from "./utils";

export interface ProgressData {
  beatIndex: number;
  timestamp: number;
}

const STORAGE_KEY = "usplus-progress";

export function getProgress(): Record<string, ProgressData> {
  const raw = tryGet(STORAGE_KEY);
  if (!raw) return {};
  try {
    return JSON.parse(raw);
  } catch {
    return {};
  }
}

export function setProgress(entryId: string, beatIndex: number): void {
  const all = getProgress();
  all[entryId] = { beatIndex, timestamp: Date.now() };
  trySet(STORAGE_KEY, JSON.stringify(all));
}

export function getEntryProgress(entryId: string): ProgressData | null {
  return getProgress()[entryId] || null;
}

export function getContinueWatching(): string[] {
  const all = getProgress();
  return Object.entries(all)
    .sort(([, a], [, b]) => b.timestamp - a.timestamp)
    .map(([id]) => id)
    .slice(0, 10);
}
