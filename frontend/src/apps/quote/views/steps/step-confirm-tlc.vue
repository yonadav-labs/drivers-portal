<template>
  <quote-process-layout>
      Step 2
  </quote-process-layout>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';

import { Getter, Action } from 'vuex-class';

import BasicButton from '@/components/buttons/basic-button.vue'
import BasicInput from '@/components/inputs/basic-input.vue'
import IconArrowRight from '@/components/icons/icon-arrow-right.vue'
import QuoteProcessLayout from '@/apps/quote/components/layout/quote-process-layout.vue'
import ErrorMessage from '@/components/error-message.vue'

import { Colors } from '@/utils/colors'
import { TLCStepLicenseName } from '../../../../@types/quote';
import { NavigationGuard } from 'vue-router';


// First Step 

@Component({
  components: {
    QuoteProcessLayout, BasicButton, BasicInput, IconArrowRight,
    ErrorMessage
  }
})
export default class StepTLC extends Vue {

    @Getter('Quote/tlcLicenseNameValid')
    tlcLicenseNameValid!: boolean

    created(): void {
        if (!this.tlcLicenseNameValid) {
            this.$router.push({ name: 'quoteTlc' })
        }
    }
}
</script>