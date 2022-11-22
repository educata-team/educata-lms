import styles from './styles.module.scss';
import React from 'react';
import { FC } from '../../../common/types/react/fc.type';

export const FilterBar: FC = () => {
  return (
    <div className={styles['filter']}>
      <ul>
        <li>Home</li>
        <li>In Progress</li>
        <li>Completed</li>
      </ul>
    </div>
  );
};
