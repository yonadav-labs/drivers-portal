
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
            if (data instanceof Object) {
                state.data = {...data}
            } else {
                state.data = data;
            }
            state.status = 'success'
            state.error = undefined;
        }
        return {...state}
    }
}

export const client = axios.create({
    baseURL: process.env.VUE_APP_API_URL,
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFToken'
});
