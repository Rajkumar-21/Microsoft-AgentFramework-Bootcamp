export type Visibility = 'public' | 'private';

export interface Publisher {
  id: string;
  name: string;
}

export interface BaseResource {
  id: string;
  kind: 'agent' | 'mcp_server' | 'skill';
  name: string;
  summary: string;
  description: string;
  version: string;
  tags: string[];
  visibility: Visibility;
  publisher: Publisher;
  updated_at: string;
}

export interface Agent extends BaseResource {
  kind: 'agent';
  endpoint: string;
  protocol: string;
  auth: string;
  scopes: string[];
}

export interface MCPServer extends BaseResource {
  kind: 'mcp_server';
  url: string;
  transport: string;
  auth: string;
  tools: { name: string; description: string }[];
}

export interface Skill extends BaseResource {
  kind: 'skill';
  skill_kind: string;
  spec: string;
}

export interface Page<T> {
  items: T[];
  count: number;
  total: number;
}

export type ResourceType = 'agents' | 'mcp-servers' | 'skills';
