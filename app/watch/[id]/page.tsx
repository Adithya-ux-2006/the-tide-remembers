import { getEntries } from "@/lib/content";
import WatchPageClient from "./client";

export function generateStaticParams() {
  return getEntries().map((entry) => ({ id: entry.id }));
}

export default function WatchPage({ params }: { params: Promise<{ id: string }> }) {
  return <WatchPageClient params={params} />;
}
