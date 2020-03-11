<template>
  <div class="svg-icon-center">
    <svg aria-hidden="true" data-prefix="fas" data-icon="circle" class="svg-inline--fa fa-circle fa-w-16" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" :width="size" :height="size"><path fill="currentColor" d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8z"></path></svg>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

@Component
export default class IconInvoiceDollar extends Vue {
    @Prop()
    size?: string | number;
}
</script>

<style lang="scss" scoped>
  .svg-icon-center {
    display: flex;
  }
</style>
