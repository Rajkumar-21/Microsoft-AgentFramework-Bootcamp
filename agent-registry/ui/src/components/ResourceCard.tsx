import type { BaseResource, Agent, MCPServer, Skill } from '../types';

const KIND_LABEL: Record<string, string> = {
  agent: 'Agent',
  mcp_server: 'MCP Server',
  skill: 'Skill',
};

export function ResourceCard({ resource }: { resource: BaseResource }) {
  return (
    <article className="card">
      <header className="card__head">
        <span className={`badge badge--${resource.kind}`}>
          {KIND_LABEL[resource.kind]}
        </span>
        <span className="card__version">v{resource.version}</span>
      </header>
      <h3 className="card__title">{resource.name}</h3>
      <p className="card__summary">{resource.summary}</p>

      <Details resource={resource} />

      <div className="card__tags">
        {resource.tags.map((t) => (
          <span key={t} className="tag">
            {t}
          </span>
        ))}
      </div>
      <footer className="card__foot">
        <span>by {resource.publisher.name}</span>
        <span className={`vis vis--${resource.visibility}`}>
          {resource.visibility}
        </span>
      </footer>
    </article>
  );
}

function Details({ resource }: { resource: BaseResource }) {
  if (resource.kind === 'agent') {
    const a = resource as Agent;
    return (
      <dl className="meta">
        <dt>Protocol</dt>
        <dd>{a.protocol}</dd>
        <dt>Auth</dt>
        <dd>{a.auth}</dd>
        <dt>Endpoint</dt>
        <dd className="mono">{a.endpoint}</dd>
      </dl>
    );
  }
  if (resource.kind === 'mcp_server') {
    const s = resource as MCPServer;
    return (
      <dl className="meta">
        <dt>Transport</dt>
        <dd>{s.transport}</dd>
        <dt>Tools</dt>
        <dd>{s.tools.map((t) => t.name).join(', ') || '—'}</dd>
        <dt>URL</dt>
        <dd className="mono">{s.url}</dd>
      </dl>
    );
  }
  const sk = resource as Skill;
  return (
    <dl className="meta">
      <dt>Kind</dt>
      <dd>{sk.skill_kind}</dd>
    </dl>
  );
}
