import { AjaxClient } from '@commite/ajax-client';

export const httpClient = new AjaxClient({
  baseUrl: process.env.VUE_APP_API_URL,
});
