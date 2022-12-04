import { Button, Grid, Paper, TextField, Typography } from '@mui/material';
import { FC } from 'common/types/types';
import { FormValues } from '../common/form-values';
import { UseFormRegister, UseFormWatch } from 'react-hook-form';

interface Props {
  onPageSwitch(pageNumber: number): void;
  register: UseFormRegister<FormValues>;
  watch: UseFormWatch<FormValues>;
}

export const FirstPage: FC<Props> = ({
  onPageSwitch,
  register,
  watch,
}) => {
  return (
    <Grid>
      <Paper elevation={10} style={{ padding: 20, height: '70vh', width: 380, margin: '20px auto', display: 'flex', flexDirection: 'column', justifyContent: 'space-around' }}>
        <Grid style={{ textAlign: 'center' }}>
          <Typography variant="h4" gutterBottom>Sign Up</Typography>
        </Grid>
        <TextField label="Email" placeholder="Enter email" type="email" required {...register('email')} />
        <TextField label="Password" placeholder="Enter password" type="password" required {...register('password')} />
        <TextField
          label="Repeat password"
          placeholder="Repeat password"
          type="password"
          required
          {...register('password_repeat', {
            validate: (val: string): string | undefined => {
              if (watch('password') !== val) {
                return 'The passwords do not match';
              }
            },
          })} />

        <Button variant="contained" style={{ margin: '8px 0' }} onClick={(): void => onPageSwitch(2)}>Next</Button>

      </Paper>
    </Grid >
  );
};
