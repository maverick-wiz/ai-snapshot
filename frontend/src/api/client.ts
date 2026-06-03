// API client functions — AISNP-31 · Owner: PIXEL
import type { NewsResponse, StocksResponse, Country } from '../types';

const API = import.meta.env.VITE_API_URL ?? '/api';

export async function fetchNews(country: string, limit = 20): Promise<NewsResponse> {
  const res = await fetch(`${API}/news?country=${country}&limit=${limit}`);
  if (!res.ok) throw new Error(`News API error: ${res.status}`);
  return res.json();
}

export async function fetchStocks(tickers = 'NVDA,AMD,TSM,ASML,MSFT,AVGO'): Promise<StocksResponse> {
  const res = await fetch(`${API}/stocks?tickers=${tickers}`);
  if (!res.ok) throw new Error(`Stocks API error: ${res.status}`);
  return res.json();
}

export async function fetchCountries(): Promise<Country[]> {
  const res = await fetch(`${API}/countries`);
  if (!res.ok) throw new Error(`Countries API error: ${res.status}`);
  return res.json();
}
