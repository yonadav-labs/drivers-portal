<template>
    <div class='question-container'>
        <p class='question-container__explain'><slot></slot></p>
        <form id='radioForm' @submit.prevent.stop="next">
          <div class="question-content">
            <ul>
              <radio
                v-for="answer in answers"
                class="question-content__radio"
                :key="answer.value"
                :name="name"
                :value="answer.value"
                :model-value="value"
                @input="input"
              >
                {{ answer.label }}
              </radio>
            </ul>
          </div>
          <basic-button
            text='Next Step'
            :disabled="!value"
            :color='colorBlue'
            >
            <icon-arrow-right size='16' class='icon--blue'></icon-arrow-right>
          </basic-button>
      </form>
    </div>
</template>

<script lang="ts">
import { Component, Vue, Prop, Model } from 'vue-property-decorator';

import { RadioElement } from '@/apps/quote/components/@types/forms'

import BasicButton from '@/components/buttons/basic-button.vue'
import Radio from '@/components/inputs/radio.vue'
import IconArrowRight from '@/components/icons/icon-arrow-right.vue'

import { Colors } from '@/utils/colors'

@Component({
  components: {
    Radio, BasicButton, IconArrowRight
  }
})
export default class QuoteProcessRadioForm extends Vue {
  
  @Prop({ default: () => [] })
  answers!: RadioElement[]

  @Prop()
  name!: string

  @Prop()
  value!: string

  get colorBlue(): string {
    return Colors.Blue
  }

  input(val: string): void {
    this.$emit('input', val)
  }

  next(): void {
    this.$emit('next')
  }
}
</script>

<style lang='scss' scoped>
.question-container {
  padding: 1.875rem 5.625rem 1.75rem;
  text-align: center;

  .question-container__explain {
    line-height: 1.5;
    font-size: $fs-lg;
    margin-left: auto;
    margin-right: auto;

    span {
      font-weight: $fw-semibold;
    }
  }

  .question-content {
    background-color: $grey-opacity;
    border-radius: 8px;
    margin: 1.25rem auto;
    padding: 1.25rem 1.875rem;

    &.question-content--success {
      padding: 1.25rem 1.5rem;
      text-align: left;
    }

    .question-content__radio {
      &:not(:last-child) {
        margin-bottom: 1.25rem;
      }
    }
  }
}
</style>
