<template>
  <modal @close="$emit('close')">
    <div class="modal-create-password">
      <div class="modal-header">
        <span>Create a password</span>
      </div>
      <div class="modal-content">
        <div class='form'>
            <p class='form__explain'>
              Your insurance quote is being validated! Create a password to track progress and communicate with Stable directly!
            </p>
            <form id='passwordForm' @submit.prevent.stop="createPassword">
              <div class="form-input">
                <div class="form-input__container">
                    <div class='form-input__field'>
                      <span class='form-input__label'>Email address</span>
                      <basic-input
                        id='email'
                        class='form-input__input'
                        :value="email"
                        type="text"
                        :disabled="true"
                        icon="envelope"
                        >
                        </basic-input>
                    </div>
                </div>
                <div class="form__password">
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
              </div>
              <basic-button
                :disabled="!passwordValid"
                text='Create password'
                :color='colorBlue'
                >
                <icon-arrow-right size='16'></icon-arrow-right>
              </basic-button>   
          </form>
        </div>
      </div>
    </div>
  </modal>
</template>

<script lang="ts">

import { Component, Vue, Prop, } from 'vue-property-decorator';

import Modal from '@/components/modals/modal.vue'

import BasicButton from '@/components/buttons/basic-button.vue'
import BasicInput from '@/components/inputs/basic-input.vue'

import ErrorMessage from '@/components/error-message.vue'

import IconArrowRight from '@/components/icons/icon-arrow-right.vue'

import { Colors } from '@/utils/colors'

@Component({
  components: {
    Modal, BasicButton, BasicInput, ErrorMessage, IconArrowRight
  },
})
export default class ModalCreatePassword extends Vue {
  @Prop({ default: '' })
  email!: string;

  confirmPassword = ''
  password = ''

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

  createPassword():void {
    if (this.passwordValid) {
      this.$emit('submit', this.password)
    }
  }
}
</script>

<style lang="scss" scoped>
.modal-create-password {
  background-color: $white;
  border-radius: 8px;
  box-shadow: 0 10px 20px 0 rgba(206,212,218,0.4);
  max-width: 36.875rem;
  min-height: 33.25rem;
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
}
</style>