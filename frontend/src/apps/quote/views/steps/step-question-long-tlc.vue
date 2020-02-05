<template>
  <quote-process-layout>
    <quote-process-radio-form :answers="answers" name="years" v-model="value" @next="onNext">
      How long have you had your TLC license?
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
export default class StepQuestionLongTlc extends Vue {
  @quote.Getter
  questionAnswers!: QuestionsStep;

  @quote.Getter
  stepCompletedByName!: (route: QuoteRouteNames) => boolean

  @quote.Action
  updateStepStatus!: (payload: { step: QuoteRouteNames, value: boolean }) => void;

  @quote.Action
  updateQuestionAnswers!: (payload: QuestionsStep) => void;

  value = ''
  
  answers = [
    {
      label: '+3 years',
      value: '+3'
    },
    {
      label: '1 - 3 years',
      value: '1-3'
    },
    {
      label: '<1 year',
      value: '<1'
    }
  ]

  onNext(): void {
    this.updateQuestionAnswers({ tlc_license_years: this.value })
    this.updateStepStatus({ step: this.$route.name! as QuoteRouteNames, value: true });
    this.$router.push(QuoteProcessRouter.nextRoute(this.$route.name! as QuoteRouteNames))
  }

  created(): void {
    this.value = this.questionAnswers.tlc_license_years || ''
  }

  resetState(): void {
    this.value = '';
    this.updateQuestionAnswers({ tlc_license_years: undefined });
    this.updateStepStatus({ step: this.$route.name! as QuoteRouteNames, value: false });
  }

  beforeRouteEnter (to: Route, from: Route, next: any): void {
    next((vm: StepQuestionLongTlc) => {
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
