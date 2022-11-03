import React from 'react';
import ReactDOM from 'react-dom/client';
import { App } from 'components/app/app';
import { Provider } from 'react-redux';
import { persistor, store } from './store/store';

import 'assets/styles/styles.scss';
import { PersistGate } from 'redux-persist/integration/react';
import { BrowserRouter } from 'react-router-dom';

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);

root.render(
  <React.StrictMode>
    <Provider store={store}>
      <PersistGate persistor={persistor}>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </PersistGate>
    </Provider>
  </React.StrictMode>,
);
