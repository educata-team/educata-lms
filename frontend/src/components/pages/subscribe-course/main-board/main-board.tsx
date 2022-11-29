import styles from './styles.module.scss';
import { FC } from 'common/types/types';
import React from 'react';
import { Review } from './review/review';
  import { Logo } from './logo/logo';

export const MainBoard:FC = () => {
  return (
    <div className={styles['main-board-wrapper']}>
      <div className={styles['main-board']}>
        <Review/>
        <Logo/>
      </div>
    </div>
  );
};
