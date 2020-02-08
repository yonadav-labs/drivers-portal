// Specific polyfills to allow code compatibility with IE11
import 'core-js/es6';
import 'core-js/es7'; 
import 'ie11-custom-properties';
import 'element-closest-polyfill';
import 'child-replace-with-polyfill';

// Hooks for components
import './class-component-hooks'

import Vue from 'vue';
import VueRouter from 'vue-router'

import App from './app.vue';

import { router } from './router'
import { store } from './store/store'

import 'url-polyfill'; // Polyfill to make Plyr working on IE11
import 'custom-event-polyfill'; // Polyfill to make Plyr working on IE11
import { initClient } from './store/api';

Vue.config.productionTip = false;

Vue.use(VueRouter)

new Vue({
  router,
  store,
  created: async () => {
    await initClient();
  },
  render: h =>
    h(App),
}).$mount(`#app`);

