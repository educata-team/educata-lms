import { StorageService } from './storage/local-storage.service';
import { TokensStorageService } from './storage/tokens-storage.service';

const storageService = new StorageService();
const tokensStorageService = new TokensStorageService(storageService);

export {
  storageService,
  tokensStorageService,
};
