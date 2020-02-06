<template>
  <div>
    <p class="form-info form-explain" v-if="showTLC">TLC license number {{ tlcStepLicenseName.tlc_number }}</p>
    <div class="divider" v-if="showTLC"></div>
    <p class="form-info form-explain form-info--capitalize" v-if="showName">{{ driverName }}</p>
    <div class="divider" v-if="showName"></div>
    <p
      class="form-info form-explain"
      v-if="showVIN"
    >VIN # {{ fhvInfo.vehicle_vin }} – Vehicle License Plate # {{ fhvInfo.license_plate }}</p>
    <div class="divider" v-if="showVIN"></div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import { Getter, namespace } from 'vuex-class';

import { TLCStepLicenseName, VINStepFHVInfo } from '@/@types/quote';

import { QuoteRouteNames, QuoteProcessRouter } from '@/router/quote'

import { capitalize } from '@/utils/text'

const quote = namespace('Quote')
const quoteTLC = namespace('QuoteTlc')
const quoteVIN = namespace('QuoteVin')

@Component
export default class QuoteSummary extends Vue {
 
  @quoteTLC.Getter
  tlcStepLicenseName?: TLCStepLicenseName

  @quoteVIN.Getter
  fhvInfo?: VINStepFHVInfo

  @quote.Getter
  stepCompletedByName!: (step: string) => boolean

  get driverName(): string {
    return !!this.tlcStepLicenseName ? capitalize(this.tlcStepLicenseName.tlc_name):''
  }

  get showTLC(): boolean {
    return !!this.tlcStepLicenseName && !!this.tlcStepLicenseName.tlc_number
  }

  get showName(): boolean {
    return this.stepCompletedByName(QuoteRouteNames.TLC)
  }

  get showVIN(): boolean {
    return this.stepCompletedByName(QuoteRouteNames.VIN)
  }
}
</script>

<style lang="scss">
p {
  font-weight: $fw-light;
  text-align: center;

  &.form-info {
    color: $grey-darker;
    font-size: $fs-md;
    margin-top: 1rem;

    &.form-info--capitalize {
      text-transform: capitalize;
    }
  }
  &.form-question {
    color: $blue-dark;
    margin-top: 1.75rem;
    span {
      text-transform: capitalize;
    }
  }
}
.form-explain {
  line-height: 1.5;
  font-size: $fs-lg;
  margin-left: auto;
  margin-right: auto;
  span {
    font-weight: $fw-semibold;
  }
}

.divider {
  border-top: 2px dashed $grey-medium;
  margin: 1rem 0;
  width: 100%;

  &:last-child {
    margin-bottom: 0.25rem;
  }
}
</style>
