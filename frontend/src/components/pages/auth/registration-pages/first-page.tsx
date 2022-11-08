import React, { useState } from 'react';
import { FC } from '../../../../common/types/react/fc.type';
import { Button, Grid, Paper, TextField } from '@mui/material';

interface Props{
  goToPage(pageNumber: number): void;
  setInfoFromFirstPage(email: string | undefined, password: string | undefined): void;
}

const FirstPage:FC<Props> = ({
  goToPage,
  setInfoFromFirstPage,
                             }) => {
  const [email, setEmail] = useState<string>();
  const [password, setPassword] = useState<string>();
  const [repeat, setRepeat] = useState<string>();

  return (
    <Grid>
      <Paper elevation={10} style = { { padding :20,height: '60vh',width:380, margin:'20px auto', display: 'flex', flexDirection: 'column', justifyContent: 'space-around' } }>
        <Grid style={ { textAlign: 'center' } }>
          <h2>Sign In</h2>
        </Grid>
        <TextField label="Email" placeholder="Enter email" type="email"  required onChange={(event: React.ChangeEvent<HTMLInputElement>):void => {setEmail(event.target.value);}}/>
        <TextField label="Password" placeholder="Enter password" type="password"  required onChange={(event: React.ChangeEvent<HTMLInputElement>):void => {setPassword(event.target.value);}}/>
        <TextField label="Password" placeholder="Enter password" type="password"  required onChange={(event: React.ChangeEvent<HTMLInputElement>):void => {setRepeat(event.target.value);}}/>

        <Button type="submit" variant="contained" style={ { margin:'8px 0' } }  onClick={() => {if (password === repeat){setInfoFromFirstPage(email, password); goToPage(2);}}}>Next</Button>

      </Paper>
    </Grid>
  );
};

export default FirstPage;
