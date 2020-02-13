<template>
  <quote-process-layout>
    <quote-summary></quote-summary>
    <div class='question-container'>
        <p class='question-container__explain'>Please select all that apply to you</p>
        <form id='checkForm' @submit.prevent.stop="onNext">
          <div class="question-content">
            <checkbox
              class="question-content__radio"
              name="dwi_36_months"
              :value="true"
              v-model="dwi_36_months"
              @change="onNotNone"
            >
              <span>I have had a DWI or DUI violation within the past 36 months</span>
            </checkbox>
            <checkbox
              class="question-content__radio"
              name="fault_accident_pedestrian"
              :value="true"
              v-model="fault_accident_pedestrian"
              @change="onNotNone"
            >
              <span>I have had an at fault accident w/ pedestrian/bicyclist 24 months </span>
            </checkbox>
            <checkbox
              class="question-content__radio"
              name="speeding_violation"
              :value="true"
              v-model="speeding_violation"
              @change="onNotNone"
            >
              <span>I have had a speeding violation > 30 MPH within the last 24 months</span>
            </checkbox>
            <checkbox
              class="question-content__radio"
              name="none_above"
              :value="true"
              v-model="none_above"
              @change="onNone"
            >
              <span>None of the above</span>
            </checkbox>
          </div>
          <basic-button
            text='Next Step'
            :disabled="!anyAnswered"
            :color='colorBlue'
            >
            <icon-arrow-right size='16' class='icon--blue'></icon-arrow-right>
          </basic-button>
      </form>
    </div>
  </quote-process-layout>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';

import { Getter, Action, namespace } from 'vuex-class';
import { Route } from 'vue-router';

import { QuestionsStep } from '@/@types/quote';

import BasicButton from '@/components/buttons/basic-button.vue'
import Checkbox from '@/components/inputs/checkbox.vue'
import IconArrowRight from '@/components/icons/icon-arrow-right.vue'
import QuoteProcessLayout from '@/components/layout/quote-process-layout.vue'
import QuoteSummary from '@/apps/quote/components/containers/quote-summary.vue'


import { OrderedQuoteRouteName, QuoteProcessRouter } from '@/router/quote'

import { Colors } from '@/utils/colors'

// Question Step 

const quote = namespace('Quote')

@Component({
  components: {
    BasicButton, QuoteProcessLayout, Checkbox, QuoteSummary, IconArrowRight
  }
})
export default class StepQuestionLongDwi extends Vue {
  @quote.Getter
  questionAnswers!: QuestionsStep;

  @quote.Getter
  stepCompletedByName!: (route: OrderedQuoteRouteName) => boolean

  @quote.Action
  updateStepStatus!: (payload: { step: string, value: boolean }) => void;

  @quote.Action
  updateQuestionAnswers!: (payload: QuestionsStep) => void;

  dwi_36_months: string | boolean = ''; // FIX THIS
  fault_accident_pedestrian: string | boolean = ''; // FIX THIS
  speeding_violation: string | boolean = ''; // FIX THIS
  none_above: string | boolean = ''; // FIX THIS

  get anyAnswered(): boolean {
    return !!this.dwi_36_months || !!this.fault_accident_pedestrian || !!this.speeding_violation || !!this.none_above
  }

  get colorBlue(): string {
    return Colors.Blue
  }

  onNext(): void {
    this.updateQuestionAnswers({ dwi_36_months: !!this.dwi_36_months });
    this.updateQuestionAnswers({ fault_accident_pedestrian: !!this.fault_accident_pedestrian });
    this.updateQuestionAnswers({ speeding_violation: !!this.speeding_violation });
    this.updateStepStatus({ step: this.$route.name!, value: true });
    this.$router.push(QuoteProcessRouter.nextRoute(this.$route.name!))
  }

  onNotNone(val: boolean): void {
    this.none_above = '';
  }

  onNone(val: boolean): void {
    if (val === true) {
      this.dwi_36_months = ''
      this.fault_accident_pedestrian = ''
      this.speeding_violation = ''
    }
  }

  created(): void {
    this.dwi_36_months = this.questionAnswers.dwi_36_months || ''
    this.fault_accident_pedestrian = this.questionAnswers.fault_accident_pedestrian || ''
    this.speeding_violation = this.questionAnswers.speeding_violation || ''
  }

  resetState(): void {
    this.dwi_36_months = ''
    this.fault_accident_pedestrian = ''
    this.speeding_violation = ''
    this.none_above = ''
    this.updateQuestionAnswers({ dwi_36_months: undefined });
    this.updateQuestionAnswers({ fault_accident_pedestrian: undefined });
    this.updateQuestionAnswers({ speeding_violation: undefined });
    this.updateStepStatus({ step: this.$route.name!, value: false });
  }

  beforeRouteEnter (to: Route, from: Route, next: any): void {
    next((vm: StepQuestionLongDwi) => {
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
      text-align: left;

      &:not(:last-child) {
        margin-bottom: 1.25rem;
      }
    }
  }
}
</style>
