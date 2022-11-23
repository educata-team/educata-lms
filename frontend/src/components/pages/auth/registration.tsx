import { FC } from 'common/types/types';
import React, { useCallback, useState } from 'react';
import { useForm } from 'react-hook-form';
import { FormValues } from './common/form-values';
import { FirstPage } from './components/first-page';
import { SecondPage } from './components/second-page';

import styles from './styles.module.scss';

export const Registration: FC = () => {
  const { register, watch } = useForm<FormValues>();

  const [page, setPage] = useState(1);

  const handlePageSwitch = useCallback((pageNumber: number) => {
    setPage(pageNumber);
  }, [setPage]);

  const handleFormSubmit = useCallback(async () => {
    // fetch('http://localhost:8000/api/v1/users/login/')
    console.warn('sent request');
  }, []);

  return (
    <div className={styles['form-wrapper']}>
      {page === 1 && <FirstPage onPageSwitch={handlePageSwitch} register={register} watch={watch} />}
      {page === 2 && <SecondPage onPageSwitch={handlePageSwitch} onSubmit={handleFormSubmit} register={register} />}
    </div>
  );
};
