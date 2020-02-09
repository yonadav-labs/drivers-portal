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

  @Action
  initializeStore!: () => void;

  async created(): Promise<void> {
    await this.initializeStore();

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
