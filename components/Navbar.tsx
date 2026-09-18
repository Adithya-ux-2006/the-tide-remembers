"use client";

import { useState, useEffect, useCallback } from "react";
import { motion } from "framer-motion";
import { useRouter, usePathname } from "next/navigation";
import { tryGet } from "@/lib/utils";
import { getConfig, getEntries } from "@/lib/content";
import type { Entry } from "@/lib/types";

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<Entry[]>([]);
  const router = useRouter();
  const pathname = usePathname();
  const config = getConfig();
  const profileName = tryGet("usplus-profile") || config.myName;

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const handleSearch = useCallback((q: string) => {
    setSearchQuery(q);
    if (!q.trim()) { setSearchResults([]); return; }
    const entries = getEntries();
    const lower = q.toLowerCase();
    setSearchResults(
      entries.filter(
        (e) =>
          e.title.toLowerCase().includes(lower) ||
          e.tags.some((t) => t.toLowerCase().includes(lower))
      )
    );
  }, []);

  const links = [
    { label: "Home", href: "/browse" },
    { label: "Seasons", href: "/browse#seasons" },
    { label: "Top 10", href: "/browse#top10" },
    { label: "Trips", href: "/browse#trips" },
  ];

  return (
    <>
      <motion.nav
        className="fixed top-0 left-0 right-0 z-50 px-4 sm:px-8 lg:px-12 h-14 flex items-center justify-between transition-colors duration-300"
        style={{ backgroundColor: scrolled ? "var(--bg)" : "transparent" }}
      >
        <div className="flex items-center gap-6">
          <button
            onClick={() => router.push("/browse")}
            className="text-3xl tracking-tight cursor-pointer"
            style={{ fontFamily: "var(--font-bebas)", color: "var(--accent)" }}
          >
            {config.appName}
          </button>
          <div className="hidden md:flex items-center gap-4">
            {links.map((link) => (
              <button
                key={link.label}
                onClick={() => router.push(link.href)}
                className={`text-sm cursor-pointer transition-colors ${
                  pathname === link.href ? "text-text font-semibold" : "text-text-dim hover:text-text"
                }`}
              >
                {link.label}
              </button>
            ))}
          </div>
        </div>

        <div className="flex items-center gap-4">
          {/* Search */}
          <div className="relative">
            <button
              onClick={() => { setSearchOpen(!searchOpen); setSearchQuery(""); setSearchResults([]); }}
              className="text-text-dim hover:text-text transition-colors cursor-pointer"
              aria-label="Search"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="11" cy="11" r="8" />
                <line x1="21" y1="21" x2="16.65" y2="16.65" />
              </svg>
            </button>
            {searchOpen && (
              <motion.div
                className="absolute right-0 top-10 w-72 bg-bg-elev border border-white/10 rounded-lg p-3 shadow-xl"
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => handleSearch(e.target.value)}
                  className="w-full px-3 py-2 bg-card border border-white/10 rounded text-sm text-text focus:outline-none focus:border-accent"
                  placeholder="Search memories..."
                  autoFocus
                  aria-label="Search memories"
                />
                {searchResults.length > 0 && (
                  <div className="mt-2 max-h-60 overflow-y-auto" aria-live="polite">
                    <p className="text-xs text-text-dim mb-2">{searchResults.length} result{searchResults.length !== 1 ? "s" : ""}</p>
                    {searchResults.map((entry) => (
                      <button
                        key={entry.id}
                        onClick={() => { router.push(`/watch/${entry.id}`); setSearchOpen(false); }}
                        className="w-full flex items-center gap-3 p-2 rounded hover:bg-card transition-colors text-left cursor-pointer"
                      >
                        <div className="w-16 h-9 bg-card rounded overflow-hidden flex-shrink-0" />
                        <div>
                          <p className="text-sm text-text">{entry.title}</p>
                          <p className="text-xs text-text-dim">S{entry.season} E{entry.episode}</p>
                        </div>
                      </button>
                    ))}
                  </div>
                )}
              </motion.div>
            )}
          </div>

          {/* Profile */}
          <div className="w-8 h-8 rounded bg-accent flex items-center justify-center text-white text-xs font-bold">
            {profileName.charAt(0)}
          </div>
        </div>
      </motion.nav>

      {/* Mobile bottom bar */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 z-50 bg-bg-elev border-t border-white/10 h-14 flex items-center justify-around px-4">
        {links.map((link) => (
          <button
            key={link.label}
            onClick={() => router.push(link.href)}
            className={`flex flex-col items-center gap-0.5 text-[10px] cursor-pointer transition-colors ${
              pathname === link.href ? "text-accent" : "text-text-dim"
            }`}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <rect x="3" y="3" width="7" height="7" rx="1" />
              <rect x="14" y="3" width="7" height="7" rx="1" />
              <rect x="3" y="14" width="7" height="7" rx="1" />
              <rect x="14" y="14" width="7" height="7" rx="1" />
            </svg>
            {link.label}
          </button>
        ))}
      </div>
    </>
  );
}
