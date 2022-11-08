import { ENV } from 'common/enums/enums';
import { AuthApi } from './auth-api/auth-api.service';
import { Http } from './http/http.service';
import { attachAuthTokenInterceptor } from './http/interceptors/attach-auth-token-interceptor';
import { StorageService } from './storage/local-storage.service';
import { TokensStorageService } from './storage/tokens-storage.service';

const storageService = new StorageService();
const tokensStorageService = new TokensStorageService(storageService);

const http = new Http([attachAuthTokenInterceptor], []);

const authApi = new AuthApi({
  apiPrefix: ENV.API_PATH,
  http,
});

export {
  storageService,
  tokensStorageService,
  authApi,
};
