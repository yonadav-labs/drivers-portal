<template>
  <div class="settings-view">
    <h3 class="title">Settings</h3>
    <div class="settings-container">
      <div class="settings-box">
        <h4 class="settings-box__title">Change password</h4>
        <form class="form-password">
          <div class="form-input">
            <div class='form-input__field'>
              <span class='form-input__label'>Your password</span>
              <basic-input
                id='password'
                class='form-input__input'
                minlength="8"
                type="password"
                icon="lock"
                v-model="password"
                @input="passwordInput = true"
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
                @input="passwordInput = true"
                >
                </basic-input>
            </div>
            <p class="error"><error-message v-if="passwordLengthValid && this.confirmPassword.length >= this.password.length && !passwordsMatch">The passwords must match</error-message></p>
            <p class="success" v-if="passwordChanged && !passwordInput">Password has been updated successfully!</p>
            <div class="settings-box__action">
              <contained-button
                :disabled="!passwordValid"
                color="blue"
                @click.prevent.stop="changePassword"
              >
                Change password
              </contained-button>
            </div>
          </div>
        </form>
      </div>
      <div class="settings-box">
        <h4 class="settings-box__title">Change email address</h4>
        <form class="form-email">
          <div class="form-input">
            <div class='form-input__field'>
              <span class='form-input__label'>Email address</span>
              <basic-input
                id='email'
                class='form-input__input'
                v-model="email"
                type='email'
                placeholder='your.email-here@email.com'
                icon="envelope"
                :required="true"
                @input="emailInput = true"
                @valid="onValidChange"
                >
                </basic-input>
            </div>
            <error-message class="error" v-if="email === user.email" slot="error">This email is already associated to this account</error-message>
            <error-message class="error" v-if="emailAlreadyExists && !emailInput" slot="error">This email is already associated to another user</error-message>
            <p class="success" v-if="emailChanged && !emailInput">Email has been updated successfully!</p>
            <div class="settings-box__action">
              <contained-button
                :disabled="!emailValid || email === user.email"
                color='blue'
                @click.prevent.stop="changeEmail"
              >
                Change email
              </contained-button>   
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import { Getter, Action, namespace } from 'vuex-class';

import BasicInput from '@/components/inputs/basic-input.vue'
import ContainedButton from '@/components/buttons/contained-button.vue'
import ErrorMessage from '@/components/error-message.vue'

import { User } from '@/@types/users'

import { Route } from 'vue-router';
import { RouteName } from '@/router';

import { Colors } from '@/utils/colors'

const users = namespace('Users')

@Component({
  components: {
    BasicInput, ContainedButton, ErrorMessage
  }
})
export default class DashboardSettingsView extends Vue {
  confirmPassword = ''
  password = ''
  passwordInput = false
  passwordChanged = false
  email = ''
  emailValid = false
  emailInput = false
  emailChanged = false

  @users.Getter
  user?: User

  @users.Getter
  emailAlreadyExists?: boolean

  @users.Action
  updateUserPassword!: (password: string) => Promise<void>

  @users.Action
  updateUserEmail!: (email: string) => Promise<void>

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

  onValidChange(valid: boolean): void {
    this.emailValid = valid
  }

  async changePassword(): Promise<void> {
    this.passwordInput = false
    this.passwordChanged = false
    await this.updateUserPassword(this.password)
    this.password = ''
    this.confirmPassword = ''
    this.passwordChanged = true
    setTimeout(() => {
      this.passwordChanged = false
    }, 2000);
  }

  async changeEmail(): Promise<void> {
    this.emailInput = false
    this.emailChanged = false
    await this.updateUserEmail(this.email)
    if (!this.emailAlreadyExists) {
      this.email = ''
      this.emailChanged = true
      setTimeout(() => {
        this.emailChanged = false
      }, 2000);
    }
  }
}
</script>

<style lang="scss" scoped>
  .title {
    font-size: 1.25rem;
    font-weight: $fw-semibold;
    line-height: 24px;
    margin-bottom: 1rem;
  }

  .settings-container {
    display: flex;
    justify-content: space-between;

    .settings-box {
      display: flex;
      flex-direction: column;
      width: 49%;

      &:first-of-type {
        border-right: 1px solid rgba($grey, 0.4);
      }

      .settings-box__title {
        font-size: $fs-lg;
        line-height: 20px;
        margin-bottom: 1rem;
      }

      form {
        max-width: 18rem;

        .form-input {
          border-radius: 8px;
          margin-bottom: 1.25rem;
          text-align: left;

          .form-input__container {
            padding: 1.25rem 2.5rem;
          }

          .form-input__field {
            align-items: flex-start;
            display: flex;
            flex-direction: column;
            justify-content:flex-start;

            &:not(:first-child) {
              margin-top: 1.25rem;
            }
          }

          .form-input__label {
            font-size: $fs-md;
            font-weight: $fw-semibold;
            margin-bottom: 0.5rem;
            opacity: 0.8;
          }

          .form-input__input {
            width: 17.5rem;
          }

          .success {
            color: $blue;
            font-weight: $fw-semibold;
          }
        }

        .settings-box__action {
          display: flex;
          justify-content: center;
          margin-top: 1rem;
        }
      }
    }
  }
</style>