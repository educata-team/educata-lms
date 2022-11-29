import { ApiPath, HttpMethod, UsersApiPath } from 'common/enums/enums';
import { UserInfoResponseDto } from 'common/types/types';
import { Http } from 'services/http/http.service';

type Constructor = {
  http: Http;
  apiPrefix: string;
};

class UserApi {
  #http: Http;
  #apiPrefix: string;

  constructor({ http, apiPrefix }: Constructor) {
    this.#http = http;
    this.#apiPrefix = apiPrefix;
  }

  public getUserById(userId: string): Promise<UserInfoResponseDto> {
    return this.#http.load({
      url: `${this.#apiPrefix}${ApiPath.USERS}${UsersApiPath.USER}/${userId}`,
      options: {
        method: HttpMethod.GET,
      },
      preInterceptors: [],
      postInterceptors: [],
    });
  }

}

export { UserApi };
