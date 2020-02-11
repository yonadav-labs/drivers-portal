<template>
  <div class="modal-container">
    <div class="modal-container__overlay" @click="$emit('close')"></div>
    <div class="modal-container__content">
      <slot></slot>
    </div>
  </div>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator';

@Component
export default class Modal extends Vue {
  mounted(): void {
    document.body.style.overflow = 'hidden';
  }

  beforeDestroy(): void {
    document.body.style.overflow = '';
  }
}
</script>

<style lang="scss" scoped>
    .modal-container{
      height: 100vh;
      position: fixed;
      right: 50%;
      top: 50%;
      transform: translate(50%,-50%);
      width: 100%;
      z-index: 4;
      .modal-container__overlay {
        animation: fadeIn 0.5s ease;
        background-color: rgba(66, 99, 235, 0.3);
        bottom: 0;
        left: 0;
        position: absolute;
        right: 0;
        top: 0;
      }
      .modal-container__content {
        animation: fadeIn 0.75s ease;
        overflow: hidden;
        position: absolute;
        right: 50%;
        top: 50%;
        transform: translate(50%, -50%);

      }
    }
</style>