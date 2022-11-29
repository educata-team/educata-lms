import { AppRoute, IconColor, IconName } from 'common/enums/enums';
import { FC } from 'common/types/types';
import { Icon } from 'components/common/icon/icon';
import { Route, Routes } from 'react-router-dom';
import { ScrollToTop } from './scroll-to-top';

import styles from './styles.module.scss';
import { SubscribeCourse } from '../pages/subscribe-course/subscribe-course';

const scrollToTopQuerySelectors = [`.${styles['main-content']}`];

export const App: FC = () => {
  return (
    <>
      <ScrollToTop querySelectors={scrollToTopQuerySelectors} />
      {/* Remove this later */}
      <Icon name={IconName.HOME} size={20} color="green" />
      <Icon name={IconName.BELL} size={50} color={IconColor.PRIMARY_BLUE} />

      <div className={styles['main-content']}>
        <Routes>
          <Route path={AppRoute.SUBSCRIBE} element={<SubscribeCourse />} />
          <Route path={AppRoute.ROOT} element={<SubscribeCourse />} />
          {/* Insert other routes here */}
          <Route path={AppRoute.ANY} element={<></> /* Insert 404 page component here */} />
        </Routes>
      </div>
    </>
  );
};
