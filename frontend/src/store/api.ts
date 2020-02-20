
import axios from 'axios';

type callStatus = 'initial' | 'pending' | 'success' | 'failed'

export interface State { data?: any, error?: Error, status: callStatus }

export interface APIProperty<V> extends State { data?: V, error?: Error, status: callStatus }

export class APIState {
    // Based on 
    // https://medium.com/js-dojo/yet-another-pattern-for-api-calls-using-vuejs-vuex-b22ecdfb0ea2
    
    static state<V>(data?: V): APIProperty<V>  {
        return {
            data,
            error: undefined,
            status: 'initial'
        }
    }

    static setPending(state: State): State {
        return {
            ...state,
            status: 'pending'
        }
    }

    static update(state: State, data: any): State {
        if (data instanceof Error) {
            state.error = data;
            state.status = 'failed'
            state.data = undefined
        } else {
            if (data instanceof Object && !Array.isArray(data)) {
                state.data = {...data}
            } else {
                state.data = data;
            }
            state.status = 'success'
            state.error = undefined;
        }
        return {...state}
    }

    static patch(state: State, data: any): State {
      if (data instanceof Error) {
        state.error = data;
        state.status = 'failed'
        state.data = undefined
      } else {
        if (data instanceof Object) {
          state.data = { ...state.data, ...data }
        } else {
          state.data = data;
        }
        state.status = 'success'
        state.error = undefined;
      }
      return { ...state }
    }
}

const AUTH_TOKEN_KEY = 'auth_token'

export const client = axios.create({
    baseURL: process.env.VUE_APP_API_URL,
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFToken'
});

export async function initClient(): Promise<void> {
  const token = localStorage.getItem(AUTH_TOKEN_KEY)
  if (token !== null) {
    client.defaults.headers.Authorization = `Token ${token}`;

    try {
      await client.get('users/check_token/')
    } catch (e) {
      clearAuthToken();
    }
  }
}

export function clearAuthToken(): void {
  delete client.defaults.headers.Authorization;
  localStorage.removeItem(AUTH_TOKEN_KEY);
  deleteAuthenticatedCookie()
}

export function hasToken(): boolean {
  return !!client.defaults.headers.Authorization
}

export function setAuthToken(token: string): void {
  client.defaults.headers.Authorization = `Token ${token}`;
  localStorage.setItem(AUTH_TOKEN_KEY, token);
  setAuthenticatedCookie()
}


function getCookieDomain(): string {
  return process.env.VUE_APP_ENV === 'development' ? '.stableins.test':'.stableins.com'
}

export function setAuthenticatedCookie(): void {
  const exdays = 15;
  const d = new Date();
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
  const expires = 'expires=' + d.toUTCString();
  document.cookie = `authenticated=true;${expires};path=/;domain=${getCookieDomain()};`
}

export function deleteAuthenticatedCookie(): void {
  document.cookie = `authenticated=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;domain=${getCookieDomain()};`
}