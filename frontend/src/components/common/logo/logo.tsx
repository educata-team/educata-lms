import { AppRoute } from 'common/enums/enums';
import { FC } from 'common/types/types';
import { Link } from '../link/link';
import logo from 'assets/img/logo.png';

type Props = {
  width?: number;
  className?: string;
};

export const Logo: FC<Props> = ({ width = 300, className }) => {
  return (
    <div className={className}>
      <Link to={AppRoute.ROOT}>
        <img src={logo} alt="Educata" width={width} />
      </Link>
    </div>
  );
};
