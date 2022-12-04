import { Button, Grid, Paper, TextField, Typography } from '@mui/material';
import { FC } from 'common/types/types';
import { useAppDispatch } from 'hooks/hooks';
import { useForm } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
import { authActions } from 'store/actions';
import { AppRoute } from '../../../common/enums/enums';
import { FormValues } from './common/form-values';

import styles from './styles.module.scss';

export const Auth: FC = () => {
  const { register, handleSubmit } = useForm<FormValues>({
    criteriaMode: 'all',
    reValidateMode: 'onChange',
    mode: 'onChange',
  });
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  return (
    <div className={styles['form-wrapper']}>
      <form onSubmit={handleSubmit(async (data) => {
        await dispatch(authActions.signIn(data))
          .unwrap()
          .then(() => navigate(AppRoute.ROOT));
      })}>
        <Grid>
          <Paper elevation={10} style={{ padding: 20, height: '70vh', width: 380, margin: '20px auto', display: 'flex', flexDirection: 'column', justifyContent: 'space-around' }}>
            <Grid style={{ textAlign: 'center' }}>
              <Typography variant="h4" gutterBottom>Sign In</Typography>
            </Grid>
            <TextField label="Username" placeholder="Enter username" type="text" required {...register('username')} />
            <TextField label="Password" placeholder="Enter password" type="text" required {...register('password')} />
            <Button type="submit" variant="contained" style={{ margin: '8px 0' }} >Sign in</Button>
            <Typography>
              You're new here? 
              <Link to={AppRoute.SIGN_UP} >
                Sign Up
              </Link>
            </Typography>
          </Paper>
        </Grid>

      </form>
    </div>
  );
};

