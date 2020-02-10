<docs>
</docs>
<template>
  <div class="radio-component" :class="{'active': active}">
    <input type="checkbox"
      :id="id"
      :name="name"
      :value="value"
      :class="className"
      :required="required"
      :disabled="disabled"
      @change="toggle"
      :checked="state">
    <label :for="id">
      <span class="input-box">
        <span class="input-box-circle"></span>
      </span>
      <span class="input-text" v-if="text !== ''">{{text}}</span>
      <slot></slot>
    </label>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch, Model } from 'vue-property-decorator';

import { VueConstructor } from 'vue';

@Component
export default class Checkbox extends Vue {

  @Prop({ default: () => `radio-id-${Math.floor(Math.random() * 9999)}` })
  id!: string;

  @Prop()
  name!: string;

  @Prop({ default: false })
  value!: string;

  @Prop()
  className?: string;

  @Prop({ default: '' })
  text?: string;

  @Prop({ default: false })
  checked!: boolean;

  @Prop({ default: false })
  active!: boolean;

  @Prop({ default: false })
  required!: boolean;

  @Prop({ default: false })
  disabled!: boolean;

  @Model('input', { type:  [String, Boolean] }) 
  readonly modelValue!: string | boolean

  get state(): boolean {
    return this.modelValue === undefined ? this.checked:(this.modelValue === this.value)
  }
  
  toggle(): void {
    this.$emit('input', this.state ? '' : this.value);
  }

  @Watch('checked')
  changeChecked(val: boolean): void {
    if (val !== this.state) {
      this.toggle();
    }
  }

  created(): void {
    if (this.checked && !this.state) {
      this.toggle();
    }
  }
}
</script>

<style lang="scss" scoped>
.radio-component {
  cursor:pointer;

  .input-text{
    margin-top: 0.75rem;
    span{
      text-transform: capitalize;
    }
  }
  &.active > input + label > .input-box{
    border: 1px solid $blue;
  }
  &.active > input:disabled + label > .input-box{
    border: 1px solid $grey;
  }

  > input {
    opacity: 0;
    position: absolute;

    + label {
      align-items: center;
      color: $blue-dark;
      cursor:pointer;
      display: flex;
      flex-direction: row;
      font-size: $fs-lg;
      letter-spacing: 0.2px;
      line-height: 24px;


      & > .input-box {
      display: inline-block;
      background-color: $white;
      border: 1px solid $grey;
      flex-shrink: 0;
      height: 1.5rem;
      margin-right: 0.75rem;
      width: 1.5rem;

      > .input-box-circle {
        display: block;
        margin: 50%;
        width: 0%;
        height: 0%;
        background: $blue;
        opacity: 0;
        transition: width 0.15s ease-in, height 0.15s ease-in, margin 0.15s ease-in;
      }
    }
  }

    
    &:checked + label > .input-box{
      background-color: rgba(66,99,235,0.35);
      border: 1px solid $blue;
      & > .input-box-circle {
        opacity: 1;
        margin: 4px;
        width: 14px;
        height: 14px;
      }
    } 
    &:disabled + label {
      cursor: not-allowed;
      .input-text,.radio-form--text{
          opacity: 0.4;
      }
    }
  }
}
</style>
