<template>
  <modal @close="$emit('close')">
    <div class="modal-make-payment">
      <div class="modal-header">
        <span>Make payment</span>
      </div>
      <div class="modal-content">
        <div class="payment-info">
          <p class="form-explain">Payment Amount</p>
          <p class="payment-info--price">{{ paymentTotalAmount | currency }}</p>
          <p v-if="creditCardFormOpened" class="payment-info--price-detail">Credit Cart Fee: <span>{{ stripeFee }}</span></p>
          <p class="payment-info--price-detail">Hereford Fee: <span>{{ paymentFee | currency }}</span></p>
          <p class="payment-info--price-detail">Insurance Premium: <span>{{ paymentAmount | currency }}</span></p>
        </div>
        <div v-if="loading" class="spinner">
          Processing payment... Please, wait.
        </div>
        <div class="payment-error error-info" v-if="(hasError || fatalError || stripeError) && !loading">
          <p class="error-info--title">There was an error with your payment.</p>
          <p>{{ errorDisplay }}</p>
          <p v-if="stripeError">{{ !!stripeError.response ? stripeError.response.data[0]:stripeError.message }}</p>
          <p v-if="hasError && disabledBank && !fatalError">You can still pay with Credit Card</p>
        </div>
        <div class="form-container" v-if="!fatalError && !stripeError && !creditCardFormOpened && !loading">
          <p class="form-explain">How would you like to make the payment?</p>
          <form id="paymentForm">
            <div class="form-content form-content--pay">
              <pay-button text="Credit Card" :info="`${stripeFee} Fee`" @click.prevent="startPay()" color="#f76707">
              </pay-button>
              <plaid-button
                v-if="!disabledBank"
                @success="plaidHandler"
                @exit="plaidExitHandler"
                :onClick="startPlaid">
                <template v-slot:button="props">
                  <pay-button text="Bank" :info="`No Fee`" @click="props.onClick" color="#F76707">
                  </pay-button>
                </template>
              </plaid-button>
            </div>
          </form>
        </div>
        <credit-card-form
          v-show="!loading && !fatalError && !stripeError && creditCardFormOpened"
          :amount="paymentAmount + paymentFee + stripeFeeAmount"
          @success="onCreditSuccess"
          @error="onCreditError"
          @loading="loading = true"
        ></credit-card-form>
      </div>
    </div>
  </modal>
</template>

<script lang="ts">

import { Component, Vue, Prop } from 'vue-property-decorator';
import { Getter, Action, namespace } from 'vuex-class';

import { PolicyPayment } from '@/@types/policy'
import { StripeChargePayload, PlaidChargePayload } from '@/@types/payment'

import Modal from '@/components/modals/modal.vue'

import CreditCardForm from '@/components/forms/credit-card-form.vue'
import PayButton from '@/components/buttons/pay-button.vue'
import PlaidButton from '@/components/buttons/plaid-button.vue'

import ErrorMessage from '@/components/error-message.vue'

import { currency } from '@/utils/text'

const policy = namespace('Policy')

@Component({
  components: {
    Modal, CreditCardForm, PayButton, PlaidButton
  },
  filters: {
    currency
  }
})
export default class ModalMakePayment extends Vue {
  @Prop({ default: [] })
  payment!: PolicyPayment

  @policy.Getter
  stripeError?: Error | undefined

  @policy.Getter
  plaidError?: Error | undefined

  @policy.Action
  payPaymentStripe!: ({id, charge}: {id: string, charge: StripeChargePayload}) => void;

  @policy.Action
  payPaymentPlaid!: ({id, charge}: {id: string, charge: PlaidChargePayload}) => void;

  disabledBank = false
  error = false
  fatalError = false;
  errorDisplay = ''
  loading = false
  creditCardFormOpened = false;

  get hasError(): boolean {
    return this.error || !!this.stripeError || !!this.plaidError
  }

  get paymentAmount(): number {
    return !!this.payment ? this.payment.payment_amount:0
  }

  get paymentFee(): number {
    return this.payment.fee_amount
  }

  get stripeFeeAmount(): number {
   return this.payment.stripe_fee 
  }

  get plaidFeeAmount(): number {
   return this.payment.plaid_fee 
  }

  get stripeFee(): string {
    return currency(this.stripeFeeAmount)
  }

  get plaidFee(): string {
    return currency(this.plaidFeeAmount)
  }

  get paymentTotalAmount(): number {
    let total = this.paymentAmount + this.paymentFee
    if (this.creditCardFormOpened) {
      total += this.stripeFeeAmount
    }
    return total;
  }

  async plaidHandler({public_token, metadata}: {public_token: string, metadata: any}): Promise<void> {
    this.loading = true;
    await this.payPaymentPlaid({
      id: this.payment.id,
      charge: {
        public_token,
        account_id: metadata.account_id,
      }
    })
    if (!this.plaidError) {
      this.$emit('success')
    } else {
      this.disabledBank = true;
    }
    this.loading = false;
  }

  plaidExitHandler({ result, err, metadata }: { result: string, err: any, metadata: any }): void {
    if (result==='plaid_error') {
      this.disabledBank = true;
      this.loading = false;
      this.error = true;
      this.errorDisplay = 'There was an error paying with Bank'
    }
  }

  startPlaid(): void {
    // pass
  }

  startPay(): void {
    this.creditCardFormOpened = true;
  }

  onCreditError(): void {
    this.error = true;
    this.fatalError = true;
    this.loading = false;
  }

  async onCreditSuccess(payload: StripeChargePayload): Promise<void> {
    await this.payPaymentStripe({id: this.payment.id, charge: payload})
    if (!this.stripeError) {
      this.$emit('success')
    }
    this.loading = false;
  }
}
</script>

<style lang="scss" scoped>
.modal-make-payment {
  background-color: $white;
  border-radius: 8px;
  box-shadow: 0 10px 20px 0 rgba(206,212,218,0.4);
  max-width: 36.875rem;
  min-height: 21.25rem;
  padding: 0.625rem;
  width: calc(100vw - 8rem);
  z-index: 1;

  .modal-header {
    background-color: $blue;
    background-image: url("~@/assets/headerModal.png");
    background-repeat: no-repeat;
    background-size: cover;
    border-radius: 4px;
    color: $white;
    padding: 1rem;
    text-align: center;

    span {
      color: $white;
      font-size: $fs-lg;
      font-weight: $fw-semibold;
    }
  }
  .modal-content {
    max-height: calc(100vh - 1rem);
    overflow-y: auto;
  }
}

.form-container {
  text-align: center;
  
  .form-explain {
    line-height: 1.5;
    font-size: $fs-lg;
    margin-left: auto;
    margin-right: auto;
    margin-top: 1rem;
    span {
      font-weight: $fw-semibold;
    }
  }
}

.form-content--pay{
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
  margin-top: 1.25rem;
}

.payment-info {
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-top: 1.8rem;
  span {
    font-size: $fs-lg;
  }
  p {
    text-align: center;
    &.payment-info--price {
      color: $blue;
      font-size: $fs-xxl;
      font-weight: $fw-semibold;
      margin-top: 1rem;
      margin-bottom: 1rem;
    }

    &.payment-info--price-detail {
      font-size: $fs-md;
      font-weight: $fw-semibold;
      margin-bottom: 0.25rem;

      span {
        font-size: $fs-md;
        font-weight: $fw-semibold;
        color: $blue;
      }
    }
  }
  .payment-info--date {
    background-color: $grey-light;
    font-size: $fs-sm;
    margin: 0 auto;
    opacity: 0.5;
    padding: 0.5rem;
  }
}
.error-info {
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin: 1.875rem auto 1.25rem;
  width: 24rem;

  span {
    font-size: $fs-lg;
  }

  p {
    font-size: $fs-lg;
    line-height: 1.56;
    text-align: center;
    &.error-info--title {
      font-weight: $fw-bold;
    }
  }
}

.spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 22.5rem;
}

.or-separator {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
}
</style>