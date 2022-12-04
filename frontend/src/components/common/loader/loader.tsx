import clsx from 'clsx';
import { IconColor } from 'common/enums/enums';
import { FC } from 'common/types/types';

import styles from './styles.module.scss';

type Props = {
  className?: string;
  size?: number;
  color?: IconColor | string;
};

export const Loader: FC<Props> = ({ className, size = 60, color = IconColor.BLACK }) => {

  return (
    <div className={clsx(className, styles['loader-wrapper'])} style={{ '--loader-size': `${size}px`, '--loader-color': color } as React.CSSProperties}>
      <span className={styles['loader']}></span>
    </div>
  );
};
