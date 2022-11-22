import styles from './style.module.scss';
import React from 'react';
import { FC } from '../../../common/types/react/fc.type';
import { CourseCard } from './course-card/course-card';

interface CourseProps{
  banner: string,
  name: string,
  author: string,
}

interface Props{
  courses: Array<CourseProps>,
}

export const CourseList:FC<Props> = ({
  courses,
                              }) => {

  return (
    <div className={styles['course-list']}>
      {courses.map((item:CourseProps) => <CourseCard banner={item.banner} name={item.name} author={item.author}/>)}
    </div>
  );
};
