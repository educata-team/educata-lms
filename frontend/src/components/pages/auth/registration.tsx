import { AppRoute } from 'common/enums/enums';
import { FC } from 'common/types/types';
import { useAppDispatch, useNavigate } from 'hooks/hooks';
import React, { useCallback, useState } from 'react';
import { useForm } from 'react-hook-form';
import { authActions } from 'store/actions';
import { FormValues } from './common/form-values';
import { FirstPage } from './components/first-page';
import { SecondPage } from './components/second-page';

import styles from './styles.module.scss';

export const Registration: FC = () => {
  const { register, watch, handleSubmit } = useForm<FormValues>();
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const [page, setPage] = useState(1);

  const handlePageSwitch = useCallback((pageNumber: number) => {
    setPage(pageNumber);
  }, [setPage]);
  return (
    <div className={styles['form-wrapper']}>
      <form onSubmit={handleSubmit(async (data) => {
        await dispatch(authActions.signUp(data))
        .unwrap()
        .then(() => navigate(AppRoute.SIGN_IN));
      })}>
        {page === 1 && <FirstPage onPageSwitch={handlePageSwitch} register={register} watch={watch} />}
        {page === 2 && <SecondPage onPageSwitch={handlePageSwitch} register={register} />}
      </form>
    </div>
  );
};
