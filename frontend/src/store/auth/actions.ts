import { createAsyncThunk } from '@reduxjs/toolkit';
import { AsyncThunkConfig, RefreshTokenRequestDto, RefreshTokenResponseDto, SignInRequestDto, SignUpRequestDto, UserInfoResponseDto } from 'common/types/types';
import { tokensStorageService } from 'services/services';
import { ActionType } from './common';

const signUp = createAsyncThunk<void, SignUpRequestDto, AsyncThunkConfig>(
  ActionType.SIGN_UP,
  async (registerPayload, { extra }) => {
    const { authApi } = extra;

    await authApi.signUp(registerPayload);
  },
);

const signIn = createAsyncThunk<UserInfoResponseDto, SignInRequestDto, AsyncThunkConfig>(
  ActionType.SIGN_IN,
  async (signInPayload, { extra }) => {
    const { authApi, userApi } = extra;
    const { access, refresh, user_id } = await authApi.signIn(signInPayload);
    tokensStorageService.saveTokens({ access, refresh });
    const user = await userApi.getUserById(user_id);
    return user;
  },
);

let refreshPromise: Promise<RefreshTokenResponseDto> | null;
const refreshTokens = createAsyncThunk<RefreshTokenResponseDto, RefreshTokenRequestDto, AsyncThunkConfig>(
  ActionType.REFRESH_TOKENS,
  async (refreshPayload, { extra }) => {
    const { authApi } = extra;
    let newTokens;
    if (refreshPromise) {
      newTokens = await refreshPromise;
    } else {
      refreshPromise = authApi.refreshTokens(refreshPayload);
      newTokens = await refreshPromise;
      refreshPromise = null;
    }
    tokensStorageService.saveTokens(newTokens.tokens);
    return newTokens;
  },
);

// in some cases there is a need only to sign out on client, while usually it's also needed to signOut on backend
const signOut = createAsyncThunk<void, { hitApi: boolean; } | undefined, AsyncThunkConfig>(
  ActionType.SIGN_OUT,
  async ({ hitApi } = { hitApi: true }, { extra }) => {
    const { authApi } = extra;
    try {
      if (hitApi) {
        await authApi.signOut();
      }
    } finally {
      tokensStorageService.clearTokens();
    }
  },
);

export {
  signUp,
  signIn,
  refreshTokens,
  signOut,
};
