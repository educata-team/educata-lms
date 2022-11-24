import styles from './styles.module.scss';
import React from 'react';
import { FC } from '../../../common/types/react/fc.type';

interface Props{
  select: string;
  setSelect(select: string):void;
}

export const FilterBar: FC<Props> = ({
  select,
  setSelect,
                                     }) => {
  return (
    <div className={styles['filter']}>
      <ul>
        <li className={ select === 'home'? styles['select'] : '' } onClick={():void => setSelect('home')}>Home</li>
        <li className={ select === 'in-progress'? styles['select'] : '' } onClick={():void => setSelect('in-progress')}>In Progress</li>
        <li className={ select === 'completed'? styles['select'] : '' } onClick={():void => setSelect('completed')}>Completed</li>
      </ul>
    </div>
  );
};
