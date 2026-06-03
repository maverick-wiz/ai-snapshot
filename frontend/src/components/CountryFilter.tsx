// CountryFilter — Top 25 GDP dropdown. AISNP-34 · Owner: PIXEL
import { useState, useEffect } from 'react';
import { fetchCountries } from '../api/client';
import type { Country } from '../types';

interface Props { selected: string; onChange: (iso2: string) => void; }

export function CountryFilter({ selected, onChange }: Props) {
  const [countries, setCountries] = useState<Country[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCountries().then(c => { setCountries(c); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
      <label style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 500 }}>
        🌍 Country
      </label>
      <select
        value={selected}
        onChange={e => onChange(e.target.value)}
        disabled={loading}
        aria-label="Select country for news filter"
        style={{
          background: 'rgba(15,17,36,0.8)', color: 'var(--text-primary)',
          border: '1px solid var(--border)', borderRadius: 10,
          padding: '8px 14px', fontSize: '0.85rem', cursor: 'pointer',
          backdropFilter: 'blur(10px)', outline: 'none',
          appearance: 'none', minWidth: 180,
        }}
      >
        {countries.map(c => (
          <option key={c.iso2} value={c.iso2}>{c.flag} {c.name}</option>
        ))}
      </select>
    </div>
  );
}
