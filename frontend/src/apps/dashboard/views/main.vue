<template>
  <div id="dashboard-view">
    <div class="dashboard-view-container">
      <dashboard-navbar></dashboard-navbar>
      <div class="dashboard-container">
        <dashboard-menu></dashboard-menu>
        <div class="dashboard-content">
          <router-view></router-view>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import { Getter, Action, namespace } from 'vuex-class';

import DashboardNavbar from '@/apps/dashboard/components/navigation/dashboard-navbar.vue'
import DashboardMenu from '@/apps/dashboard/components/navigation/dashboard-menu.vue'

import { User } from '@/@types/users';

import { QuoteProcessRouter } from '@/router/quote'
import { DashboardRouteName } from '@/router/dashboard'

const users = namespace('Users')

@Component({
  components: {
    DashboardNavbar, DashboardMenu
  }
})
export default class Dashboard extends Vue {

  @users.Getter
  isAuthenticated!: boolean

  @users.Getter
  isUserRetrieved!: boolean

  @users.Getter
  user?: User

  @users.Action
  retrieveUser!: () => Promise<void>

  async created(): Promise<void> {
    if (!this.isUserRetrieved) {
      await this.retrieveUser()
    }
    if (!this.isAuthenticated) {
      this.$router.replace(QuoteProcessRouter.getRouteByOrder(0))
    }

    if (!!this.user && this.user.quote_status !== 'done') {
      this.$router.replace({ name: DashboardRouteName.DOCS })
    }
  }
}
</script>

<style lang="scss" scoped>
#dashboard-view {
  background-color: $grey-light;
  .dashboard-view-container{
    background-color: $white;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    margin: 0 auto;
    max-width: 73.13rem;
    padding: 4px 10px;
    width: 100%;
  }
  .dashboard-container {
    align-items: stretch;
    display: flex;
    height: 100%;

    .dashboard-content {
      padding: 1.875rem 1.25rem 1.875rem 1.875rem;
      width: 100%;
    }
  }
}
</style>