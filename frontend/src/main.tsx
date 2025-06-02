import React from 'react';
import ReactDOM from 'react-dom/client';
import { MantineProvider } from '@mantine/core';
import '@mantine/core/styles.css';
import '@mantine/dropzone/styles.css';
import App from './App.tsx';
import ErrorBoundary from './components/ErrorBoundary';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ErrorBoundary>
      <MantineProvider>
        <App />
      </MantineProvider>
    </ErrorBoundary>
  </React.StrictMode>
);
