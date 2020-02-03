<template>
  <quote-process-layout>
    <div class='form'>
      <p class='form__explain'>To start, we need your TLC number.</p>
        <form id='tlcForm'>
        <div class='form-input'>
          <span class='form-input__label'>TLC license number</span>
          <basic-input
          id='tlcLicenseField'
          class='form-input__tlc'
          v-model="tlcValue"
          :minlength='7'
          :maxlength='7'
          type='text'
          placeholder='000000'>
          </basic-input>
        </div>
        <basic-button
          text='Next Step'
          :disabled="tlcValue.length != 7"
          :color='colorBlue'
        >
        <icon-arrow-right size='16' class='icon--blue'></icon-arrow-right>
        </basic-button>
      </form>
    </div>
  </quote-process-layout>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BasicButton from '@/components/buttons/basic-button.vue'
import BasicInput from '@/components/inputs/basic-input.vue'
import IconArrowRight from '@/components/icons/icon-arrow-right.vue'
import QuoteProcessLayout from '@/apps/quote/components/layout/quote-process-layout.vue'

import { Colors } from '@/utils/colors'

// First Step 

@Component({
  components: {
    QuoteProcessLayout, BasicButton, BasicInput, IconArrowRight
    
  }
})
export default class StepTLC extends Vue {
  get colorBlue(): string {
    return Colors.Blue
  }

  tlcValue = ''
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
    align-items: center;
    background-color: rgba(206, 212, 218, 0.2);
    border-radius: 8px;
    display: flex;
    justify-content: space-between;
    margin: 1.25rem auto;
    padding: 0.75rem 2rem;

    .form-input__label {
      font-size: $fs-lg;
      font-weight: $fw-semibold;
      opacity: 0.8;
    }
    .form-input__tlc {
      width: 8rem;

      .error {
        font-size: $fs-xs;
        margin-top: 0.5rem;
      }
    }
  }
}
</style>
