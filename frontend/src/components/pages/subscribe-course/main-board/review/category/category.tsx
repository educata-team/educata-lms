import styles from '../../styles.module.scss';
import React from 'react';
import { FC } from '../../../../../../common/types/react/fc.type';

export const Category:FC = () => {

  return (
   <ul className={styles['category']}>
     <li>Огляд</li>
     <li>Комп’ютерні науки</li>
     <li>Розробка програмного забезпечення</li>
   </ul>
  );
};
