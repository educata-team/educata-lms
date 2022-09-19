import { FC } from 'common/types/types';

import styles from './styles.module.scss';

export const App: FC = () => {
  return (
    <div className={styles['app']}>
      <header className={styles['app-header']}>
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className={styles['app-link']}
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
};
