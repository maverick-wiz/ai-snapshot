// LiveIndicator — pulsing green dot. AISNP-42 · Owner: PIXEL
interface Props { active?: boolean; intervalSecs?: number; }
export function LiveIndicator({ active = true, intervalSecs = 5 }: Props) {
  return (
    <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6,
                   fontSize: '0.72rem', color: 'var(--text-muted)' }}>
      <span className="pulse-dot"
        style={{ background: active ? 'var(--gain-green)' : '#64748b' }} />
      {active ? `LIVE · ${intervalSecs}s` : 'PAUSED'}
    </span>
  );
}
