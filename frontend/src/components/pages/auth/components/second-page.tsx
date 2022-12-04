import { FC } from '../../../../common/types/react/fc.type';
import { FormValues } from '../common/form-values';
import { Button, Grid, MenuItem, Paper, TextField, Typography } from '@mui/material';
import { UseFormRegister } from 'react-hook-form';
import { Stack } from '@mui/system';

interface Props {
  onPageSwitch(pageNumber: number): void;
  register: UseFormRegister<FormValues>;
}

export const SecondPage: FC<Props> = ({
  onPageSwitch,
  register,
}) => {

  return (
    <Grid>
      <Paper elevation={10} style={{ padding: 20, height: '70vh', width: 380, margin: '20px auto', display: 'flex', flexDirection: 'column', justifyContent: 'space-around' }}>
        <Grid style={{ textAlign: 'center' }}>
          <Typography variant="h4" gutterBottom>Sign Up</Typography>
        </Grid>
        <TextField label="Username" placeholder="Enter username" type="text" required {...register('username')} />
        <TextField label="First name" placeholder="Enter first name" type="text" required {...register('first_name')} />
        <TextField label="Last name" placeholder="Enter last name" type="text" required {...register('last_name')} />
        <Grid style={{ textAlign: 'center' }}>
          <Typography variant="subtitle1">Account type:</Typography>
        </Grid>
        <TextField label="Select account type" select required defaultValue="user" {...register('role')}>
          <MenuItem value="user">User</MenuItem>
          <MenuItem value="lecturer">Lecturer</MenuItem>
        </TextField>

        <Stack direction="row" style={{ width: '100%' }}>
          <Button variant="outlined" style={{ margin: '8px 10px 0 0', width: '100%' }} onClick={(): void => onPageSwitch(1)}>Back</Button>
          <Button type="submit" variant="contained" style={{ margin: '8px 0 0 10px', width: '100%' }} >Sign up</Button>
        </Stack>
      </Paper>
    </Grid>
  );
};

