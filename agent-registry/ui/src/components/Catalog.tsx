import { useEffect, useState } from 'react';
import { listResources } from '../api';
import type { BaseResource, ResourceType } from '../types';
import { ResourceCard } from './ResourceCard';

const TABS: { id: ResourceType; label: string }[] = [
  { id: 'agents', label: 'Agents' },
  { id: 'mcp-servers', label: 'MCP Servers' },
  { id: 'skills', label: 'Skills' },
];

export function Catalog() {
  const [tab, setTab] = useState<ResourceType>('agents');
  const [query, setQuery] = useState('');
  const [items, setItems] = useState<BaseResource[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError(null);
    listResources<BaseResource>(tab, { q: query || undefined })
      .then((page) => {
        if (active) setItems(page.items);
      })
      .catch((e) => {
        if (active) setError(String(e.message ?? e));
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [tab, query]);

  return (
    <section className="catalog">
      <nav className="tabs">
        {TABS.map((t) => (
          <button
            key={t.id}
            className={`tab ${tab === t.id ? 'tab--active' : ''}`}
            onClick={() => setTab(t.id)}
          >
            {t.label}
          </button>
        ))}
      </nav>

      <input
        className="search"
        type="search"
        placeholder="Search the catalog…"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      {error && <p className="error">{error}</p>}
      {loading && <p className="muted">Loading…</p>}

      {!loading && !error && items.length === 0 && (
        <p className="muted">No results.</p>
      )}

      <div className="grid">
        {items.map((r) => (
          <ResourceCard key={r.id} resource={r} />
        ))}
      </div>
    </section>
  );
}
