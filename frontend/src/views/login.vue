<template>
  <quote-process-layout :simple-header="true" :hide-breadcrumbs="true" :on-back="onBack" :hide-login="true">
      <div class='form'>
        <p class='form__explain'>
          Welcome back!
        </p>
        <form id='passwordForm' @submit.prevent.stop="doLogin">
          <div class="form-input">
            <div class="form-input__container">
                <div class='form-input__field'>
                  <span class='form-input__label'>Email address</span>
                  <basic-input
                    id='tlcLicenseField'
                    class='form-input__input'
                    v-model="user"
                    type='email'
                    placeholder='your.email-here@email.com'
                    icon="envelope"
                    :required="true"
                    @valid="onValidChange"
                    >
                    </basic-input>
                </div>
                <div class='form-input__field'>
                  <span class='form-input__label'>Your password</span>
                  <basic-input
                    id='password'
                    class='form-input__input'
                    type="password"
                    icon="lock"
                    v-model="password"
                    >
                  </basic-input>
                  <error-message class="error" v-if="errors">Incorrect email or password</error-message>
                  <a @click.prevent.stop="goToForgotPassword" class="forgot-password">Forgot your password?</a>
              </div>
            </div>
          </div>
          <basic-button
            text='Log In'
            :color='colorBlue'
            :disabled="!emailValid || !password"
            >
            <icon-arrow-right size='16'></icon-arrow-right>
          </basic-button>   
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
import ErrorMessage from '@/components/error-message.vue'

import { Colors } from '@/utils/colors'
import { RouteName } from '@/router';
import { Route } from 'vue-router';


const users = namespace('Users')

// First Step 

@Component({
  components: {
    QuoteProcessLayout, BasicButton, BasicInput, IconArrowRight,
    ErrorMessage
  }
})
export default class LoginView extends Vue {

  @users.Getter
  isAuthenticated!: boolean

  @users.Action
  login!: (payload: {user: string, password: string}) => void;

  errors = false;
  emailValid = false;
  user = ''
  password = ''

  get colorBlue(): string {
    return Colors.Blue
  }

  onValidChange(value: boolean): void {
    this.emailValid = value;
  }

  async doLogin(): Promise<void> {
    this.errors = false;
    await this.login({ user: this.user, password: this.password })
    if (!this.isAuthenticated) {
      this.errors = true;
    } else {
      this.$router.push({ name: RouteName.DASHBOARD })
    }
  }

  onBack():void {
    this.$router.push('/')
  }

  goToForgotPassword(): void {
    this.$router.push({ name: RouteName.FORGOT })
  }

  beforeRouteEnter (to: Route, from: Route, next: any): void {
    next(
      (vm: LoginView) => {
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
    align-self: center;
    color: $blue;
    cursor: pointer;
    font-size: $fs-md;
    font-weight: $fw-semibold;
    margin-top: 1.125rem;
  }
}
</style>
