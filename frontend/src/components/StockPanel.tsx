// StockPanel — integrates useStocks, StockCard, LiveIndicator.
// AISNP-43 · Owner: PIXEL
import { memo } from 'react';
import { useStocks } from '../hooks/useStocks';
import { StockCard } from './StockCard';
import { LiveIndicator } from './LiveIndicator';

export const StockPanel = memo(function StockPanel() {
  const { stockData, stockLoading, stockError, lastUpdated } = useStocks();

  const fmt = (iso: string | null) => iso
    ? new Date(iso).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    : '—';

  return (
    <section style={{ padding: '20px 32px 0' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 14 }}>
        <h2 style={{ margin: 0, fontSize: '1rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
          📈 AI &amp; Semiconductor Stocks
        </h2>
        <LiveIndicator active={!stockError} />
        {stockError && (
          <span style={{ fontSize: '0.72rem', color: 'var(--loss-red)' }}>⚠ {stockError}</span>
        )}
        <span style={{ marginLeft: 'auto', fontSize: '0.72rem', color: 'var(--text-muted)',
                       fontVariantNumeric: 'tabular-nums' }}>
          Updated: {fmt(lastUpdated)}
        </span>
      </div>

      {stockLoading && stockData.length === 0 ? (
        <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
          {[...Array(6)].map((_, i) => (
            <div key={i} className="skeleton" style={{ flex: '1 1 150px', height: 110, borderRadius: 16 }} />
          ))}
        </div>
      ) : (
        <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
          {stockData.map(q => <StockCard key={q.symbol} quote={q} />)}
        </div>
      )}
    </section>
  );
});
