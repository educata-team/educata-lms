export type SignUpRequestDto = {
  email: string;
  username: string;
  password: string;
  passwordConfirm?: string;
  firstName: string;
  lastName: string;
};
