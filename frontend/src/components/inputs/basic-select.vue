<template>
  <div class="basic-select" :class="{'check':valueSelected != defaultOptionValue}">
    <select
      v-model="valueSelected"
      :disabled="disabled"
      :class="{'disabled':disabled}"
      @click="$emit('focus')"
      :id="id"
      :ref="id"
    >
      <option :value="defaultOptionValue" disabled>Select one</option>
      <option v-for="(option,index) in options" :value="option.value" :key="index">{{option.text}}</option>
    </select>
    <icon-chevron-down size="14" class="icon" :class="{'selected': valueSelected != ''}"></icon-chevron-down>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import IconChevronDown from '@/components/icons/icon-chevron-down.vue';

@Component({
  components: {
    IconChevronDown,
  }
})
export default class BasicSelect extends Vue {
  @Prop({ default: () => [] })
  options!: Array<{ value: any, text: string }>

  @Prop({ default: '' })
  selected!: any

  @Prop({ default: false })
  disabled!: boolean

  @Prop({ default: () => `select-${Math.floor(Math.random() * 9999)}` })
  id!: string

  @Prop({ default: '' })
  defaultOptionValue: any


  get valueSelected(): string {
    return this.selected;
  }

  set valueSelected(val: string) {
    this.$emit('input', val);
  }
}
</script>

<style lang="scss" scoped>
.basic-select {
  background-color: $white;
  border: 1px solid $grey;
  border-radius: 4px;
  cursor: pointer;
  position: relative;
  width: 9rem;

  &.check {
    border: 1px solid $blue;
    box-shadow: 0 2px 4px 0 rgba(206, 212, 218, 0.5);
    select {
      color: $blue-dark;
    }
  }
  select {
    color: $grey-darker;
    cursor: pointer;
    font-size: $fs-md;
    padding: 0.75rem;
    width: 100%;
    &:focus {
      outline: none;

      option {
        &:not(:disabled) {
          color: $blue-dark;
        }
      }
    }
    &.disabled {
      cursor: not-allowed;
      opacity: 0.5;
    }
  }
  .icon {
    color: $grey;
    position: absolute;
    right: 0.75rem;
    top: 50%;
    transform: translateY(-50%);
    &.selected {
      color: $blue;
    }
  }
}
</style>