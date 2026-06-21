import { getAccessToken } from './auth';
import type { Page, ResourceType, BaseResource } from './types';

const BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';

async function authedFetch(path: string): Promise<Response> {
  const token = await getAccessToken();
  return fetch(`${BASE_URL}${path}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function listResources<T extends BaseResource>(
  type: ResourceType,
  opts: { q?: string; tag?: string } = {}
): Promise<Page<T>> {
  const params = new URLSearchParams();
  if (opts.q) params.set('q', opts.q);
  if (opts.tag) params.set('tag', opts.tag);
  const qs = params.toString();
  const resp = await authedFetch(`/${type}${qs ? `?${qs}` : ''}`);
  if (!resp.ok) {
    throw new Error(`Failed to load ${type}: ${resp.status}`);
  }
  return resp.json();
}

export interface Me {
  id: string;
  name: string;
  tenant_id: string;
  scopes: string[];
  is_app: boolean;
}

export async function whoami(): Promise<Me> {
  const resp = await authedFetch('/me');
  if (!resp.ok) throw new Error('Not authenticated.');
  return resp.json();
}
