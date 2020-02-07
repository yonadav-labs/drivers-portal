<template>
  <quote-process-layout :hide-back="true" :hide-breadcrumbs="true">
    <div class='form' v-if="!success">
        <p class='form__explain'>
          Looks like your policy is a little tricky! Give us your name and contact 
          information and our team will reach out right away to get you a quote! 
        </p>
        <form id='falloutForm' @submit.prevent.stop="send">
          <div class="form-input">
            <div class="form-input__container">
              <div class='form-input__input' ref="input-name">
                  <span class='form-input__label'>Name</span>
                  <basic-input
                    id='name'
                    class='form-input__field'
                    v-model="nameValue"
                    type='text'
                    placeholder='John Doe'
                    icon="user"
                    :required="true"
                    >
                    </basic-input>
                </div>
                <div class='form-input__input' ref="input-email">
                  <span class='form-input__label'>Email address</span>
                  <basic-input
                    id='email'
                    class='form-input__field'
                    v-model="emailValue"
                    type='email'
                    placeholder='your.email-here@email.com'
                    icon="envelope"
                    :required="true"
                    @valid="onValidChange"
                    >
                    </basic-input>
                </div>
               <div class='form-input__input' ref="input-phone">
                  <span class='form-input__label'>Phone number</span>
                  <basic-input
                    id='phone'
                    class='form-input__field'
                    v-model="phoneValue"
                    type='text'
                    placeholder='(Optional)'
                    icon="phone"
                    >
                    </basic-input>
                </div>
            </div>
          </div>
          <basic-button
            text='Send'
            :disabled="!formValid"
            :color='colorBlue'
            >
            <icon-arrow-right size='16' class='icon--blue'></icon-arrow-right>
          </basic-button>        
      </form>
    </div>
    <div class="success" v-else>
      <div class="success-content">
        <!-- <div class="success-content__icon">
          <icon-check-circle size="46"></icon-check-circle>
        </div> -->
        <p class="success-content__title">
          Thanks!
        </p>
        <p>
          Our team will contact you as soon as possible.
        </p>
      </div>
    </div>
  </quote-process-layout>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';

import { Action, namespace } from 'vuex-class';
import { Route } from 'vue-router';

import QuoteProcessLayout from '@/apps/quote/components/layout/quote-process-layout.vue'

import BasicButton from '@/components/buttons/basic-button.vue'
import BasicInput from '@/components/inputs/basic-input.vue'
import IconArrowRight from '@/components/icons/icon-arrow-right.vue'
import IconCheckCircle from '@/components/icons/icon-check-circle.vue'

import { Colors } from '@/utils/colors'
import { QuoteSoftFallout } from '@/@types/quote';

// Soft Fallout

const quote = namespace('Quote')

@Component({
  components: {
    BasicButton, BasicInput, QuoteProcessLayout, IconArrowRight, IconCheckCircle
  }
})
export default class StepQuoteSoftFallout extends Vue {

  nameValue = ''
  phoneValue = ''
  emailValue = ''
  emailValid = false
  success = false;

  @quote.Action
  createQuoteSoftFallout!: (payload: QuoteSoftFallout) => Promise<void>

  get colorBlue(): string {
    return Colors.Blue
  }

  get formValid(): boolean {
    return !!this.nameValue && this.emailValid
  }

  onValidChange(value: boolean): void {
    this.emailValid = value;
  }

  async send(): Promise<void> {
    await this.createQuoteSoftFallout({ name: this.nameValue, phone_number: this.phoneValue, email: this.emailValue });
    this.success = true;
  }
}
</script>

<style lang='scss' scoped>
.form {
  padding: 1.875rem 5.625rem 1.75rem;
  text-align: center;

  .form__explain {
    line-height: 1.5;
    font-size: $fs-lg;
    margin-left: auto;
    margin-right: auto;

    span {
      font-weight: $fw-semibold;
    }
  }


  .form-input {
    background-color: $grey-opacity;
    border-radius: 8px;
    margin: 1.25rem auto;
    text-align: left;

    .form-input__container {
      padding: 1.25rem 2.5rem;
    }

    .form-input__input {
      align-items: flex-start;
      display: flex;
      flex-direction: column;
      justify-content:flex-start;
      
      &:not(:last-child) {
        margin-bottom: 1.25rem;
      }
    }

    .form-input__label {
      font-size: $fs-lg;
      font-weight: $fw-semibold;
      margin-bottom: 0.5rem;
      opacity: 0.8;
    }

    .form-input__field {
      width: 17.5rem;

      .error {
        font-size: $fs-xs;
        margin-top: 0.5rem;
      }
    }
  }

  .form__result {
    background-color: rgba(206,212,218,0.4);
    border-bottom-left-radius: 8px; 
    border-bottom-right-radius: 8px; 
    line-height: 28px;
    padding: 1.25rem 1rem;
    text-align: center;

    span {
      font-weight: $fw-semibold;
    }
  }
}

.success {
  padding: 1.875rem 5.625rem 1.75rem;
  text-align: center;  

  .success-content {
    background-color: $grey-opacity;
    border-radius: 8px;
    margin: 1.25rem auto;
    padding: 1.5rem 6rem;

    .success-content__title {
      font-weight: $fw-semibold;
      font-size: $fs-lg;
      margin-bottom: 0.5rem;
    }
  }
}
</style>
