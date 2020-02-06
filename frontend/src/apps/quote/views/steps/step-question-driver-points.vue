<template>
  <quote-process-layout>
    <quote-summary></quote-summary>
    <quote-process-radio-form :answers="answers" name="years" v-model="value" @next="onNext">
      How many driver points do you have in the last 36 months? 
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

import { QuoteRouteNames, QuoteProcessRouter } from '@/router/quote'

// Question Step 

const quote = namespace('Quote')

@Component({
  components: {
    QuoteProcessLayout, QuoteProcessRadioForm, QuoteSummary
  }
})
export default class StepQuestionDriverPoints extends Vue {

  @quote.Getter
  questionAnswers!: QuestionsStep;

  @quote.Getter
  stepCompletedByName!: (route: QuoteRouteNames) => boolean

  @quote.Action
  updateStepStatus!: (payload: { step: string, value: boolean }) => void;

  @quote.Action
  updateQuestionAnswers!: (payload: QuestionsStep) => void;

  value = ''
  
  answers = [
    {
      label: '0-6',
      value: '0-6'
    },
    {
      label: '7-10',
      value: '7-10'
    },
    {
      label: '10+',
      value: '10+'
    }
  ]

  onNext(): void {
    this.updateQuestionAnswers({ driver_points_last_months: this.value })
    this.updateStepStatus({ step: this.$route.name!, value: true });
    this.$router.push(QuoteProcessRouter.nextRoute(this.$route.name!))
  }

  resetState(): void {
    this.value = '';
    this.updateQuestionAnswers({ driver_points_last_months: undefined });
    this.updateStepStatus({ step: this.$route.name!, value: false });
  }

  created(): void {
    this.value = this.questionAnswers.driver_points_last_months || ''
  }

  beforeRouteEnter (to: Route, from: Route, next: any): void {
    next((vm: StepQuestionDriverPoints) => {
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
