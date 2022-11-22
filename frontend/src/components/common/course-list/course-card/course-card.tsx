import styles from '../style.module.scss';
import React from 'react';
import { FC } from '../../../../common/types/react/fc.type';

interface Props{
  banner: string,
  name: string,
  author: string,
}

export const CourseCard:FC<Props> = ({
  banner,
  name,
  author,
                                     }) => {
  const CourseClick = ():void => {
    alert('you clicked on course');
  };

  return (
    <div className={styles['course-card']} onClick={CourseClick}>
      <div className={styles['banner']}>{banner}</div>
      <div className={styles['course-name']}>{name}</div>
      <div className={styles['course-author']}>{author}</div>
    </div>
  );
};
