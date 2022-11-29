import styles from '../../styles.module.scss';
import React from 'react';
import { FC } from '../../../../../../common/types/react/fc.type';
import { Rating } from './rating';

interface Props{
  name: string;
  rating: number;
  number_of_grades: number;
  author: string;
}

export const Info:FC<Props> = ({
  name,
  rating,
  number_of_grades,
  author,
                               }) => {

  return (
    <div className={styles['info']}>
      <div className={styles['name']}>{name}</div>
      <div className={styles['rating-block']}>
        <Rating rating={rating}/>
        <div>{number_of_grades + ' оцінок'}</div>
      </div>
      <div className={styles['author']}>{author}</div>
    </div>
  );
};
