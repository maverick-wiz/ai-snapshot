// LoadingSkeleton — shimmer placeholders. AISNP-36 · Owner: PIXEL
export function LoadingSkeleton({ count = 6 }: { count?: number }) {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: 20 }}>
      {[...Array(count)].map((_, i) => (
        <div key={i} className="glass-card" style={{ padding: 20, height: 200 }}>
          <div className="skeleton" style={{ width: '60%', height: 14, marginBottom: 10 }} />
          <div className="skeleton" style={{ width: '40%', height: 10, marginBottom: 16 }} />
          <div className="skeleton" style={{ width: '100%', height: 80, borderRadius: 8, marginBottom: 12 }} />
          <div className="skeleton" style={{ width: '80%', height: 10 }} />
        </div>
      ))}
    </div>
  );
}
