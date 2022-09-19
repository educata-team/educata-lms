import { FC as OriginFC, ReactNode } from 'react';

export type FC<P = Record<string, unknown>> = OriginFC<
  P & {
    children?: ReactNode;
  }
>;
