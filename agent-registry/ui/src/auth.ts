// Auth helpers — MSAL for Entra mode, static token for dev mode.
import {
  PublicClientApplication,
  type Configuration,
} from '@azure/msal-browser';

export const AUTH_MODE = import.meta.env.VITE_AUTH_MODE ?? 'dev';
export const API_SCOPE = import.meta.env.VITE_API_SCOPE ?? '';

const msalConfig: Configuration = {
  auth: {
    clientId: import.meta.env.VITE_ENTRA_CLIENT_ID ?? '',
    authority: `https://login.microsoftonline.com/${
      import.meta.env.VITE_ENTRA_TENANT_ID ?? 'common'
    }`,
    redirectUri: window.location.origin,
  },
  cache: {
    cacheLocation: 'sessionStorage',
  },
};

export const msalInstance = new PublicClientApplication(msalConfig);

/** Acquire a bearer token for the registry API. */
export async function getAccessToken(): Promise<string> {
  if (AUTH_MODE === 'dev') {
    // Matches the API's dev auth: bare "dev" grants all scopes.
    return 'dev';
  }
  const accounts = msalInstance.getAllAccounts();
  const account = accounts[0];
  if (!account) {
    throw new Error('Not signed in.');
  }
  const result = await msalInstance.acquireTokenSilent({
    scopes: [API_SCOPE],
    account,
  });
  return result.accessToken;
}
