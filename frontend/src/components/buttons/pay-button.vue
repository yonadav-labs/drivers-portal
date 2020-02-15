<template>
  <button class="pay-button" :class="{'disabled' : disabled}" @click="$emit('click',$event)" :disabled="disabled" :style="{color:color}">
    <div class="pay-button--action">
      <span :style="{color:color}">{{text}}</span>
      <slot></slot>
    </div>
    <span class="pay-button--info" v-if="info">{{info}}</span>
  </button>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

@Component
export default class PayButton extends Vue {
  @Prop()
  text!: string;

  @Prop({ default: '#868E96' })
  color?: string

  @Prop()
  info!: string;

  @Prop({ default: false })
  disabled?: boolean
}
</script>

<style lang="scss" scoped>
  .pay-button{
    align-items: center;
    background-color: $white;
    border: 1px solid $orange;
    border-radius: 0.5rem;
    cursor: pointer;
    flex-direction: column;
    display: flex;
    margin: 0 1.25rem;
    opacity: 0.8;
    padding: 0.625rem;
    width: 10.69rem;
    &:hover{
      background-color: rgba(247, 103, 7, 0.1);
    }
    .pay-button--action{
      display: flex;
      justify-content: center;
      align-items: center;
    }
    span{
      font-size: $fs-lg;
      font-weight: 600;
      line-height: 1.33;
      &.pay-button--info{
        font-size: $fs-sm;
        font-weight: $fw-light;
        margin: 0.25rem 0 0;
        opacity: 0.5;
      }
    }
    
    &:focus{
      outline: none;
    }
  }
</style>