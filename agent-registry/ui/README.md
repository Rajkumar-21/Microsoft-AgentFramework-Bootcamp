# Agent Registry — Marketplace UI

A small React (Vite) front-end for browsing and searching the registry catalog
of **Agents**, **MCP servers**, and **Skills**. Signs in with Microsoft Entra ID
via MSAL, or runs in a keyless **dev mode** against the local API.

## Run locally (dev mode)

```bash
cd agent-registry/ui
npm install
copy .env.example .env      # Windows (use cp on macOS/Linux)
npm run dev
```

Open <http://localhost:5173>. In dev mode the UI sends `Authorization: Bearer dev`
so it works against the API running in `REGISTRY_AUTH_MODE=dev`.

## Entra ID mode

Set in `.env`:

```env
VITE_AUTH_MODE=entra
VITE_ENTRA_CLIENT_ID=<spa-app-registration-client-id>
VITE_ENTRA_TENANT_ID=<tenant-guid>
VITE_API_SCOPE=api://<registry-app-client-id>/Registry.Read
```

Register a SPA app in Entra ID, add a redirect URI for your origin
(`http://localhost:5173` in dev), and grant it the registry's `Registry.Read`
delegated scope. The UI acquires a token for that scope and calls the API.

## Build

```bash
npm run build      # outputs to dist/
npm run preview
```
