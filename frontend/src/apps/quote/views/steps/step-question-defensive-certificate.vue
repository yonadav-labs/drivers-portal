<template>
  <quote-process-layout>
    <quote-summary></quote-summary>
    <quote-process-yes-no-form @yes="yes" @no="no">
      Do you have a defensive driving certificate completed over the last 3 years? 
    </quote-process-yes-no-form>
  </quote-process-layout>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';

import { Action, namespace } from 'vuex-class';
import { Route } from 'vue-router';

import { QuestionsStep } from '@/@types/quote';

import QuoteProcessYesNoForm from '@/apps/quote/components/forms/quote-process-yes-no-form.vue'
import QuoteProcessLayout from '@/components/layout/quote-process-layout.vue'
import QuoteSummary from '@/apps/quote/components/containers/quote-summary.vue'

import { OrderedQuoteRouteName, QuoteProcessRouter } from '@/router/quote'

// Question Step 

const quote = namespace('Quote')

@Component({
  components: {
    QuoteProcessLayout, QuoteProcessYesNoForm, QuoteSummary
  }
})
export default class StepQuestionDefensiveCertificate extends Vue {
  @quote.Getter
  stepCompletedByName!: (route: OrderedQuoteRouteName) => boolean

  @quote.Action
  updateStepStatus!: (payload: { step: string, value: boolean }) => void;

  @quote.Action
  updateQuestionAnswers!: (payload: QuestionsStep) => void;

  yes(): void {
    this.updateQuestionAnswers({ defensive_driving_certificate: true })
    this.next()
  }

  no(): void {
    this.updateQuestionAnswers({ defensive_driving_certificate: false })
    this.next()
  }

  resetState(): void {
    this.updateQuestionAnswers({ defensive_driving_certificate: undefined });
    this.updateStepStatus({ step: this.$route.name!, value: false });
  }

  next(): void {
    this.updateStepStatus({ step: this.$route.name!, value: true });
    this.$router.push(QuoteProcessRouter.nextRoute(this.$route.name!))
  }

  beforeRouteEnter (to: Route, from: Route, next: any): void {
    next((vm: StepQuestionDefensiveCertificate) => {
      vm.resetState();
      
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
