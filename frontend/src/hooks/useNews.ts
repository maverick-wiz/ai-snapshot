// useNews — fetches news on country change only. Never rerenders on stock updates.
// AISNP-37 · Owner: PIXEL
import { useState, useEffect } from 'react';
import { fetchNews } from '../api/client';
import type { NewsArticle } from '../types';

interface UseNewsResult {
  articles: NewsArticle[];
  newsLoading: boolean;
  newsError: string | null;
  refetch: () => void;
}

export function useNews(country: string, limit = 20): UseNewsResult {
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [newsLoading, setNewsLoading] = useState(true);
  const [newsError, setNewsError] = useState<string | null>(null);

  const load = async () => {
    setNewsLoading(true);
    setNewsError(null);
    try {
      const res = await fetchNews(country, limit);
      setArticles(res.articles);
    } catch (err) {
      setNewsError(err instanceof Error ? err.message : 'News fetch failed');
    } finally {
      setNewsLoading(false);
    }
  };

  useEffect(() => {
    load();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [country]);

  return { articles, newsLoading, newsError, refetch: load };
}
