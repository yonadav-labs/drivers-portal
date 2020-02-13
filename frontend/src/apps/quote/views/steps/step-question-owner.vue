<template>
  <quote-process-layout>
    <quote-summary></quote-summary>
    <quote-process-radio-form :answers="answers" name="years" v-model="value" @next="onNext">
      Who owns this car?
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
import QuoteProcessLayout from '@/components/layout/quote-process-layout.vue'
import QuoteSummary from '@/apps/quote/components/containers/quote-summary.vue'

import { OrderedQuoteRouteName, QuoteProcessRouter, ExtraQuoteRouteNames } from '@/router/quote'

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
  stepCompletedByName!: (route: OrderedQuoteRouteName) => boolean

  @quote.Action
  updateStepStatus!: (payload: { step: string, value: boolean }) => void;

  @quote.Action
  updateQuestionAnswers!: (payload: QuestionsStep) => void;

  value = ''
  
  answers = [
    {
      label: 'I am the owner and the only driver of this car',
      value: 'owner-driver'
    },
    {
      label: 'I am the owner and there is only 1 additional driver for this policy.',
      value: 'owner-named'
    },
    {
      label: 'I am the owner and there are more than 1 additional drivers on this policy.',
      value: 'corporate-1'
    },
    {
      label: 'This car is owned by a fleet or LLC',
      value: 'corporate-2'
    },
    {
      label: 'Other',
      value: 'other'
    }
  ]
  

  onNext(): void {
    if (this.value === 'other') {
      this.$router.push({ name: ExtraQuoteRouteNames.SOFT_FALLOUT })
    } else {
      const finalValue = this.value.startsWith('corporate') ? 'corporate':this.value
      this.updateQuestionAnswers({ vehicle_owner: finalValue })
      this.updateStepStatus({ step: this.$route.name!, value: true });
      this.$router.push(QuoteProcessRouter.nextRoute(this.$route.name!))
    }

  }

  resetState(): void {
    this.value = '';
    this.updateQuestionAnswers({ vehicle_owner: undefined });
    this.updateStepStatus({ step: this.$route.name!, value: false });
  }

  created(): void {
    this.value = this.questionAnswers.vehicle_owner || ''
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
