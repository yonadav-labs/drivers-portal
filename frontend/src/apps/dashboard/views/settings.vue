<template>
  <div class="settings-view">
    <h3 class="title">Settings</h3>
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
          <div class="settings-box__action">
            <contained-button
              :disabled="!passwordValid"
              color="blue"
              @click="changePassword"
            >
              Change password
            </contained-button>
          </div>
        </div>
      </form>
    </div>
    <!-- <div class="settings-box">
      <h4 class="settings-box__title">Change email address</h4>
      <div class="form-password">
        <div class="form-input__container">
          <div class='form-input__field'>
            <span class='form-input__label'>Email address</span>
            <basic-input
              id='tlcLicenseField'
              class='form-input__email'
              v-model="emailValue"
              type='email'
              placeholder='your.email-here@email.com'
              icon="envelope"
              :required="true"
              @valid="onValidChange"
              >
              </basic-input>
          </div>
          <error-message class="error" v-if="emailExists" slot="error">This email is already registered as user</error-message>
          <div class="settings-box__action">
            <basic-button
              :disabled="!passwordValid"
              text='Create password'
              :color='colorBlue'
              >
              <icon-arrow-right size='16'></icon-arrow-right>
            </basic-button>   
          </div>
        </div>
      </div>
    </div> -->
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import { Getter, Action, namespace } from 'vuex-class';

import BasicInput from '@/components/inputs/basic-input.vue'
import ContainedButton from '@/components/buttons/contained-button.vue'
import ErrorMessage from '@/components/error-message.vue'


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

  @users.Action
  updateUserPassword!: (password: string) => Promise<void>

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

  async changePassword(): Promise<void> {
    await this.updateUserPassword(this.password)
    this.password = ''
    this.confirmPassword = ''
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

  .settings-box {
    display: flex;
    flex-direction: column;
    max-width: 18rem;
    
    .settings-box__title {
      font-size: $fs-lg;
      line-height: 20px;
      margin-bottom: 1rem;
    }

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
    }

    .settings-box__action {
      display: flex;
      justify-content: center;
      margin-top: 1rem;
    }
  }
</style>