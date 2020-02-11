<template>
  <quote-process-columns-layout v-if="!!quoteProcessPayment" :hide-breadcrumbs="true" :on-back="back">
    <quote-summary></quote-summary>
    <div class="questions">
      <div class="questions__result">
        <p class="questions__title">Physical Coverage</p>
        <p class="questions__value">{{ !!quoteDeductible ? `$${quoteDeductible}`:'No' }}</p>
      </div>
      <div class="divider"></div>
      <div class="questions__result">
        <p class="questions__title">Deposit</p>
        <p class="questions__value">{{ quoteDeposit }}%</p>
      </div>
      <div class="divider"></div>
      <div class="questions__result">
        <p class="questions__title">Desired Policy Start Date</p>
        <p class="questions__value">{{ formatDate(quoteStartDate) }}</p>
      </div>
      <div class="divider"></div>
      <dropdown-info
        title="Bodily injury"
        price="$100,000 - $300,000"
      >
        Bodily Injury Liability insurance pays for injuries you cause to another driver if you are at-fault in the accident.
      </dropdown-info>
      <dropdown-info
        title="Property damage"
        price="$100,000"
      >
        Property Damage Liability insurance pays for damages to someone else's property after an accident you cause.
      </dropdown-info>
      <dropdown-info
        title="Uninsured motorist"
        price="$25,000 - $50,000"
      >
        Uninsured Motorist insurance pays you damages for any injury recieved from an uninsured, negligent driver.
      </dropdown-info>
      <dropdown-info
        title="Personal injury protection"
        price="$200,000"
      >
        Personal Injury Protection insurance covers medical expenses and can cover lost wages.
      </dropdown-info>
      <dropdown-info
        title="Aggregate no-fault"
        price="$200,000"
      >
        Aggregate No-Fault insurance can cover medical expensive and lost wages. As no fault insurance, because it is available regardless of who caused the accident.
      </dropdown-info>
    </div>
    <div slot="right-column">
      <div class="insurance-info">
        <p class="insurance-title">Your insurance</p>
        <div class="insurance-text" v-if="!!liability">
          <span>Liability</span>
          <span>{{ liability }}</span>
        </div>
        <div class="insurance-text" v-if="hasDeductible">
          <div>
            <span>Physical coverage</span>
            <span class="insurance-price" v-if="!!quoteDeductible">Deductible {{ quoteDeductible | currency }}</span>
          </div>
          <span
            v-if="hasDeductible"
          >{{ physicalAmount| currency }}</span>
          <span v-else-if="quoteDeductible == 0">$0</span>
          <span v-else>$--</span>
        </div>
        <div class="insurance-text insurance-text--total">
          <span>Total</span>
          <span>{{ total | currency }}</span>
        </div>
        <a href class="insurance-info--question" @click.prevent.stop="setShowPremium(true)">
          <icon-info size="16" class="insurance-info__icon icon--blue"></icon-info>How is my premium calculated?
        </a>
      </div>

      <div class="insurance-resume">
        <div class="insurance-estimated">
          <p>Monthly payment</p>
          <p class="estimated-price">{{ monthlyPaymentText }}<sup v-if="herefordFee">+{{ herefordFee | beautyCurrency }}</sup></p>
          <span class="estimated-date">9 payments starting on
            <br>
            {{ firstPaymentDue }}
          </span>
        </div>
        <div class="insurance-estimated">
          <p>Deposit</p>
          <p class="estimated-price">{{ depositText }}</p>
          <span class="estimated-date">{{ quoteDeposit ? `${quoteDeposit}%`:'--%' }} of total price</span>
        </div>
      </div>
      <button
        class="insurance-action active"
        @click="pay"
      >Pay {{ deposit | beautyCurrency }}
        <icon-arrow-right class="icon" size="16"></icon-arrow-right>
      </button>
    </div>
    <modal-premium 
      v-if="!!quoteProcess && showPremium"
      :tlc-name="quoteProcess.tlc_name"
      :tlc-number="quoteProcess.tlc_number"
      :has-defensive="quoteProcess.defensive_driving_certificate"
      :points="quoteProcess.driver_points_last_months"
      :accidents="quoteProcess.fault_accidents_last_months"
      :vehicle-vin="quoteProcess.vehicle_vin"
      :vehicle-owner="quoteProcess.vehicle_owner"
      :vehicle-plate="quoteProcess.license_plate"
      :vehicle-year="quoteProcess.vehicle_year"
      :base-name="quoteProcess.base_name"
      :base-number="quoteProcess.base_number"
      :insurance-name="quoteProcess.insurance_carrier_name"
      :insurance-policy="quoteProcess.insurance_policy_number"
      :deposit-option="quoteDeposit"
      :deductible-option="quoteDeductible"
      :total="total"
      :monthly-payment="monthlyPayment"
      :deposit="deposit"
      :first-payment-due="firstPaymentDue"

      @close="setShowPremium(false)"
      ></modal-premium>
  </quote-process-columns-layout>
</template>

<script lang="ts">
import { Component, Vue, Watch, Prop } from 'vue-property-decorator';

import { Getter, Action, namespace } from 'vuex-class';

import { Route } from 'vue-router';

import { addDays, addMonths, format } from 'date-fns';

import BasicButton from '@/components/buttons/basic-button.vue'
import DropdownInfo from '@/components/containers/dropdown-info.vue'
import IconArrowRight from '@/components/icons/icon-arrow-right.vue'
import IconInfo from '@/components/icons/icon-info.vue'
import InputDatepicker from '@/components/inputs/input-datepicker.vue'
import ModalPremium from '@/apps/quote/components/modals/modal-premium.vue'
import QuoteProcessColumnsLayout from '@/apps/quote/components/layout/quote-process-columns-layout.vue'
import QuoteSummary from '@/apps/quote/components/containers/quote-summary.vue'

import { RouteName } from '@/router'
import { OrderedQuoteRouteName, QuoteProcessRouter } from '@/router/quote'

import { QuoteProcess, QuoteProcessPayment } from '@/@types/quote';
import { User } from '@/@types/users';

import { currency, beautyCurrency } from '@/utils/text'
import { getHerefordFee } from '@/utils/quote'

const quote = namespace('Quote')
const quotePayment = namespace('QuotePayment')
const users = namespace('Users')

// Ninth Step 
@Component({
  components: {
    BasicButton, DropdownInfo, InputDatepicker, QuoteProcessColumnsLayout,
    IconArrowRight, IconInfo, QuoteSummary, ModalPremium
  },
  filters: {
    currency, beautyCurrency
  }
})
export default class StepQuote extends Vue {

  @Prop({ default: ''})
  quoteId!: string

  @quote.Getter
  quoteProcess?: QuoteProcess

  @quote.Getter
  quoteProcessId?: string

  @quotePayment.Getter
  quoteProcessPayment?: QuoteProcessPayment

  @users.Getter
  user?: User

  @quote.Action
  retrieveDeconstructQuoteProcess!: (id: string) => Promise<void>

  @quotePayment.Action
  retrieveQuoteProcessPayment!: () => Promise<void>
  
  disabledDates = {
    to: new Date(),
    from: addDays(new Date(), 20)
  }

  showPremium = false;

  get hasDeductible(): boolean {
    return !!this.quoteProcess!.deductible;
  }

  get monthlyPayment(): number {
    return (this.total * (1-(this.quoteDeposit/100)))/9;
  }

  get quoteDeductible(): number {
    return !!this.quoteProcess && !!this.quoteProcess.deductible ? this.quoteProcess.deductible:0
  }

  get quoteDeposit(): number {
    return !!this.quoteProcess ? this.quoteProcess.deposit!:0
  }

  get quoteStartDate(): string {
    return !!this.quoteProcess ? this.quoteProcess.start_date!:''
  }

  get deposit(): number {
    return this.total * (this.quoteDeposit/100)
  }

  get herefordFee(): number {
    return !!this.quoteDeposit ? getHerefordFee(this.quoteDeposit):0;
  }

  get depositText(): string {
    return this.quoteDeposit ? beautyCurrency(this.deposit):'$--'
  }

  get firstPaymentDue(): string {
    if (!this.quoteStartDate) {
      return '--'
    }
    const selectedDate = new Date(this.quoteStartDate)
    return this.formatDate(addMonths(selectedDate, 3))
  }

  get liability(): string {
    return !!this.quoteProcessPayment && !!this.quoteProcessPayment.liability_amount ? currency(Number(this.quoteProcessPayment.liability_amount)):'0'
  }

  get monthlyPaymentText(): string {
    return this.quoteDeposit ? beautyCurrency(this.monthlyPayment):'$--'
  }

  get physicalAmount(): number {
    return !!this.quoteProcessPayment!.physical_amount ? Number(this.quoteProcessPayment!.physical_amount):0
  }
  
  get total(): number {
    return !!this.quoteProcessPayment ? Number(this.quoteProcessPayment.official_hereford_quote):0
  }

  back(): void {
    this.$router.push({ name: RouteName.DASHBOARD })
  }

  formatDate(date: Date | string): string {
    return format(new Date(date), 'MMM d, yyyy')
  }

  async pay(): Promise<void> {
  
  }

  setShowPremium(value: boolean): void {
    this.showPremium = value;
  }
  async beforeRouteEnter (to: Route, from: Route, next: any): Promise<void> {
    next(async (vm: StepQuote) => {
      if (!vm.quoteId || !vm.user) {
        vm.$router.replace(QuoteProcessRouter.getRouteByOrder(0))
      } else {
        if (!vm.quoteProcess) {
          await vm.retrieveDeconstructQuoteProcess(vm.quoteId);
          if (!vm.quoteProcess) {
            vm.$router.replace(QuoteProcessRouter.getRouteByOrder(0))
          }
        }
        if (!vm.quoteProcessPayment) {
          await vm.retrieveQuoteProcessPayment();
          if (!vm.quoteProcessPayment) {
            vm.$router.replace(QuoteProcessRouter.getRouteByOrder(0))
          }
        }
      }
    })
  }
}
</script>

<style lang='scss' scoped>
.divider {
  border-top: 2px dashed $grey-medium;
  margin: 1rem 0;
  width: 100%;
}

 .insurance-info {
  font-size: $fs-lg;
  padding: 1.875rem;

  .insurance-info--question {
    color: $blue;
    display: flex;
    font-weight: $fw-semibold;
    font-size: $fs-md;
  }

  .insurance-info__icon {
    margin-right: 0.5rem;
  }
}
.insurance-resume {
  background-color: rgba(241, 243, 245, 0.92);
  display: flex;
  justify-content: space-between;
  padding: 1.25rem;
  .insurance-estimated {
    background-color: $white;
    border-radius: 2px;
    text-align: center;
    display: flex;
    flex-direction: column;
    padding: 1rem 0.875rem 0.875rem;
    width: 9.813rem;
    span {
      font-size: $fs-lg;
    }
    p {
      text-align: center;
      &.estimated-price {
        color: $blue;
        font-size: $fs-xl;
        font-weight: $fw-semibold;
        margin-top: 1rem;
        margin-bottom: 1rem;

        sup {
          font-size: $fs-sm;
          font-weight: $fw-semibold;
        }
      }
    }
    .estimated-date {
      background-color: $grey-light;
      font-size: $fs-sm;
      margin: 0 auto;
      opacity: 0.5;
      padding: 0.5rem;
    }
  }
}
.insurance-action {
  background-color: $grey;
  border-radius: 0 0 8px 8px;
  color: $white;
  cursor: not-allowed;
  display: flex;
  justify-content: center;
  font-size: $fs-md;
  font-weight: $fw-semibold;
  text-align: center;
  text-decoration: none;
  padding: 1rem 0;
  width: 100%;
  .icon {
    color: $white;
    margin-left: 1rem;
  }
  &.active {
    background-image: linear-gradient(105deg, #fca011, #f76707);
    cursor: pointer;
  }
}
.insurance-title {
  font-size: $fs-md;
  font-weight: $fw-semibold;
  line-height: 1.22;
  text-transform: uppercase;
  padding-bottom: 1.875rem;
}
.insurance-text {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.25rem;
  > div {
    display: flex;
    flex-direction: column;
  }
  .insurance-price {
    color: $grey-darker;
    font-size: $fs-md;
    padding-top: 0.5rem;
  }
  &.insurance-text--total {
    span {
      font-weight: $fw-bold;
      line-height: 22px;
    }
  }
}

.questions {
  margin-top: 1rem;

  .questions__result {
    align-items: center;
    display: flex;
    justify-content: space-between;
    padding: 0.25rem 1.25rem;

    .questions__title {
      color:$blue-dark;
      font-size: $fs-lg;
      font-weight: $fw-bold;
      line-height: 1.22;
    }
  }
}
</style>
