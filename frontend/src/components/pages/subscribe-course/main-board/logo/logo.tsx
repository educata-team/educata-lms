import React from 'react';
import styles from '../styles.module.scss';
import { FC } from '../../../../../common/types/react/fc.type';

interface Props{
  url: string;
}

export const Logo:FC<Props> = ({
  url,
                               }) => {
  return (
    <div className={styles['logo']}>
      <p>Пропонує</p>
      <img src={url} alt={'course logo'}/>
    </div>
  );
};
