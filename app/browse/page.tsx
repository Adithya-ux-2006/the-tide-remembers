"use client";

import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import Row from "@/components/Row";
import DetailModal from "@/components/DetailModal";
import MusicToggle from "@/components/MusicToggle";
import SmoothScroll from "@/components/SmoothScroll";
import { getRows, getEntryIdsForRow } from "@/lib/content";
import { getContinueWatching } from "@/lib/progress";
import { useState } from "react";
import type { Entry } from "@/lib/types";

export default function BrowsePage() {
  const rows = getRows();
  const [selectedEntry, setSelectedEntry] = useState<Entry | null>(null);

  return (
    <SmoothScroll>
      <div className="min-h-screen bg-bg pt-14 pb-20 md:pb-0">
        <Navbar />
        <Hero />

        <div className="relative z-10 -mt-24 sm:-mt-32">
          {rows.map((row) => {
            let entries = getEntryIdsForRow(row);

            // Continue watching row
            if (row.type === "continue") {
              const continueIds = getContinueWatching();
              entries = continueIds
                .map((id) => entries.find((e) => e.id === id) || null)
                .filter(Boolean) as Entry[];
            }

            return (
              <Row
                key={row.id}
                id={row.id}
                title={row.title}
                entries={entries}
                isTop10={row.type === "top10"}
                isContinue={row.type === "continue"}
              />
            );
          })}
        </div>

        <DetailModal entry={selectedEntry} onClose={() => setSelectedEntry(null)} />
        <MusicToggle />
      </div>
    </SmoothScroll>
  );
}
