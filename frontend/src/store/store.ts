import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

import QuoteModules from './quote'

export const store = new Vuex.Store({
  strict: true,
  state: {},
  modules: {
    ...QuoteModules,
  },
});
