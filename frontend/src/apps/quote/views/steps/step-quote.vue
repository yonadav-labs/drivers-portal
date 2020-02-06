<template>
  <quote-process-columns-layout>
    <quote-summary></quote-summary>
    <div class="questions">
      <banner
        title="Physical Coverage"
        text="If you want Physical (Collision and Comprehensive) Coverage, please select your desired Deductible."
        :active="focus=='physical'"
        :info="true"
      >
        <basic-select
          v-model="internalPhysical"
          :selected="internalPhysical"
          :options="PHYSICAL_OPTIONS"
          :no-value="true"
          @focus="focus='physical'"
        ></basic-select>
      </banner>
      <div class="divider"></div>
      <banner
        title="Add Deposit"
        text="Choose the the deposit amount you would like to pay. This is due immediately."
        :active="focus=='deposit'"
      >
        <basic-select
          v-model="internalDeposit"
          :selected="internalDeposit"
          :options="DEPOSIT_OPTIONS"
          :disabled="internalPhysical == ''"
          @focus="focus='deposit'"
        ></basic-select>
      </banner>
      <div class="divider"></div>
      <banner
        title="When would you like your policy to start? "
        text="Choose a date up to 20 days in advance."
        :active="focus=='date'"
      >
        <input-datepicker
          class="input"
          placeholder="Select date"
          v-model="internalDate"
          :disabled-dates="disabledDates"
          format="MMM d yyyy"
          :disabled="internalPhysical == '' || internalDeposit == ''"
          @focus="focus='date'">
        </input-datepicker>
      </banner>
      <div class="divider"></div>
      <banner
        title="Your insurance includes"
        text="The following coverages are mandated by the NYC Taxi & Limousine Commission."
      ></banner>
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
        <div class="insurance-text">
          <span>Liability</span>
          <span>$380</span>
        </div>
        <div class="insurance-text">
          <div>
            <span>Physical coverage</span>
            <span class="insurance-price">Deductible $750</span>
          </div>
          <span
            v-if="internalPhysical != '' && internalPhysical != 'no'"
          >$300</span>
          <span v-else-if="internalPhysical == 'no'">$0</span>
          <span v-else>$-</span>
        </div>
        <div class="insurance-text insurance-text--total">
          <span>Total</span>
          <span>$450</span>
          <!-- <span>${{formatNumber(variations.liabilityTotal)}}</span> -->
        </div>
        <a href class="insurance-info--question">
          <icon-info size="16" class="insurance-info__icon icon--blue"></icon-info>How is my premium calculated?
        </a>
      </div>

      <div class="insurance-resume">
        <div class="insurance-estimated">
          <p>Monthly payment</p>
          <p class="estimated-price">$1000</p>
          <span class="estimated-date">First Payment Due
            <br>
            Oct. 7, 2019
          </span>
        </div>
        <div class="insurance-estimated">
          <p>Deposit</p>
          <p class="estimated-price">$125</p>
          <span class="estimated-date">20% of total price</span>
        </div>
      </div>
      <button
        class="insurance-action"
        :class="{'active': internalPhysical != '' && internalDeposit != '' && internalDate != ''}"
        :disabled="internalPhysical == '' || internalDeposit == '' || internalDate == ''"
      >Get Your Insurance Policy!
        <icon-arrow-right class="icon" size="16"></icon-arrow-right>
      </button>
    </div>
  </quote-process-columns-layout>
</template>

<script lang="ts">
import { Component, Vue, Watch, Prop } from 'vue-property-decorator';

import { Getter, Action, namespace } from 'vuex-class';

import { Route } from 'vue-router';

import { addDays } from 'date-fns';

import Banner from '@/components/containers/banner.vue'
import BasicButton from '@/components/buttons/basic-button.vue'
import BasicSelect from '@/components/inputs/basic-select.vue'
import DropdownInfo from '@/components/containers/dropdown-info.vue'
import IconArrowRight from '@/components/icons/icon-arrow-right.vue'
import IconInfo from '@/components/icons/icon-info.vue'
import InputDatepicker from '@/components/inputs/input-datepicker.vue'
import QuoteProcessColumnsLayout from '@/apps/quote/components/layout/quote-process-columns-layout.vue'
import QuoteSummary from '@/apps/quote/components/containers/quote-summary.vue'

import { QuoteRouteNames, QuoteProcessRouter } from '@/router/quote'


const quote = namespace('Quote')

// Ninth Step 
@Component({
  components: {
    Banner, BasicButton, BasicSelect, DropdownInfo, InputDatepicker, QuoteProcessColumnsLayout,
    IconArrowRight, IconInfo, QuoteSummary
  }
})
export default class StepQuote extends Vue {

  @Prop({ default: ''})
  quoteId!: string

  @quote.Getter
  quoteProcessId?: string

  @quote.Action
  retrieveQuoteProcess!: (id: string) => Promise<void>

  DEPOSIT_OPTIONS = [
    {
      text: 'No',
      value: 'no'
    },
    {
      text: '15%',
      value: '15'
    },
    {
      text: '20%',
      value: '20'
    },
    {
      text: '25%',
      value: '25'
    }
  ]

  PHYSICAL_OPTIONS = [
    {
      text: 'No',
      value: 'no'
    },
    {
      text: '$750',
      value: '750'
    },
    {
      text: '$1,000',
      value: '1000'
    },
    {
      text: '$1,500',
      value: '1500'
    }
  ]

  internalPhysical = ''
  internalDeposit = ''
  internalDate = ''
  
  disabledDates = {
    to: new Date(),
    from: addDays(new Date(), 20)
  }

  focus = 'physical'

  @Watch('internalPhysical')
  onPhysicalChange(val: string): void {
    if (!!val) {
      this.focus = 'deposit'
    }
  }

  @Watch('internalDeposit')
  onDepositChange(val: string): void {
    if (!!val) {
      this.focus = 'date'
    }
  }

  async beforeRouteEnter (to: Route, from: Route, next: any): Promise<void> {
    next(async (vm: StepQuote) => {
      if (!vm.quoteId) {
        vm.$router.replace(QuoteProcessRouter.getRouteByOrder(0))
      } else {
        await vm.retrieveQuoteProcess(vm.quoteId);
        if (!vm.quoteProcessId) {
          vm.$router.replace(QuoteProcessRouter.getRouteByOrder(0))
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
}
</style>
