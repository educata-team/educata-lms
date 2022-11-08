import { ContentType, HttpMethod } from 'common/enums/enums';

export type HttpOptions = {
  method: HttpMethod;
  contentType: ContentType;
  payload: BodyInit | null;
};
