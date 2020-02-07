<template>
  <div class="container">
    <dashboard-menu-item :disabled="true">
      <icon-policy size="20"></icon-policy>
    </dashboard-menu-item>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import DashboardMenuItem from '@/apps/dashboard/components/navigation/dashboard-menu-item.vue'
import IconPolicy from '@/components/icons/icon-policy.vue'

import { DashboardRouteName } from '@/router/dashboard'

@Component({
  components: {
    DashboardMenuItem, IconPolicy
  }
})
export default class DashboardMenu extends Vue {
    @Prop({ default: false })
    selected!: boolean

    routeNames = DashboardRouteName

    onClick(): void {
      this.$emit('click');
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
