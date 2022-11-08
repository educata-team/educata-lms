import React from 'react';
import { FC } from '../../../../common/types/react/fc.type';
interface Props{
  goToPage(pageNumber: number): void;
  setInfoFromSecondPage(username: string, first_name: string, last_name: string): void;
}

const SecondPage:FC<Props> = ({
  goToPage,
  setInfoFromSecondPage
                              }) => {
  return (
    <div>

    </div>
  );
};

export default SecondPage;
