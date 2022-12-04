import { createReducer, isAnyOf } from '@reduxjs/toolkit';
import { DataStatus } from 'common/enums/enums';
import { UserInfoResponseDto } from 'common/types/types';

import {
  signOut,
  refreshTokens,
  signIn,
  signUp,
} from './actions';

type State = {
  dataStatus: DataStatus;
  user: UserInfoResponseDto | null;
  error: string | undefined;
};

const initialState: State = {
  dataStatus: DataStatus.IDLE,
  user: null,
  error: undefined,
};

const reducer = createReducer(initialState, (builder) => {
  builder.addCase(signIn.fulfilled, (state, { payload }) => {
    state.user = payload;
  });
  builder.addMatcher(
    isAnyOf(signOut.rejected, signOut.fulfilled),
    (state) => {
      state.user = null;
    },
  );
  builder.addMatcher(
    isAnyOf(signUp.pending, signIn.pending, refreshTokens.pending, signOut.pending),
    (state) => {
      state.dataStatus = DataStatus.PENDING;
      state.error = undefined;
    },
  );
  builder.addMatcher(
    isAnyOf(signUp.fulfilled, signIn.fulfilled, refreshTokens.fulfilled, signOut.fulfilled),
    (state) => {
      state.dataStatus = DataStatus.FULFILLED;
      state.error = undefined;
    },
  );
  builder.addMatcher(
    isAnyOf(signUp.rejected, signIn.rejected, refreshTokens.rejected, signOut.rejected),
    (state, { error }) => {
      state.dataStatus = DataStatus.REJECTED;
      state.error = error.message;
    },
  );
});

export { reducer };
