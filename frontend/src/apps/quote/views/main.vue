<template>
  <router-view v-if="showQuote"></router-view>
</template>
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import { Getter, namespace } from 'vuex-class';
import { Route } from 'vue-router';

import { QuoteStatus } from '@/@types/quote';

import { RouteName } from '@/router'


const users = namespace('Users')

@Component
export default class Main extends Vue {
  
  @users.Getter
  isAuthenticated!: boolean

  @users.Getter
  userQuoteStatus?: QuoteStatus

  showQuote = false;

  async beforeRouteEnter(to: Route, from: Route, next: any): Promise<void> {

    next(async vm => {
      if (vm.isAuthenticated && vm.userQuoteStatus !== undefined) {
        vm.$router.replace({ name: RouteName.DASHBOARD })
      } else {
        vm.showQuote = true;
      }
    })
  }
}
</script>
