"use client";

import DiaryScroller from "@/components/DiaryScroller";
import FinalPage from "@/components/FinalPage";
import MusicToggle from "@/components/MusicToggle";
import SmoothScroll from "@/components/SmoothScroll";
import { getEntries, getConfig } from "@/lib/content";

export default function DiaryPage() {
  const entries = getEntries();
  const config = getConfig();

  return (
    <SmoothScroll>
      <main className="min-h-screen bg-paper">
        <DiaryScroller entries={entries} />
        <FinalPage finalLetter={config.finalLetter} />
        <MusicToggle />
      </main>
    </SmoothScroll>
  );
}
