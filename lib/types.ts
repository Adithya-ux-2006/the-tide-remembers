export type EntryLayout = "left" | "right" | "full" | "collage";

export interface Entry {
  id: string;
  date: string;
  title: string;
  body: string;
  images: string[];
  layout: EntryLayout;
  mood?: string;
  caption?: string;
}

export interface DiaryConfig {
  partnerName: string;
  myName: string;
  startDate: string;
  anniversaryDate: string;
  passcode: string;
  finalLetter: string;
}
