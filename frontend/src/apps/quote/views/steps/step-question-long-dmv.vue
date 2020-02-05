<template>
  <quote-process-layout>
    <quote-process-radio-form :answers="answers" name="years" v-model="value" @next="onNext">
      How long have you had your DMV license?
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


import { QuoteRouteNames, QuoteProcessRouter } from '@/router/quote'

// Question Step 

const quote = namespace('Quote')

@Component({
  components: {
    QuoteProcessLayout, QuoteProcessRadioForm
  }
})
export default class StepQuestionLongDmv extends Vue {
  @quote.Getter
  stepCompletedByName!: (route: QuoteRouteNames) => boolean

  @quote.Getter
  questionAnswers!: QuestionsStep;

  @quote.Action
  updateStepStatus!: (payload: { step: QuoteRouteNames, value: boolean }) => void;

  @quote.Action
  updateQuestionAnswers!: (payload: QuestionsStep) => void;

  value = ''
  
  answers = [
    {
      label: '+3 years',
      value: '3+'
    },
    {
      label: '2 - 3 years',
      value: '2-3'
    },
    {
      label: '<2 year',
      value: '<2'
    }
  ]

  onNext(): void {
    this.updateQuestionAnswers({ dmv_license_years: this.value })
    this.updateStepStatus({ step: this.$route.name! as QuoteRouteNames, value: true });
    this.$router.push(QuoteProcessRouter.nextRoute(this.$route.name! as QuoteRouteNames))
  }

  resetState(): void {
    this.value = '';
    this.updateQuestionAnswers({ dmv_license_years: undefined });
    this.updateStepStatus({ step: this.$route.name! as QuoteRouteNames, value: false });
  }

  created(): void {
    this.value = this.questionAnswers.dmv_license_years || ''
  }

  beforeRouteEnter (to: Route, from: Route, next: any): void {
    next((vm: StepQuestionLongDmv) => {
      if (!from.name || QuoteProcessRouter.isBefore(from.name as QuoteRouteNames, vm.$route.name! as QuoteRouteNames)) {
        vm.resetState();
      }

      if (!vm.stepCompletedByName(QuoteProcessRouter.previousRouteName(vm.$route.name! as QuoteRouteNames))) {
        vm.resetState();
        vm.$router.replace(QuoteProcessRouter.previousRoute(vm.$route.name! as QuoteRouteNames));
      }
    })
  }
}
</script>

<style lang='scss' scoped>

</style>
