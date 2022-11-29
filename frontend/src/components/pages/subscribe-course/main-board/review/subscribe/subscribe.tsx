import styles from '../../styles.module.scss';
import React from 'react';
import { FC } from '../../../../../../common/types/react/fc.type';

interface Props{
  number_of_subscribers: number;
}

export const Subscribe:FC<Props> = ({
  number_of_subscribers,
                                    }) => {

  return (
    <div className={styles['subscribe']}>
      <button>Запишіться безкоштовно</button>
      <div>{`${number_of_subscribers} уже записалися`}</div>
    </div>
  );
};
