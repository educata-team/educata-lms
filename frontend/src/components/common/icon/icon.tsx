import { FC } from 'common/types/types';
import { IconColor, IconName } from 'common/enums/enums';
import clsx from 'clsx';

import { ReactComponent as Bell } from 'assets/img/icons/bell.svg';
import { ReactComponent as Home } from 'assets/img/icons/home.svg';
import { ReactComponent as MagnifyingGlass } from 'assets/img/icons/magnifying-glass.svg';
import { ReactComponent as User } from 'assets/img/icons/user.svg';

interface Props {
  name: IconName;
  color: IconColor | string;
  size: number;
  className?: string;
}

export const Icon: FC<Props> = ({
  name,
  color = '#000',
  size = 20,
  className,
}) => {
  const iconProps = {
    className: clsx(className),
    width: size,
    height: size,
  };
  const iconStyle = {
    fill: color,
  };

  switch (name) {
    case IconName.BELL: {
      return <Bell {...iconProps} style={{ ...iconStyle }} />;
    }
    
    case IconName.HOME: {
      return <Home {...iconProps} style={{ ...iconStyle }} />;
    }
    
    case IconName.MAGNIFYING_GLASS: {
      return <MagnifyingGlass {...iconProps} style={{ ...iconStyle }} />;
    }
    
    case IconName.USER: {
      return <User {...iconProps} style={{ ...iconStyle }} />;
    }
  }
};
