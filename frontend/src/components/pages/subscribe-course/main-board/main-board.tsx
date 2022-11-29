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
        <Logo url={'https://images-platform.99static.com//KlBLMX8dQrcq6hZGnxf5HSnG29I=/8x543:525x1060/fit-in/500x500/99designs-contests-attachments/123/123360/attachment_123360235'}/>
      </div>
    </div>
  );
};
