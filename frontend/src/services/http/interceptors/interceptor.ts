type PostInterceptorParameters = {
  response: Response;
  initialRequest: {
    url: string;
    options: RequestInit;
  };
  makeRequestFn: (url: string, options: RequestInit) => Promise<Response>;
};

type PreInterceptorParameters = {
  options: RequestInit;
  url: string;
};

export type PostInterceptor = {
  (parameters: PostInterceptorParameters): Promise<Response>;
};

export type PreInterceptor = {
  (parameters: PreInterceptorParameters): Promise<[string, RequestInit]>;
};
