import { FC } from '../../../../common/types/react/fc.type';
import { FormValues } from '../common/form-values';
import { Button, Grid, Paper, TextField, Typography } from '@mui/material';
import { UseFormRegister } from 'react-hook-form';
import { Stack } from '@mui/system';

interface Props {
  onPageSwitch(pageNumber: number): void;
  register: UseFormRegister<FormValues>;
  onSubmit(): void;
}

export const SecondPage: FC<Props> = ({
  onPageSwitch,
  register,
  onSubmit,
}) => {

  return (
    <Grid>
      <Paper elevation={10} style={{ padding: 20, height: '60vh', width: 380, margin: '20px auto', display: 'flex', flexDirection: 'column', justifyContent: 'space-around' }}>
        <Grid style={{ textAlign: 'center' }}>
          <Typography variant="h4" gutterBottom>Sign Up</Typography>
        </Grid>
        <TextField label="Username" placeholder="Enter username" type="text" required {...register('username')} />
        <TextField label="First name" placeholder="Enter first name" type="text" required {...register('firstName')} />
        <TextField label="Last name" placeholder="Enter last name" type="text" required {...register('lastName')} />

        <Stack >
          <Button variant="outlined" style={{ margin: '8px 0' }} onClick={(): void => onPageSwitch(1)}>Back</Button>
          <Button variant="contained" style={{ margin: '8px 0' }} onClick={(): void => onSubmit()}>Sign up</Button>
        </Stack>
      </Paper>
    </Grid>
  );
};

