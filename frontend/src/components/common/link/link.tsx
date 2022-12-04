import { AppRoute } from 'common/enums/enums';
import { FC } from 'common/types/types';
import { NavLink } from 'react-router-dom';

type Props = {
  to: AppRoute;
  className?: string;
};

export const Link: FC<Props> = ({ children, to, className }) => {
  return (
    <NavLink className={className} to={to}>
      {children}
    </NavLink>
  );
};
