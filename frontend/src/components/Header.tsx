// Header — logo, tagline, live clock. AISNP-33 · Owner: PIXEL
import { useState, useEffect } from 'react';

export function Header() {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const id = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(id);
  }, []);

  const fmt = time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

  return (
    <header style={{
      background: 'rgba(15,17,36,0.8)',
      backdropFilter: 'blur(20px)',
      borderBottom: '1px solid rgba(99,102,241,0.2)',
      padding: '16px 32px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      position: 'sticky', top: 0, zIndex: 100,
    }}>
      <div>
        <h1 style={{
          margin: 0, fontSize: '1.5rem', fontWeight: 700,
          background: 'linear-gradient(135deg, #818cf8, #a78bfa)',
          WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
          letterSpacing: '-0.02em',
        }}>
          ⚡ AI-SNAPSHOT
        </h1>
        <p style={{ margin: 0, fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: 2 }}>
          Real-time AI &amp; Financial Intelligence
        </p>
      </div>
      <div style={{ fontVariantNumeric: 'tabular-nums', fontSize: '0.9rem',
                    color: 'var(--text-secondary)', fontFamily: 'monospace' }}>
        🕐 {fmt}
      </div>
    </header>
  );
}
