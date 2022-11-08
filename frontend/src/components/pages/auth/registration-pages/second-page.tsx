import React, { useState } from 'react';
import { FC } from '../../../../common/types/react/fc.type';
import { Button, Grid, Paper, TextField } from '@mui/material';
interface Props{
  goToPage(pageNumber: number): void;
  setInfoFromSecondPage(username: string, first_name: string, last_name: string): void;
  submitClick():void;
}

export const SecondPage:FC<Props> = ({
  goToPage,
  setInfoFromSecondPage,
  submitClick,
                              }) => {
  const [username, setUsername] = useState<string>('');
  const [first_name, setFirst_name] = useState<string>('');
  const [last_name, setLast_name] = useState<string>('');

  return (
    <Grid>
      <Paper elevation={10} style = { { padding :20,height: '60vh',width:380, margin:'20px auto', display: 'flex', flexDirection: 'column', justifyContent: 'space-around' } }>
        <Grid style={ { textAlign: 'center' } }>
          <h2>Sign Up</h2>
        </Grid>
        <TextField label="Username" placeholder="Enter username" required onChange={(event: React.ChangeEvent<HTMLInputElement>):void => {setUsername(event.target.value);}}/>
        <TextField label="Name" placeholder="Enter name" required onChange={(event: React.ChangeEvent<HTMLInputElement>):void => {setFirst_name(event.target.value);}}/>
        <TextField label="Lastname" placeholder="Enter last name" required onChange={(event: React.ChangeEvent<HTMLInputElement>):void => {setLast_name(event.target.value);}}/>

        <Button type="submit" variant="contained" style={ { margin:'8px 0' } }  onClick={():void => {setInfoFromSecondPage(username, first_name, last_name); submitClick(); goToPage(1);} }>Submit</Button>

      </Paper>
    </Grid>
  );
};

