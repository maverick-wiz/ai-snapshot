// ArticleCard — thumbnail, headline, source badge, summary.
// AISNP-35 · Owner: PIXEL
import { memo } from 'react';
import type { NewsArticle } from '../types';

const FALLBACK_IMG = 'https://images.unsplash.com/photo-1677442135703-1787eea5ce01?w=400';

function sourceColor(source: string): string {
  let h = 0;
  for (let i = 0; i < source.length; i++) h = source.charCodeAt(i) + ((h << 5) - h);
  const hue = Math.abs(h) % 360;
  return `hsl(${hue},60%,65%)`;
}

function relativeTime(iso: string): string {
  const diff = (Date.now() - new Date(iso).getTime()) / 1000;
  if (diff < 60) return `${Math.floor(diff)}s ago`;
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  return `${Math.floor(diff / 86400)}d ago`;
}

export const ArticleCard = memo(function ArticleCard({ article }: { article: NewsArticle }) {
  const color = sourceColor(article.source);
  return (
    <a href={article.url} target="_blank" rel="noopener noreferrer"
      className="glass-card"
      style={{ display: 'flex', flexDirection: 'column', textDecoration: 'none',
               color: 'inherit', overflow: 'hidden' }}>
      <img src={article.image_url || FALLBACK_IMG} alt=""
        onError={(e) => { (e.target as HTMLImageElement).src = FALLBACK_IMG; }}
        loading="lazy"
        style={{ width: '100%', height: 140, objectFit: 'cover', borderRadius: '14px 14px 0 0' }} />
      <div style={{ padding: '14px 16px', display: 'flex', flexDirection: 'column', gap: 8, flex: 1 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span style={{ fontSize: '0.65rem', fontWeight: 600, padding: '2px 8px',
                         borderRadius: 20, background: `${color}22`, color,
                         border: `1px solid ${color}44`, whiteSpace: 'nowrap',
                         maxWidth: 120, overflow: 'hidden', textOverflow: 'ellipsis' }}>
            {article.source}
          </span>
          <span style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginLeft: 'auto' }}>
            {relativeTime(article.published_at)}
          </span>
        </div>
        <h3 style={{ margin: 0, fontSize: '0.9rem', fontWeight: 600, lineHeight: 1.4,
                     color: 'var(--text-primary)',
                     display: '-webkit-box', WebkitLineClamp: 2,
                     WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
          {article.title}
        </h3>
        <p style={{ margin: 0, fontSize: '0.78rem', color: 'var(--text-secondary)', lineHeight: 1.5,
                    display: '-webkit-box', WebkitLineClamp: 3,
                    WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
          {article.summary}
        </p>
      </div>
    </a>
  );
});
