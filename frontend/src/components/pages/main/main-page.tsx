import styles from './styles.module.scss';
import React from 'react';
import { FC } from 'common/types/types';
import { Header } from '../../common/header/header';
import { Footer } from '../../common/footer/footer';
import { FilterBar } from '../../common/filter-bar/filter-bar';
import { CourseList } from '../../common/course-list/course-list';

export const MainPage:FC = () => {
  const courses = [{ banner: 'tut bude link na baner', name: 'Nazva kursu', author: 'Author Kursu' }];

  return (
    <div className={styles['main-page']}>
      <Header/>
      <FilterBar/>
      <CourseList courses={courses}/>
      <Footer/>
    </div>
  );
};
