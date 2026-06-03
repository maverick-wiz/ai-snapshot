// App root — stock state completely isolated from news state.
// AISNP-31 · Owner: PIXEL
import { useState } from 'react';
import './styles/globals.css';
import { Header } from './components/Header';
import { StockPanel } from './components/StockPanel';
import { NewsPanel } from './components/NewsPanel';

export default function App() {
  // selectedCountry drives useNews only — stock polling is independent
  const [selectedCountry, setSelectedCountry] = useState('US');

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Header />
      <main style={{ flex: 1 }}>
        {/* StockPanel uses its own isolated useStocks hook — never rerenders on news changes */}
        <StockPanel />
        <div style={{ margin: '0 32px', borderTop: '1px solid var(--border)', marginTop: 24 }} />
        {/* NewsPanel only rerenders when selectedCountry changes */}
        <NewsPanel country={selectedCountry} onCountryChange={setSelectedCountry} />
      </main>
      <footer style={{ padding: '16px 32px', borderTop: '1px solid var(--border)',
                       fontSize: '0.72rem', color: 'var(--text-muted)',
                       display: 'flex', justifyContent: 'space-between' }}>
        <span>AI-SNAPSHOT v1.0 · Data: Google News RSS + Yahoo Finance (yfinance)</span>
        <span>Stock prices auto-refresh every 5s · News cache: 5 min</span>
      </footer>
    </div>
  );
}
