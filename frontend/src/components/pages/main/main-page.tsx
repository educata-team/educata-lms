import styles from './styles.module.scss';
import React from 'react';
import { FC } from 'common/types/types';
import { Header } from '../../common/header/header';
import { Footer } from '../../common/footer/footer';
import { FilterBar } from '../../common/filter-bar/filter-bar';
import { CourseList } from '../../common/course-list/course-list';
import { useCallback, useState } from '../../../hooks/hooks';

export const MainPage:FC = () => {
  const courses = [{ banner: 'tut bude link na baner', name: 'Nazva kursu', author: 'Author Kursu' }];
  const [select, setSelect] = useState<string>('home');
  const selectCourse = useCallback((select: string):void => setSelect(select), [setSelect]);

  return (
    <div className={styles['main-page']}>
      <Header/>
      <FilterBar select={select} setSelect={selectCourse}/>
      <CourseList courses={courses}/>
      <Footer/>
    </div>
  );
};
