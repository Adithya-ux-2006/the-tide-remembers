export interface Entry {
  id: string;
  season: 1 | 2 | 3;
  episode: number;
  date: string;
  title: string;
  synopsis: string;
  story: string;
  thumb: string;
  images: string[];
  backdrop?: string;
  tags: string[];
  runtime?: string;
  featured?: boolean;
  top10?: boolean;
  music?: string;
}

export interface Row {
  id: string;
  title: string;
  type: "season" | "tag" | "top10" | "continue" | "custom";
  ref?: string;
  entryIds?: string[];
}

export interface AppConfig {
  appName: string;
  myName: string;
  partnerName: string;
  startDate: string;
  anniversaryDate: string;
  passcode: string;
  finalLetter: string[];
}
