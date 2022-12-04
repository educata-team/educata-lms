import { UserRole } from 'common/enums/enums';

export type UserInfoResponseDto = {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  avatar: string;
  bio: string;
  role: UserRole;
};
