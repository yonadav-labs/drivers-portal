<template>
  <button class="contained-button" :class="buttonClasses" @click="$emit('click', $event)" :disabled="disabled">
    <span><slot></slot></span>
    <component
      v-bind:is="iconComponent"
      :size="iconSize"
      class="icon"
    ></component>
  </button>
</template>

<script lang="ts">
import { VueConstructor } from 'vue';

import { Component, Vue, Prop } from 'vue-property-decorator';

import { DashboardQuoteRouteName } from '@/router/dashboard'

import IconCheck from '@/components/icons/icon-check.vue'
import IconDollar from '@/components/icons/icon-dollar.vue'
import IconFileDownload from '@/components/icons/icon-file-download.vue'
import IconFileUpload from '@/components/icons/icon-file-upload.vue'
import IconPenAlt from '@/components/icons/icon-pen-alt.vue'

type Icon = ''| 'check' | 'dollar' | 'file-download' | 'file-upload' | 'pen-alt'

@Component
export default class ContainedButton extends Vue {
  @Prop({ default: '' })
  color!: '' | 'blue' | 'grey'
  
  @Prop({ default: false })
  disabled!: boolean;

  @Prop({ default: ''})
  icon!: Icon;

  @Prop({ default: '16' })
  iconSize!: string;

  get buttonClasses(): Record<string, boolean> {
    return {
      'disabled': this.disabled,
      [this.color]: !!this.color
    }
  }

  get iconComponent(): VueConstructor<Vue> | undefined {
    switch (this.icon) {
      case 'check':
        return IconCheck;
      case 'dollar':
        return IconDollar;
      case 'file-download':
        return IconFileDownload
      case 'file-upload':
        return IconFileUpload;
      case 'pen-alt':
        return IconPenAlt;
      default:
        return undefined;
    }
  }

}
</script>

<style lang="scss" scoped>
.contained-button{
  align-items: center;
  border-radius: 4px;
  cursor: pointer;
  justify-content: center;
  display: inline-flex;
  padding: 0.875rem 0.7625rem;

  span{
    font-size: $fs-md;
    font-weight: $fw-semibold;
    margin-right: 1rem;
  }
  &:focus{
    outline: none;
  }

  &.blue {
    background-color: $blue;
    color: $white;

    &:hover{
      background-color: #2C4DD3;
    }
  }

  &.grey {
    background-color: $grey-opacity;
    color: $blue;
    
    &:hover{
      background-color: $grey-medium-dark;
    }

  }

  &.disabled {
    background-color: $grey-opacity;
    color: $grey-darker;
    cursor: not-allowed;

    &:hover{
      background-color: $grey-opacity;
    }
  }
}

</style>
