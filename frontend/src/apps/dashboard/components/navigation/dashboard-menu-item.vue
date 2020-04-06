<template>
  <div class="menu-item" :class="{ 'selected': selected }" @click="onClick">
    <div class="menu-item--line"></div>
    <div class="menu-item--content">
      <slot></slot>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

@Component
export default class DashboardMenuItem extends Vue {
  @Prop({ default: false })
  selected!: boolean

  onClick(): void {
    if (!this.selected) {
      this.$emit('click');
    }
  }
}
</script>

<style lang="scss" scoped>
  .svg-icon-center {
      display: flex;
  }
</style>

<style lang="scss" scoped>
.menu-item {
  display: flex;
  align-items: stretch;
  justify-content: space-between;
  cursor: pointer;
  width: 46px;
  margin: 10px 10px 10px 0px;

  .menu-item--line {
    visibility: hidden;
    border-radius: 5px;
    border: 2px solid $blue;
  }

  .menu-item--content {
    align-items: center;
    border-radius: 2px;
    display: flex;
    height: 36px;
    justify-content: center;
    width: 36px;

    &:hover {
      background-color: rgba($grey, 0.2);
    }

    div {
      color: $blue;
    }
  }

  &.selected {
    cursor: default;

    .menu-item--line {
      visibility: visible;
    }

    .menu-item--content {
      background-color: rgba($grey, 0.2);
    }
  }
}
</style>