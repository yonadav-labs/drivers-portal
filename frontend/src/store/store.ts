import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

import QuoteModules from './quote'
import PolicyModules from './policy'
import UsersModules from './users'

import { initClient, hasToken, setAuthenticatedCookie, deleteAuthenticatedCookie } from './api';

export const store = new Vuex.Store({
  strict: true,
  state: {},
  modules: {
    ...QuoteModules,
    ...PolicyModules,
    ...UsersModules
  },
  actions: {
    async initializeStore(): Promise<void> {
      await initializeStore();
    },
    async resetStore(): Promise<void> {
      await resetStore();
    },
  }
});

const initialStateCopy = JSON.parse(JSON.stringify(store.state))

async function initializeStore(): Promise<void> {
  await initClient();
  if (hasToken()) {
    await store.dispatch('Users/retrieveUser');
    setAuthenticatedCookie();
  } else {
    deleteAuthenticatedCookie();
  }
}

async function resetStore():Promise<void> {
  store.replaceState(initialStateCopy)
  await initializeStore();
}
