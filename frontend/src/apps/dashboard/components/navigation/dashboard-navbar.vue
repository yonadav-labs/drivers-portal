<template>
  <nav class="container">
    <span class="logo">Stable</span>
    <div class="notifications-container">
      <div class="logout">
        <span>Log out</span><icon-logout size="18"></icon-logout>
      </div>
    </div>
  </nav>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import DashboardMenu from '@/apps/dashboard/components/navigation/dashboard-menu.vue'
import IconLogout from '@/components/icons/icon-logout.vue'


import { DashboardDocsRouteName } from '@/router/dashboard'

@Component({
  components: {
    DashboardMenu, IconLogout
  }
})
export default class DashboardNavbar extends Vue {
    routeNames = DashboardDocsRouteName
}
</script>

<style lang="scss" scoped>
.container {
  align-items: center;
  background-color: rgba($blue, 0.9);
  border-radius: 4px;
  display: flex;
  height: 60px;
  position: relative;
  width: 100%;

  &::after {
    content: "";
    background-image: url("~@/assets/navbar-bg.png");
    background-size: cover;
    border-bottom-right-radius: 4px;
    border-top-right-radius: 4px;
    bottom: 0;
    left: 25%;
    opacity: 0.5;
    position: absolute;
    right: 0;
    top: 0;
  }

  .logo {
    color: white;
    font-family: "Proxima Nova";
    font-size: $fs-xxl;
    font-weight: bold;
    margin-left: 32px;
  }

  .notifications-container {
    align-items: center;
    display: flex;
    margin-left: auto;
    margin-right: 20px;
    z-index: 1;

    .notification-item {
      cursor: pointer;
      height: 24px;
      margin: 20px;
      position: relative;
      width: 24px;

      .notification-icon {
        color: white;
        position: absolute;
        top: 6px;
      }

      .notification-count {
        align-items: center;
        background-color: #f76707;
        border-radius: 16px;
        color: white;
        display: flex;
        font-size: $fs-xs;
        font-weight: 600;
        height: 16px;
        justify-content: center;
        position: absolute;
        right: 0;
        top: 0;
        width: 16px;
      }
    }
    .logout {
      display: flex;
      align-items: center;
      background-color: #2C4DD3;
      justify-content: center;
      border-radius: 2px;
      color: white;
      cursor: pointer;
      height: 36px;
      width: 106px;

      span {
        color: $white;
        font-weight: $fw-semibold;
        margin-right: 14px;
      }
      &:hover{
        border: 1px solid rgba(255, 255, 255, 0.4);
      }
    }
  }
}
</style>