<template>
  <div>
    <p v-if="invalidLink">This link is not valid. Redirecting to quote page...</p>
    <quote-process-layout  v-else :simple-header="true" :hide-breadcrumbs="true" :hide-back="true" :hide-login="true">
      <div class='form'>
        <p class='form__explain'>
          Reset password
        </p>
        <form id='passwordForm' @submit.prevent.stop="doResetPassword">
          <div class="form-input">
            <div class="form-input__container">
              <div class='form-input__field'>
                <span class='form-input__label'>Your password</span>
                <basic-input
                  id='password'
                  class='form-input__input'
                  minlength="8"
                  type="password"
                  icon="lock"
                  v-model="password"
                  >
                </basic-input>
              </div>
              <div class='form-input__field'>
                <span class='form-input__label'>Confirm password</span>
                <basic-input
                  id='confirm-password'
                  class='form-input__input'
                  help-text="Minimum length is 8 characters"
                  minlength="8"
                  type="password"
                  icon="lock"
                  :validate="passwordsMatch"
                  v-model="confirmPassword"
                  >
                </basic-input>
              </div>
              <p class="error"><error-message v-if="passwordLengthValid && this.confirmPassword.length >= this.password.length && !passwordsMatch">The passwords must match</error-message></p>
            </div>
          </div>
          <basic-button
            v-if="!showMessage"
            :disabled="!passwordValid"
            text='Reset password'
            :color='colorBlue'
            >
            <icon-arrow-right size='16'></icon-arrow-right>
          </basic-button>
          <p v-else class="success">Password changed successfully. Please <a @click.prevent="goToLogin">log in</a> using the new password.</p>
        </form>
      </div>
    </quote-process-layout>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch, Prop } from 'vue-property-decorator';

import { Getter, Action, namespace } from 'vuex-class';

import BasicButton from '@/components/buttons/basic-button.vue'
import BasicInput from '@/components/inputs/basic-input.vue'
import IconArrowRight from '@/components/icons/icon-arrow-right.vue'
import QuoteProcessLayout from '@/components/layout/quote-process-layout.vue'
import ErrorMessage from '@/components/error-message.vue'

import { Colors } from '@/utils/colors'
import { RouteName } from '@/router';
import { Route } from 'vue-router';
import { QuoteProcessRouter } from '@/router/quote'


const users = namespace('Users')

// First Step 

@Component({
  components: {
    QuoteProcessLayout, BasicButton, BasicInput, IconArrowRight,
    ErrorMessage
  }
})
export default class ResetPasswordView extends Vue {
  @Prop({ default: '' })
  id!: string;

  @users.Getter
  isAuthenticated!: boolean

  @users.Action
  resetPasswordLinkExists!: (id: string) => boolean;
  
  @users.Action
  resetPassword!: (payload: {id: string, password: string}) => void;

  invalidLink = false
  confirmPassword = ''
  password = ''
  showMessage = false

  get colorBlue(): string {
    return Colors.Blue
  }

  get passwordLengthValid(): boolean {
    return this.password.length > 7 && this.confirmPassword.length > 7
  }

  get passwordsMatch(): boolean {
    return this.password === this.confirmPassword;
  }

  get passwordValid(): boolean {
    return this.passwordLengthValid && this.passwordsMatch;
  }

  async doResetPassword(): Promise<void> {
    if (this.passwordValid) {
      await this.resetPassword({ id: this.id, password: this.password })
      this.showMessage = true
    }
  }

  goToLogin(): void {
    this.$router.replace({ name: RouteName.LOGIN })
  }

  onInvalidLink(): void {
    this.invalidLink = true;
    setTimeout(() => {
      this.$router.replace(QuoteProcessRouter.getRouteByOrder(0))
    }, 3000)
  }

  async created(): Promise<void> {
    if (!this.id) {
      this.onInvalidLink();
    }

    const valid = await this.resetPasswordLinkExists(this.id);
    if (!valid) {
      this.onInvalidLink();
    }
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

  .form__password {
    background-color: rgba(206,212,218,0.4);
    border-bottom-left-radius: 8px; 
    border-bottom-right-radius: 8px; 
    line-height: 28px;
    text-align: left;

    .form-input__container {
      padding-bottom: 2rem;
    }
  }

  .forgot-password {
    color: $orange;
    cursor: pointer;
    font-size: $fs-sm;
  }

  .success {
    color: $blue;
    font-weight: $fw-semibold;
    line-height: 1.25;

    a {
      color: $orange;
      cursor: pointer;
    }
  }
}
</style>
