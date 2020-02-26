<template>
  <div id="dashboard-view" v-if="showDashboard">
    <div class="dashboard-view-container">
      <dashboard-navbar></dashboard-navbar>
      <div class="dashboard-container">
        <dashboard-menu></dashboard-menu>
        <div class="dashboard-content">
          <router-view></router-view>
        </div>
      </div>
    </div>
    <modal-create-password v-if="showCreatePassword" :email="user.email" @submit="createPassword"></modal-create-password>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import { Getter, Action, namespace } from 'vuex-class';

import DashboardNavbar from '@/apps/dashboard/components/navigation/dashboard-navbar.vue'
import DashboardMenu from '@/apps/dashboard/components/navigation/dashboard-menu.vue'

import ModalCreatePassword from '@/apps/dashboard/components/modals/create-password.vue'

import { User } from '@/@types/users';

import { QuoteProcessRouter } from '@/router/quote'
import { DashboardRouteName, DashboardRouter } from '@/router/dashboard'
import { Route } from 'vue-router';

const users = namespace('Users')

@Component({
  components: {
    DashboardNavbar, DashboardMenu, ModalCreatePassword
  }
})
export default class DashboardView extends Vue {

  @users.Getter
  isAuthenticated!: boolean

  @users.Getter
  user?: User

  @users.Action
  retrieveUser!: () => Promise<void>

  @users.Action
  updateUserPassword!: (password: string) => Promise<void>

  showCreatePassword = false;
  showDashboard = false;

  async createPassword(password: string): Promise<void> {
    await this.updateUserPassword(password)
    this.showCreatePassword = false;
  }

  async beforeRouteEnter(to: Route, from: Route, next: any): Promise<void> {

    next(async (vm: DashboardView) => {
      if (!vm.isAuthenticated) {
        vm.$router.replace(QuoteProcessRouter.getRouteByOrder(0))
      } else {
        if (vm.user!.quote_status !== 'done') {
          if (!DashboardRouter.isDocsRoute(vm.$route.name!)) {
            vm.$router.replace({ name: DashboardRouteName.QUOTE })
          }
        } else {
          vm.$router.replace({ name: DashboardRouteName.POLICY })
        }

        if (!vm.user!.has_usable_password) {
          setTimeout(() => {
            vm.showCreatePassword = true;
          }, 1000)
        }
        vm.showDashboard = true;
      }
    })
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