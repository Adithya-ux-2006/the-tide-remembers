"use client";

import { use } from "react";
import WatchPlayer from "@/components/WatchPlayer";
import { getEntry } from "@/lib/content";

export default function WatchPageClient({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const entry = getEntry(id);

  if (!entry) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <p className="text-white text-xl mb-4">Episode not found</p>
          <a href="/browse" className="text-accent hover:underline">Back to browse</a>
        </div>
      </div>
    );
  }

  return <WatchPlayer entry={entry} />;
}
