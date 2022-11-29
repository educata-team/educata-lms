import { configureStore } from '@reduxjs/toolkit';

import {
  authApi,
  userApi,
} from 'services/services';
import { rootReducer } from './root-reducer';
import storage from 'redux-persist/lib/storage';
import { persistReducer, persistStore } from 'redux-persist';

const extraArgument = {
  authApi,
  userApi,
};

const persistConfig = {
  key: 'root',
  storage,
  whitelist: ['auth'],
};

const persistedReducer = persistReducer(persistConfig, rootReducer);

const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) => {
    return getDefaultMiddleware({
      thunk: { extraArgument },
      serializableCheck: false,
    });
  },
});

const persistor = persistStore(store);

type storeType = typeof store;

export { extraArgument, store, persistor, type storeType };
