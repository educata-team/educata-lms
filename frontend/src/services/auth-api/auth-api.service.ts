import { ApiPath, UsersApiPath, ContentType, HttpMethod } from 'common/enums/enums';
import {
  RefreshTokenRequestDto,
  RefreshTokenResponseDto,
  SignInRequestDto,
  SignInResponseDto,
  SignUpRequestDto,
  SignUpResponseDto,
} from 'common/types/types';
import { Http } from '../http/http.service';

type Constructor = {
  http: Http;
  apiPrefix: string;
};

class AuthApi {
  #http: Http;
  #apiPrefix: string;

  constructor({ http, apiPrefix }: Constructor) {
    this.#http = http;
    this.#apiPrefix = apiPrefix;
  }

  public signUp(payload: SignUpRequestDto): Promise<SignUpResponseDto> {
    return this.#http.load({
      url: `${this.#apiPrefix}${ApiPath.USERS}${UsersApiPath.SIGN_UP}`,
      options: {
        method: HttpMethod.POST,
        contentType: ContentType.JSON,
        payload: JSON.stringify(payload),
      },
      preInterceptors: [],
      postInterceptors: [],
    });
  }

  public signIn(payload: SignInRequestDto): Promise<SignInResponseDto> {
    return this.#http.load({
      url: `${this.#apiPrefix}${ApiPath.USERS}${UsersApiPath.SIGN_IN}`,
      options: {
        method: HttpMethod.POST,
        contentType: ContentType.JSON,
        payload: JSON.stringify(payload),
      },
      preInterceptors: [],
      postInterceptors: [],
    });
  }

  public refreshTokens(payload: RefreshTokenRequestDto): Promise<RefreshTokenResponseDto> {
    return this.#http.load({
      url: `${this.#apiPrefix}${ApiPath.USERS}${UsersApiPath.REFRESH_TOKENS}`,
      options: {
        method: HttpMethod.POST,
        contentType: ContentType.JSON,
        payload: JSON.stringify(payload),
      },
      preInterceptors: [],
      postInterceptors: [],
    });
  }

  public signOut(): Promise<void> {
    return this.#http.load({
      url: `${this.#apiPrefix}${ApiPath.USERS}${UsersApiPath.SIGN_OUT}`,
      options: {
        method: HttpMethod.POST,
      },
    });
  }
}

export { AuthApi };
