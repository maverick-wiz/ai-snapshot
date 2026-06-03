// NewsPanel — useNews hook, article grid, error state. Wrapped in memo.
// AISNP-37 · Owner: PIXEL
import { memo } from 'react';
import { useNews } from '../hooks/useNews';
import { ArticleCard } from './ArticleCard';
import { CountryFilter } from './CountryFilter';
import { LoadingSkeleton } from './LoadingSkeleton';

interface Props { country: string; onCountryChange: (c: string) => void; }

export const NewsPanel = memo(function NewsPanel({ country, onCountryChange }: Props) {
  const { articles, newsLoading, newsError, refetch } = useNews(country);

  return (
    <section style={{ padding: '28px 32px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 24, flexWrap: 'wrap' }}>
        <h2 style={{ margin: 0, fontSize: '1rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
          📰 AI News
        </h2>
        <CountryFilter selected={country} onChange={onCountryChange} />
        {newsError && (
          <div style={{ fontSize: '0.8rem', color: 'var(--loss-red)', display: 'flex', gap: 8 }}>
            ⚠ {newsError}
            <button onClick={refetch} style={{ background: 'none', border: 'none',
              color: 'var(--accent-indigo-light)', cursor: 'pointer', fontSize: '0.8rem' }}>
              Retry
            </button>
          </div>
        )}
        <span style={{ marginLeft: 'auto', fontSize: '0.72rem', color: 'var(--text-muted)' }}>
          {!newsLoading && `${articles.length} articles`}
        </span>
      </div>

      {newsLoading
        ? <LoadingSkeleton count={6} />
        : (
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
            gap: 20,
          }}>
            {articles.map((a, i) => <ArticleCard key={`${a.url}-${i}`} article={a} />)}
            {articles.length === 0 && !newsError && (
              <p style={{ color: 'var(--text-muted)', gridColumn: '1/-1', textAlign: 'center', padding: 40 }}>
                No articles found for this country. Try another region.
              </p>
            )}
          </div>
        )
      }
    </section>
  );
});
