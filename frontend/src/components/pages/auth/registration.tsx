import { FC } from 'common/types/types';
import React, { useCallback, useState } from 'react';
import { FirstPage } from './registration-pages/first-page';
import { SecondPage } from './registration-pages/second-page';

export const Registration:FC = () => {
  const [username, setUsername] = useState<string>();
  const [first_name, setFirst_name] = useState<string>();
  const [last_name, setLast_name] = useState<string>();
  const [email, setEmail] = useState<string>();
  const [password, setPassword] = useState<string>();

  const [page, setPage] = useState(1);
  const goToPage = useCallback((pageNumber: number) => {setPage(pageNumber);}, [setPage]);
  const getInfoFromFirstPage = useCallback((email: string, password: string) => {setEmail(email); setPassword(password);}, [setEmail, setPassword]);
  const getInfoFromSecondPage = useCallback((username: string, first_name: string, last_name: string) => {setUsername(username); setFirst_name(first_name); setLast_name(last_name);}, [setUsername, setFirst_name, setLast_name]);
  const submitClick = useCallback(async () => {fetch('http://localhost:8000/api/v1/users/login/',{ method: 'POST', body: JSON.stringify({ username: username, first_name: first_name, last_name: last_name, email:email, password: password }) });}, [email, first_name, last_name, password, username]);

  switch (page) {
    case 1:
      return <FirstPage goToPage={goToPage} setInfoFromFirstPage={getInfoFromFirstPage}/>;
    case 2:
      return <SecondPage goToPage={goToPage} setInfoFromSecondPage={getInfoFromSecondPage} submitClick={submitClick}/>;
    default:
      return <FirstPage goToPage={goToPage} setInfoFromFirstPage={getInfoFromFirstPage}/>;
  }
};
