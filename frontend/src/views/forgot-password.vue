<template>
  <quote-process-layout :simple-header="true" :hide-breadcrumbs="true" :on-back="onBack" :hide-login="true">
      <div class='form'>
        <p class='form__explain'>
          Forgot password
        </p>
        <form id='forgotPasswordForm' @submit.prevent.stop="doSend">
          <div class="form-input">
            <div class="form-input__container">
              <div class='form-input__field'>
                <span class='form-input__label'>Email address</span>
                <basic-input
                  id='emailField'
                  class='form-input__input'
                  v-model="email"
                  type='email'
                  placeholder='your.email-here@email.com'
                  icon="envelope"
                  :required="true"
                  @valid="onValidChange"
                  >
                  </basic-input>
              </div>
            </div>
          </div>
          <basic-button v-if="!sent"
            text='Send'
            :color='colorBlue'
            :disabled="!emailValid"
            >
            <icon-arrow-right size='16'></icon-arrow-right>
          </basic-button>
          <p v-else class="success">We have sent you an email with a link to reset your password.</p>
      </form>
    </div>
  </quote-process-layout>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';

import { Getter, Action, namespace } from 'vuex-class';

import BasicButton from '@/components/buttons/basic-button.vue'
import BasicInput from '@/components/inputs/basic-input.vue'
import IconArrowRight from '@/components/icons/icon-arrow-right.vue'
import QuoteProcessLayout from '@/components/layout/quote-process-layout.vue'

import { Colors } from '@/utils/colors'
import { RouteName } from '@/router';
import { Route } from 'vue-router';


const users = namespace('Users')

@Component({
  components: {
    QuoteProcessLayout, BasicButton, BasicInput, IconArrowRight
  }
})
export default class ForgotPasswordView extends Vue {

  @users.Getter
  isAuthenticated!: boolean

  @users.Action
  forgotPassword!: (email: string) => void;

  sent = false;
  emailValid = false;
  email = ''

  get colorBlue(): string {
    return Colors.Blue
  }

  onValidChange(value: boolean): void {
    this.emailValid = value;
  }

  async doSend(): Promise<void> {
    await this.forgotPassword(this.email)
    this.sent = true;
  }

  onBack():void {
    this.$router.push({ name: RouteName.LOGIN })
  }

  beforeRouteEnter (to: Route, from: Route, next: any): void {
    next(
      (vm: ForgotPasswordView) => {
        if (vm.isAuthenticated) {
          vm.$router.push({ name: RouteName.DASHBOARD })
        }
      }
    )
  }
}
</script>

<style lang='scss' scoped>
.form {
  padding: 1.875rem 2.5rem;
  text-align: center;

  .form__explain {
    line-height: 1.5;
    font-size: $fs-lg;
    margin-bottom: 1.75rem;

    span {
      font-weight: $fw-semibold;
    }
  }


  .form-input {
    background-color: $grey-opacity;
    border-radius: 8px;
    margin-bottom: 1.25rem;
    margin-left: 3.75rem;
    margin-right: 3.75rem;
    padding: 1.5rem 2.5rem;
    text-align: left;


    .form-input__field {
      align-items: flex-start;
      display: flex;
      flex-direction: column;
      justify-content:flex-start;

      &:not(:first-child) {
        margin-top: 1.75rem;
      }
    }

    .form-input__label {
      font-size: $fs-lg;
      font-weight: $fw-semibold;
      margin-bottom: 0.5rem;
      opacity: 0.8;
    }

    .form-input__input {
      width: 17.5rem;
    }
  }

  .success {
    color: $blue;
    font-weight: $fw-semibold;
  }
}
</style>
