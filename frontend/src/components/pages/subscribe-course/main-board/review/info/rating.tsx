import styles from '../../styles.module.scss';
import React from 'react';
import { FC } from '../../../../../../common/types/react/fc.type';

interface Props{
  rating: number;
}

export const Rating:FC<Props> = ({
  rating,
                          }) => {
  let rating_star = '';

  for(let i = 0; i < Math.round(rating); i++){
    rating_star += '★';
  }

  return (
    <div className={styles['rating']}>
      <div>{rating_star}</div>
      <div>{rating}</div>
    </div>
  );
};
{/*★*/}
