// useStocks — isolated 5-second polling, never touches news state.
// AISNP-41 · Owner: PIXEL
import { useState, useEffect, useRef } from 'react';
import { fetchStocks } from '../api/client';
import type { StockQuote } from '../types';

interface UseStocksResult {
  stockData: StockQuote[];
  stockLoading: boolean;
  stockError: string | null;
  lastUpdated: string | null;
}

export function useStocks(tickers = 'NVDA,AMD,TSM,ASML,MSFT,AVGO'): UseStocksResult {
  const [stockData, setStockData] = useState<StockQuote[]>([]);
  const [stockLoading, setStockLoading] = useState(true);
  const [stockError, setStockError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<string | null>(null);
  const prevDataRef = useRef<StockQuote[]>([]);

  const poll = async () => {
    try {
      const res = await fetchStocks(tickers);
      prevDataRef.current = stockData;
      setStockData(res.quotes);
      setLastUpdated(res.last_updated);
      setStockError(null);
    } catch (err) {
      // Retain last-known data on error
      setStockError(err instanceof Error ? err.message : 'Stock fetch failed');
    } finally {
      setStockLoading(false);
    }
  };

  useEffect(() => {
    poll();
    const interval = setInterval(poll, 5000);
    return () => clearInterval(interval);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tickers]);

  return { stockData, stockLoading, stockError, lastUpdated };
}
