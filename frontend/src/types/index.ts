// TypeScript types for AI-SNAPSHOT
// AISNP-31 · Owner: PIXEL

export interface NewsArticle {
  title: string;
  source: string;
  url: string;
  published_at: string;
  summary: string;
  image_url: string;
}

export interface StockQuote {
  symbol: string;
  name: string;
  price: number;
  change: number;
  change_pct: number;
  prev_close: number;
  volume: number;
  data_source: 'yahoo_finance' | 'gbm_fallback';
  last_updated: string;
}

export interface Country {
  iso2: string;
  name: string;
  flag: string;
}

export interface NewsResponse {
  articles: NewsArticle[];
  country: string;
  total: number;
  cached_at?: string;
}

export interface StocksResponse {
  quotes: StockQuote[];
  last_updated: string;
}
