<template>
  <router-view v-if="showQuote"></router-view>
</template>
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import { Getter, namespace } from 'vuex-class';
import { Route } from 'vue-router';

import { User } from '@/@types/users';

import { RouteName } from '@/router'


const users = namespace('Users')

@Component
export default class MainView extends Vue {

  @users.Getter
  user?: User

  showQuote = false;

  async beforeRouteEnter(to: Route, from: Route, next: any): Promise<void> {

    next(async (vm: MainView) => {
      if (!!vm.user && vm.user.quoteprocess) {
        vm.$router.replace({ name: RouteName.DASHBOARD })
      } else {
        vm.showQuote = true;
      }
    })
  }
}
</script>
