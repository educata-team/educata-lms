import styles from '../styles.module.scss';
import React from 'react';
import { FC } from '../../../../../common/types/react/fc.type';
import { Category } from './category/category';
import { Info } from './info/info';
import { Subscribe } from './subscribe/subscribe';

export const Review:FC = () => {
  return (
    <div className={styles['review']}>
      <Category/>
      <Info name={'Programming for Everybody'} author={'Charles Russell Severance'} rating={4.4} number_of_grades={100}/>
      <Subscribe number_of_subscribers={234}/>
    </div>
  );
};
