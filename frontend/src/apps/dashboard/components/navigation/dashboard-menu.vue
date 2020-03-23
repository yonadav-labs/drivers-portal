<template>
  <div class="container">
    <dashboard-menu-item :selected="$route.name === mainRoute" @click="goTo(mainRoute)">
      <icon-policy size="20"></icon-policy>
    </dashboard-menu-item>
    <dashboard-menu-item :selected="$route.name === routeNames.SETTINGS" @click="goTo(routeNames.SETTINGS)">
      <icon-settings size="20"></icon-settings>
    </dashboard-menu-item>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import DashboardMenuItem from '@/apps/dashboard/components/navigation/dashboard-menu-item.vue'
import IconPolicy from '@/components/icons/icon-policy.vue'
import IconSettings from '@/components/icons/icon-settings.vue'

import { QuoteStatus } from '@/@types/quote';

import { DashboardRouter, DashboardRouteName } from '@/router/dashboard'

@Component({
  components: {
    DashboardMenuItem, IconPolicy, IconSettings
  }
})
export default class DashboardMenu extends Vue {
    @Prop()
    quoteStatus!: QuoteStatus

    routeNames = DashboardRouteName

    get mainRoute(): string {
      return DashboardRouter.getRouteForQuoteStatus(this.quoteStatus).name
    }

    goTo(menuRoute: string): void {
      this.$router.replace({ name: menuRoute }).catch(err => console.log(err))
    }
}
</script>

<style lang="scss" scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  border-right: 1px solid rgba($grey, 0.4);
  margin: 20px 0 10px;
  width: 4rem;
}
</style>
