import styles from './styles.module.scss';
import React from 'react';
import { FC } from '../../../common/types/react/fc.type';
import { NavigationPanel } from './navigation-panel/navigation-panel';

export const CoursePage:FC = () => {

  const navigation = [{ unitName: 'Introduction', lessonsName: ['Lesson 1', 'Lesson 2'] }];

  return (
    <div className={styles['course-page-wrapper']}>
      <div className={styles['course-page']}>
        <NavigationPanel navigation={navigation}/>
      </div>
    </div>
  );
};
