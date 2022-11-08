import { StorageKeys } from 'common/enums/enums';
import { TokenPair } from 'common/types/types';
import { StorageService } from './local-storage.service';

export class TokensStorageService {
  constructor(private storageService: StorageService) {}

  public saveTokens({ access, refresh }: Partial<TokenPair>): void {
    if (access) {
      this.storageService.save(StorageKeys.ACCESS_TOKEN, access);
    }
    if (refresh) {
      this.storageService.save(StorageKeys.REFRESH_TOKEN, refresh);
    }
  }

  public clearTokens(): void {
    this.storageService.remove(StorageKeys.ACCESS_TOKEN);
    this.storageService.remove(StorageKeys.REFRESH_TOKEN);
  }

  public getTokens(): { [K in keyof TokenPair]: TokenPair[K] | null } {
    return {
      access: this.storageService.retrieve(StorageKeys.ACCESS_TOKEN),
      refresh: this.storageService.retrieve(StorageKeys.REFRESH_TOKEN),
    };
  }
}
