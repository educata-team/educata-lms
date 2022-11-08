import { Button, Grid, Paper, TextField, Typography } from '@mui/material';
import { FC } from 'common/types/types';
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { AppRoute } from '../../../common/enums/enums';

export const Auth:FC = () => {
  const [login, setLogin] = useState<string>();
  const [password, setPassword] = useState<string>();

  const submitClick = async () : Promise<any> => {
    fetch('http://localhost:8000/api/v1/users/login/', {
      method: 'POST',
      body: JSON.stringify({ username: login, password: password }),
    }).then();
  };

  return (
      <Grid>
        <Paper elevation={10} style = { { padding :20,height: '60vh',width:380, margin:'20px auto', display: 'flex', flexDirection: 'column', justifyContent: 'space-around' } }>
          <Grid style={ { textAlign: 'center' } }>
            <h2>Sign In</h2>
          </Grid>
          <TextField label="Username" placeholder="Enter login"  required onChange={(event: React.ChangeEvent<HTMLInputElement>):void => {setLogin(event.target.value);}}/>
          <TextField label="Password" placeholder="Enter password" type="password"  required onChange={(event: React.ChangeEvent<HTMLInputElement>):void => {setPassword(event.target.value);}}/>

          <Button type="submit" variant="contained" style={ { margin:'8px 0' } }  onClick={submitClick}>Sign in</Button>
          <Typography >
            <Link to={AppRoute.ROOT}>
              Forgot password ?
            </Link>
          </Typography>
          <Typography > Do you have an account ?
            <Link to={AppRoute.SIGN_UP} >
              Sign Up
            </Link>
          </Typography>
        </Paper>
      </Grid>
  );
};

