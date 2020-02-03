import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

import Quote from './quote/quote'

export const store = new Vuex.Store({
  strict: true,
  state: {},
  modules: {
    Quote,
  },
});
