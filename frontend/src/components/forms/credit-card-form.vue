<template>
  <div>
    <div v-if="loading" class="spinner">
      <!-- <calculate-spinner :completedSteps="9" :total-steps="6"></calculate-spinner> -->
    </div>
    <div class="payment-error error-info" v-if="error">
      <p class="error-info--title">There was an error with your payment.</p>
      <p>{{ errorDisplay }}</p>
    </div>

    <form id="creditCardForm" v-if="!error" v-show="!loading">
      <div class="payment-action">
        <div>
          <p>Name</p>
          <basic-input
            id="nameField"
            type="text"
            placeholder="Your name here"
            @keyup="submitted = false"
            :error="submitted && !$v.form.name.required"
            v-model="$v.form.name.$model"
            icon="user"
          >
            <span
              class="error"
              v-if="submitted && !$v.form.name.required"
              slot="error"
            >Name is required</span>
          </basic-input>
        </div>
        <div>
          <p>Card Number</p>
          <basic-input-stripe
            id="cardField"
            icon="credit-card"
            :complete="form.cardNumber.complete"
            :error="(submitted && !$v.form.cardNumber.empty.required) || form.cardNumber.error"
            :empty="form.cardNumber.empty"
          >
            <div ref="cardNumber" slot="field"></div>
            <span
              class="error"
              v-if="form.cardNumber.error"
              slot="error"
            >{{ form.cardNumber.errorDisplay }}</span>
            <span
              class="error"
              v-if="submitted && !$v.form.cardNumber.empty.required"
              slot="error"
            >Card Number is required</span>
          </basic-input-stripe>
        </div>
        <div class="payment-action--card">
          <div>
            <p>Expires</p>
            <basic-input-stripe
              id="expireField"
              class="card-expire"
              icon="calendar"
              :complete="form.cardExpiry.complete"
              :error="(submitted && !$v.form.cardExpiry.empty.required) || form.cardExpiry.error"
              :empty="form.cardExpiry.empty"
            >
              <div ref="cardExpiry" slot="field"></div>
              <span
                class="error"
                v-if="form.cardExpiry.error"
                slot="error"
              >{{ form.cardExpiry.errorDisplay }}</span>
              <span
                class="error"
                v-if="submitted && !$v.form.cardExpiry.empty.required"
                slot="error"
              >Card Expires is required</span>
            </basic-input-stripe>
          </div>
          <div>
            <p>CCV</p>
            <basic-input-stripe
              id="ccvField"
              class="card-ccv"
              :complete="form.cardCvc.complete"
              :error="(submitted && !$v.form.cardCvc.empty.required) || form.cardCvc.error"
              :empty="form.cardCvc.empty"
            >
              <div ref="cardCvc" slot="field"></div>
              <span
                class="error"
                v-if="form.cardCvc.error"
                slot="error"
              >{{ form.cardCvc.errorDisplay }}</span>
              <span
                class="error"
                v-if="submitted && !$v.form.cardCvc.empty.required"
                slot="error"
              >Card CCV is required</span>
            </basic-input-stripe>
          </div>
        </div>
      </div>
    </form>
    <basic-button
      :text="`Pay ${currencyAmount}`"
      class="payment-button"
      color="#F76707"
      @click.prevent="submitForm"
      :disabled="loading || error"
      v-if="!error" v-show="!loading"
    >
      <icon-arrow-right size="16" style="icon--orange"></icon-arrow-right>
    </basic-button>
  </div>
</template>

<script lang="ts">
// COPIED FROM OLD PROJECT. I'm sorry :(
import { Component, Vue, Prop } from 'vue-property-decorator';

import { validationMixin } from 'vuelidate';
import { Validations } from 'vuelidate-property-decorators';
import { required } from 'vuelidate/lib/validators'

import BasicButton from '@/components/buttons/basic-button.vue';
import BasicInput from '@/components/inputs/basic-input.vue';
import BasicInputStripe from '@/components/inputs/basic-input-stripe.vue';
import IconArrowRight from '@/components/icons/icon-arrow-right.vue'

import { currency } from '@/utils/text'

import { getStripeClient } from '@/utils/payment'

const stripeRequiredValidator = (value: string) => !value;

@Component({
  components: {
    BasicButton, BasicInput, BasicInputStripe, IconArrowRight
  },
  filters: {
    currency,
  },
  mixins: [validationMixin, ],
})
export default class CreditCardForm extends Vue {

  @Prop()
  amount!: number
  
  @Validations()
  validations =  {
    form: {
      name: {
        required
      },
      cardNumber: {
        empty: {
          required: stripeRequiredValidator
        }
      },
      cardExpiry: {
        empty: {
          required: stripeRequiredValidator
        }
      },
      cardCvc: {
        empty: {
          required: stripeRequiredValidator
        }
      }
    }
  }
  
  // TODO: Type me
  form: any = {
    name: undefined,
    cardNumber: {
      element: undefined,
      complete: undefined,
      empty: true,
      value: undefined,
      error: false,
      errorDisplay: undefined
    },
    cardExpiry: {
      element: undefined,
      complete: undefined,
      empty: true,
      value: undefined,
      error: false,
      errorDisplay: undefined
    },
    cardCvc: {
      element: undefined,
      complete: undefined,
      empty: true,
      value: undefined,
      error: false,
      errorDisplay: undefined
    }
  }
  submitted = false
  loading = false
  error = false
  errorDisplay = ''
  stripeCli: any = undefined
  creditCard = false

  get currencyAmount(): string {
    return currency(this.amount)
  }

  stripeFieldsInvalid(): boolean {
    return (
      this.form.cardNumber.error ||
      this.form.cardExpiry.error ||
      this.form.cardCvc.error
    );
  }

  stripeFieldChangeHandler({elementType, error,  value,  empty,  complete,  brand }: {
    elementType: string,
    error: any,
    value: string,
    empty: boolean,
    complete: boolean,
    brand: any
  }): void {
    if (error) {
      this.form[elementType].error = true;
      this.form[elementType].errorDisplay = error.message;
    } else {
      this.form[elementType].error = false;
      this.form[elementType].errorDisplay = undefined;
    }
    this.form[elementType].empty = empty;
    this.form[elementType].complete = complete;
    this.form[elementType].value = value;
  }

  async submitForm(): Promise<void> {
    this.submitted = true;
    // @ts-ignore
    if (this.$v.$invalid || this.stripeFieldsInvalid()) {
      return;
    }
    this.$emit('loading')
    const token = await this.stripeCreateCardToken();
    if (token !== null) {
      this.$emit('success', {
        source: token.id,
        name: this.form.name.trim(),
        card_id: token.card.id
      });
    }
  }

  async stripeCreateCardToken(): Promise<any> {
    const { token, error } = await this.stripeCli.createToken(
      this.form.cardNumber.element,
      { name: this.form.name.trim() }
    );
    if (error) {
      // Inform the user that there was an error
      this.loading = false;
      this.error = true;
      this.errorDisplay = error.message;
      this.$emit('error', error);
      return null;
    } else {
      return token
    }
  }

  created(): void {
    this.stripeCli = getStripeClient()
  }

  mounted(): void {
    const style = {
      base: {
      fontSize: '16px',
      fontWeight: 300,
      letterSpacing: '0.2px'
      }
    }

    const elements = this.stripeCli.elements();
    const cardNumber = elements.create('cardNumber', { style });
    cardNumber.mount(this.$refs.cardNumber);
    this.form.cardNumber.element = cardNumber;
    cardNumber.addEventListener('change', this.stripeFieldChangeHandler);

    const cardExpiry = elements.create('cardExpiry', { style });
    cardExpiry.mount(this.$refs.cardExpiry);
    this.form.cardExpiry.element = cardExpiry;
    cardExpiry.addEventListener('change', this.stripeFieldChangeHandler);

    const cardCvc = elements.create('cardCvc', { style });
    cardCvc.mount(this.$refs.cardCvc);
    this.form.cardCvc.element = cardCvc;
    cardCvc.addEventListener('change', this.stripeFieldChangeHandler);
  }
}
</script>
             

<style lang="scss" scoped>
.icon--orange {
  color: $orange;
}
.checkbox-form {
  margin-top: 2rem;
  display: flex;
  justify-content: center;
}
input#nameField{
  color:#808080;
  font-size: $fs-md;
}
.radio-form--text {
  display: flex;
  p.input-text {
    margin: 0 1rem 0 0;
  }
}
.payment-option {
  display: flex;
  justify-content: space-between;
  margin: 0 auto;
  width: 21rem;
  .basic-button {
    margin: 0;
  }
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
  }
  .payment-info--date {
    background-color: $grey-light;
    font-size: $fs-sm;
    margin: 0 auto;
    opacity: 0.5;
    padding: 0.5rem;
  }
}
.payment-action {
  background-color: $grey-medium;
  border-radius: 8px;
  margin: 1.875rem auto 1.25rem;
  padding: 1.875rem 1.25rem;
  width: 23.13rem;
  > div {
    margin: 0 auto 1.25rem;
    width: 15rem;
    &:last-child {
      margin-bottom: 0;
    }
  }
  p {
    font-size: $fs-lg;
    font-weight: $fw-semibold;
    text-align: left;
    line-height: 1.33;
    margin-bottom: 0.5rem;
    opacity: 0.8;
  }
  .payment-action--card {
    display: flex;
    justify-content: space-between;
    .card-expire,
    .card-ccv {
      width: 6.875rem;
    }
  }
}
.payment-button {
  margin: 1.875rem auto 1.25rem;
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
