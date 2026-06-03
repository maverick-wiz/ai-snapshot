// StockCard — price, delta, 1-second flash animation on change.
// AISNP-40 · Owner: PIXEL
import { useEffect, useRef, useState } from 'react';
import type { StockQuote } from '../types';

interface Props { quote: StockQuote; }

export function StockCard({ quote }: Props) {
  const prevPrice = useRef<number | null>(null);
  const [flashClass, setFlashClass] = useState('');

  useEffect(() => {
    if (prevPrice.current !== null && prevPrice.current !== quote.price) {
      const cls = quote.price > prevPrice.current ? 'flash-gain' : 'flash-loss';
      setFlashClass(cls);
      const t = setTimeout(() => setFlashClass(''), 1000);
      prevPrice.current = quote.price;
      return () => clearTimeout(t);
    }
    prevPrice.current = quote.price;
  }, [quote.price]);

  const isGain = quote.change >= 0;
  const colour = isGain ? 'var(--gain-green)' : 'var(--loss-red)';

  return (
    <div className={`glass-card ${flashClass}`} style={{
      padding: '16px 20px', minWidth: 150, flex: '1 1 150px',
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <span style={{ fontWeight: 700, fontSize: '1rem', color: 'var(--accent-indigo-light)' }}>
          {quote.symbol}
        </span>
        {quote.data_source === 'gbm_fallback' && (
          <span style={{ fontSize: '0.6rem', background: 'rgba(251,191,36,0.15)',
                         color: '#fbbf24', padding: '1px 6px', borderRadius: 4 }}>SIM</span>
        )}
      </div>
      <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: 8,
                    whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
        {quote.name}
      </div>
      <div className="price-figure" style={{ fontSize: '1.4rem', fontWeight: 700, color: 'var(--text-primary)' }}>
        ${quote.price.toFixed(2)}
      </div>
      <div className="price-figure" style={{ fontSize: '0.82rem', color: colour, marginTop: 4 }}>
        {isGain ? '+' : ''}{quote.change.toFixed(2)} ({isGain ? '+' : ''}{quote.change_pct.toFixed(2)}%)
      </div>
      <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: 6 }}>
        Prev close: <span className="price-figure">${quote.prev_close.toFixed(2)}</span>
      </div>
    </div>
  );
}
