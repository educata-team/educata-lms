import styles from './styles.module.scss';
import React from 'react';
import { FC } from '../../../../common/types/react/fc.type';

interface Props{
  about_course: string;
  what_learn: Array<string>;
  skills: Array<string>;
}

export const AboutCourse:FC<Props> = ({
  about_course,
  what_learn,
  skills,
                                      }) => {
  return (
    <div className={styles['about-course-wrapper']}>
      <div className={styles['about-course']}>
        <div className={styles['description']}>
          <h2>Про цей курс</h2>
          <p>{about_course}</p>
        </div>
        <div className={styles['objectives']}>
          <label>ЧОГО ВИ НАВЧИТЕСЯ</label>
          <ul>
            {
              what_learn.map((item) => <li>{item}</li>)
            }
          </ul>
        </div>
        <div className={styles['objectives']}>
          <label>НАВИЧКИ, ЯКІ ВИ ЗДОБУДЕТЕ</label>
          <ul>
            {
              skills.map((item) => <li>{item}</li>)
            }
          </ul>
        </div>
      </div>
    </div>
  );
};
