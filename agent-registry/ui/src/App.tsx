import { useEffect, useState } from 'react';
import { useMsal, useIsAuthenticated } from '@azure/msal-react';
import { AUTH_MODE, API_SCOPE } from './auth';
import { whoami, type Me } from './api';
import { Catalog } from './components/Catalog';

export function App() {
  return (
    <div className="app">
      <Header />
      <main>
        <Catalog />
      </main>
      <footer className="page-foot">
        Agent Registry &amp; Marketplace · Microsoft Agent Framework Bootcamp
      </footer>
    </div>
  );
}

function Header() {
  const isDev = AUTH_MODE === 'dev';
  const isAuthenticated = useIsAuthenticated();
  const { instance } = useMsal();
  const [me, setMe] = useState<Me | null>(null);

  const signedIn = isDev || isAuthenticated;

  useEffect(() => {
    if (signedIn) {
      whoami().then(setMe).catch(() => setMe(null));
    }
  }, [signedIn]);

  return (
    <header className="topbar">
      <div className="brand">
        <span className="brand__mark">◆</span>
        <span className="brand__name">Agent Registry</span>
      </div>
      <div className="topbar__right">
        {me && (
          <span className="who">
            {me.name}
            <span className="who__scopes">{me.scopes.join(' · ')}</span>
          </span>
        )}
        {!isDev &&
          (isAuthenticated ? (
            <button
              className="btn"
              onClick={() => instance.logoutPopup()}
            >
              Sign out
            </button>
          ) : (
            <button
              className="btn btn--primary"
              onClick={() =>
                instance.loginPopup({ scopes: [API_SCOPE] })
              }
            >
              Sign in
            </button>
          ))}
        {isDev && <span className="dev-pill">dev mode</span>}
      </div>
    </header>
  );
}
