import { AppRoute, IconColor, IconName } from 'common/enums/enums';
import { FC } from 'common/types/types';
import { Icon } from 'components/common/icon/icon';
import { Route, Routes } from 'react-router-dom';
import { ScrollToTop } from './scroll-to-top';

import styles from './styles.module.scss';
import { Auth } from '../pages/auth/auth';
import { Registration } from '../pages/auth/registration';

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
          <Route path={AppRoute.ROOT} element={<></> /* Insert homepage component here instead of <></> */} />
          <Route path={AppRoute.SIGN_IN} element={<Auth />} />
          <Route path={AppRoute.SIGN_UP} element={<Registration />} />
          {/* Insert other routes here */}
          <Route path={AppRoute.ANY} element={<></> /* Insert 404 page component here */} />
        </Routes>
      </div>
    </>
  );
};
