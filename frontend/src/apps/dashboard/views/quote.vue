<template>
  <div id="dashboard-quote-view" v-if="showDashboard">
    <router-view></router-view>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import { Getter, Action, namespace } from 'vuex-class';

import { Route } from 'vue-router';

import { QuoteProcess } from '@/@types/quote';
import { User } from '@/@types/users';

import { DashboardRouter } from '@/router/dashboard';


const quote = namespace('Quote')
const users = namespace('Users')

@Component
export default class DashboardView extends Vue {

  @quote.Getter
  quoteProcess?: QuoteProcess

  @users.Getter
  user!: User

  @quote.Action
  retrieveQuoteProcess!: (id: string) => Promise<void>

  showDashboard = false;

  async beforeRouteEnter(to: Route, from: Route, next: any): Promise<void> {

    next(async (vm: DashboardView)  => {
      if (!vm.quoteProcess) {
        await vm.retrieveQuoteProcess(vm.user.quoteprocess!)
      }
      const nextRoute = DashboardRouter.getRouteForQuoteStatus(vm.quoteProcess!.status)
      if (nextRoute.name !== vm.$route.name) {
        vm.$router.replace(nextRoute)
      }
      vm.showDashboard = true;
    })
  }
}
</script>