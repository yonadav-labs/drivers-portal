<template>
  <quote-process-layout>
    <quote-summary></quote-summary>
    <quote-process-radio-form :answers="answers" name="years" v-model="value" @next="onNext">
      How many at fault accidents do you have in the last 36 months? 
    </quote-process-radio-form>
  </quote-process-layout>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';

import { Getter, Action, namespace } from 'vuex-class';
import { Route } from 'vue-router';

import { QuestionsStep } from '@/@types/quote';

import { RadioElement } from '@/apps/quote/components/@types/forms'
import QuoteProcessRadioForm from '@/apps/quote/components/forms/quote-process-radio-form.vue'
import QuoteProcessLayout from '@/apps/quote/components/layout/quote-process-layout.vue'
import QuoteSummary from '@/apps/quote/components/containers/quote-summary.vue'


import { OrderedQuoteRouteName, QuoteProcessRouter } from '@/router/quote'

// Question Step 

const quote = namespace('Quote')

@Component({
  components: {
    QuoteProcessLayout, QuoteProcessRadioForm, QuoteSummary
  }
})
export default class StepQuestionFaultAccidents extends Vue {

  @quote.Getter
  questionAnswers!: QuestionsStep;

  @quote.Getter
  stepCompletedByName!: (route: OrderedQuoteRouteName) => boolean

  @quote.Action
  updateStepStatus!: (payload: { step: string, value: boolean }) => void;

  @quote.Action
  updateQuestionAnswers!: (payload: QuestionsStep) => void;

  value = ''
  
  answers = [
    {
      label: '0',
      value: '0'
    },
    {
      label: '1',
      value: '1'
    },
    {
      label: '2',
      value: '2'
    },
    {
      label: '3+',
      value: '3+'
    },
  ]

  onNext(): void {
    this.updateQuestionAnswers({ fault_accidents_last_months: this.value })
    this.updateStepStatus({ step: this.$route.name!, value: true });
    this.$router.push(QuoteProcessRouter.nextRoute(this.$route.name!))
  }

  resetState(): void {
    this.value = '';
    this.updateQuestionAnswers({ fault_accidents_last_months: undefined });
    this.updateStepStatus({ step: this.$route.name!, value: false });
  }

  created(): void {
    this.value = this.questionAnswers.fault_accidents_last_months || ''
  }

  beforeRouteEnter (to: Route, from: Route, next: any): void {
    next((vm: StepQuestionFaultAccidents) => {
      if (!from.name || QuoteProcessRouter.isBefore(from.name, vm.$route.name!)) {
        vm.resetState();
      }

      if (!vm.stepCompletedByName(QuoteProcessRouter.previousRouteName(vm.$route.name!))) {
        vm.resetState();
        vm.$router.replace(QuoteProcessRouter.previousRoute(vm.$route.name!));
      }
    })
  }
}
</script>

<style lang='scss' scoped>

</style>
