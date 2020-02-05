<template>
  <div class="box-datepicker" :class="{'check': inputValue !== '','wrong': hasError && inputValue === ''}" @click="focus">
    <datepicker
      :disabledDates="disabledDates"
      :placeholder="placeholder"
      input-class="datepicker-input"
      v-model="inputValue"
      :format="format"
      :open-date="openDate"
      :initialView="initialView"
      :disabled="disabled">
    </datepicker>
    <icon-calendar size="14" :class="inputValue === '' ? 'icon--grey' : 'icon--blue'"></icon-calendar>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import Datepicker from 'vuejs-datepicker';

import IconCalendar from '@/components/icons/icon-calendar.vue';

@Component({
  components: {
    Datepicker, IconCalendar
  }
})
export default class InputDatepicker extends Vue {
  @Prop({ default: '' })
  placeholder!: string

  @Prop({ default: '' })
  value!: string

  @Prop({ default: 'MMMM d yyyy' })
  format!: string

  @Prop()
  disabledDates?: object

  @Prop({ default: false })
  hasError!: boolean

  @Prop({ default: false })
  disabled!: boolean

  @Prop()
  openDate?: Date | string

  @Prop({ default: 'day' })
  initialView!: 'day' | 'month' | 'year'

  get inputValue(): string {
    return this.value
  }

  set inputValue(val: string) {
    this.$emit('input', val);
  }

  focus():void {
    if (!this.disabled) {
      this.$emit('focus') 
    }
  }
}
</script>

<style lang="scss">
  .icon--grey {
    color: $grey;
  }
  .icon--blue {
    color: $blue;
  }
    .box-datepicker{
      align-items: center;
      background-color: $white;
      border: 1px solid $grey;
      border-radius: 2px;
      display: flex;
      justify-content: space-between;
      padding: 0.5rem 1rem;
      position:relative;
      width: 17rem;
      &.check{
        border: 1px solid $blue;
        box-shadow: 0 0 3px 0 rgba(66, 99, 235, 0.5);
      }
      &.wrong{
        animation: wrong-log 0.3s;
        border: 1px solid $orange;
      }
      .vdp-datepicker{
        font-size: $fs-md;
        line-height: 1.5;
        width: 100%;
         .datepicker-input{
            font-size: $fs-md;
            line-height: 1.5;
            width: 100%;
            &::placeholder{
                color:$grey;
            }
            &:focus{
                outline: none;
            }
        }
      }
      &:focus{
          border: 1px solid $blue;
      }
    }
    @keyframes wrong-log {
      0%{ left: 0px;}
      20%{left: 15px;}
      40%{left: -15px;}
      100% { left: 0px;}
      60%{left: 15px;}
      80%{left: -15px;}
    }
</style>