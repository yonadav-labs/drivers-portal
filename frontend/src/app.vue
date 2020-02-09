<template>
  <router-view v-if="appReady"></router-view>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Route } from 'vue-router';

import { Action } from 'vuex-class';

import { initClient, hasToken } from './store/api';


@Component
export default class App extends Vue {

  appReady = false;
  
  @Action('Users/retrieveUser')
  retrieveUser!: () => void;

  async created(): Promise<void> {
    await initClient();
    if (hasToken()) {
        await this.retrieveUser();
    }
    this.$nextTick(
      () => {
        this.appReady = true;
      }
    )
  }
}
</script>

<style lang="scss" scoped>
</style>
