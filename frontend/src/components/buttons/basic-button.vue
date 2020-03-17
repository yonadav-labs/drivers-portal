<template>
  <button class="basic-button" @click="$emit('click',$event)" :disabled="disabled" :style="{color:color,backgroundColor:backgroundColor}">
    <slot name="before"></slot>
    <span :style="{color:color}">{{text}}</span>
    <slot></slot>
  </button>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

@Component
export default class BasicButton extends Vue {
  @Prop()
  text!: string;

  @Prop({ default: '#868E96' })
  color?: string

  @Prop({ default: 'transparent' })
  backgroundColor?: string

  @Prop({ default: false })
  disabled?: boolean
}
</script>

<style lang="scss" scoped>
  .basic-button{
    align-items: center;
    cursor: pointer;
    justify-content: center;
    display: flex;
    margin: 0 auto;
    padding: 0.75rem;
    span{
      font-size: 16px;
      font-weight: 600;
      margin-left: 0.5rem;
      margin-right: 1rem;
    }
    &:disabled{
      color: $grey !important;
      cursor: not-allowed;

      span {
        color: $grey !important;
      }
    }
    &:focus{
      outline: none;
    }
  }
  .fa-arrow-right{
    height: 1rem;
    width: 1rem;
  }
</style>