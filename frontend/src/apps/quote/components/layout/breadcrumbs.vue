<template>
  <div class="steps-content">
    <div
      v-for="step in filteredSteps"
      :key="step"
      :id="step"
      :class="{'active': currentStep == step, 'done' : isDone(step)}"
      class="step"
    >
      <p>{{stepName(step)}}</p>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import { QuoteRouteNames, QuoteProcessRouter } from '@/router/quote'

@Component
export default class Breadcrumbs extends Vue {
  get currentStep(): string {
    return this.$route.name!
  }

  steps = [
      QuoteRouteNames.TLC,
      QuoteRouteNames.VIN,
      QuoteRouteNames.QUESTION_LONG_TLC,
      QuoteRouteNames.QUESTION_LONG_DMV,
      QuoteRouteNames.QUESTION_DRIVER_POINTS,
      QuoteRouteNames.QUESTION_FAULT_ACCIDENTS,
      QuoteRouteNames.QUESTION_DEFENSIVE_CERTIFICATE,
      QuoteRouteNames.QUESTION_ACCIDENT_AVOIDANCE,
      QuoteRouteNames.EMAIL,
      QuoteRouteNames.QUOTE,
  ]

  groupedSteps = [
    QuoteRouteNames.QUESTION_LONG_TLC,
    QuoteRouteNames.QUESTION_LONG_DMV,
    QuoteRouteNames.QUESTION_DRIVER_POINTS,
    QuoteRouteNames.QUESTION_FAULT_ACCIDENTS,
    QuoteRouteNames.QUESTION_DEFENSIVE_CERTIFICATE,
    QuoteRouteNames.QUESTION_ACCIDENT_AVOIDANCE,
  ]

  get filteredSteps(): string[] {
    return this.steps.filter(this.showStep)
  }

  showStep(step: string): boolean {
    const isCurrent = this.currentStep === step

    if (isCurrent) {
      return true;
    } else {
      const isGrouped = this.groupedSteps.includes(step as QuoteRouteNames)
      const currentIsGrouped = this.groupedSteps.includes(this.currentStep as QuoteRouteNames)

      return !isGrouped || (!currentIsGrouped && step === this.groupedSteps[0])
    }
  }

  stepName(step: string): string {
    return QuoteProcessRouter.getRouteTitle(step)
  }

  isDone(step: string): boolean {
    return QuoteProcessRouter.isLater(this.currentStep, step);
  }
}
</script>

<style lang="scss">
$device-desktop: 900px;
$desktop-up: "(min-width: #{$device-desktop})";
.steps-content {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;

  @media #{$desktop-up} {
    display: block;
    margin-bottom: 0;
    position: absolute;
    left: -1.25rem;
    //width: 7.75rem;
    transform: translateX(-100%);
  }
  .step {
    border-bottom-style: solid;
    border-bottom-color: $grey;
    border-bottom-width: 4px;
    display: flex;
    flex: 1;
    height: 2.5rem;
    margin: 0 0.5rem 0.25rem 0.5rem;
    @media #{$desktop-up} {
      border-bottom: none;
      border-right-style: solid;
      border-right-color: $grey;
      border-right-width: 4px;
      margin: 0 0 0.25rem 0;
    }
    &:first-child {
      margin-left: 0;
    }
    &:last-child {
      margin-right: 0;
    }
    &.active {
      border-bottom-color: $blue;
      @media #{$desktop-up} {
        border-right-color: $blue;
      }
      p {
        color: $blue;
        display: block;
        font-weight: $fw-bold;
      }
    }
    &.done{
      border-bottom: 4px solid $blue;
      @media #{$desktop-up} {
        border-bottom: none;
        border-right: 4px solid $blue;
      }
      p{
        color:$blue;
      }
    }
    &:hover {
      p {
        display: block;
      }
    }

    p {
      align-self: center;
      color: $grey;
      display: none;
      font-size: $fs-xs;
      text-align: center;
      padding-left: 0.5rem;
      padding-right: 0.5rem;
      width: 100%;
      @media #{$desktop-up} {
        padding-left: 0;
        padding-right: 1rem;
        text-align: right;
      }
    }
  }
}
</style>
