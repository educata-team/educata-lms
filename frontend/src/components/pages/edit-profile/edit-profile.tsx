import styles from './styles.module.scss';
import React from 'react';
import { FC } from '../../../common/types/react/fc.type';

export const EditProfile:FC = () => {
  return (
    <div className={styles['wrapper-edit-profile']}>
      <div className={styles['edit-profile']}>
        <div className={styles['head']}>
          Public profile
        </div>
        <hr/>
        <div className={styles['info-container']}>
          <div className={styles['user-info']}>
            <div className={styles['field-block']}>
              <h3>Username</h3>
              <input/>
            </div>
            <div className={styles['field-block']}>
              <h3>Name</h3>
              <input/>
            </div>
            <div className={styles['field-block']}>
              <h3>Lastname</h3>
              <input/>
            </div>
            <div className={styles['field-block']}>
              <h3>Bio</h3>
              <textarea placeholder="Tell us a little bit about yourself"/>
            </div>
            <div className={styles['update-button']}>
              <button>Update profile</button>
            </div>
          </div>
          <div className={styles['avatar']}>
            <h3>Profile picture</h3>
            <img src={'https://avatars.githubusercontent.com/u/105970858?s=400&u=5c12285397e61b283790bb9f6edb8c931f296f5d&v=4'} alt={'avatar'}/>
          </div>
        </div>
      </div>
    </div>
  );
};
