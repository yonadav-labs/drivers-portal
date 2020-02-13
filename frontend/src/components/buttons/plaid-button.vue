<template>
  <div class="plaid-link-wrapper">
    <slot name="button" v-bind:onClick="onClick">
      <button class="plaid-link-button" @click="onClick">
        <slot/>
      </button>
    </slot>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import { getPlaidClient } from '@/utils/payment'

@Component
export default class PlaidButton extends Vue {
  plaidCli: any;

  onClick(event: Event): void {
    event.preventDefault()
    event.stopPropagation()

    if (!!this.plaidCli) {
      this.plaidCli.open()
    }
  }

  onSuccess(public_token: string, metadata: any): void {
    // The onSuccess function is called when the user has successfully
    // authenticated and selected an account to use.
    //
    // When called, you will send the public_token and the selected
    // account ID, metadata.account_id, to your backend app server.
    this.$emit('success', { public_token, metadata });
  }

  onExit(err: any, metadata: any): void {
    // User exited the Link flow.
    if (err != null) {
      // The user encountered a Plaid API error prior to exiting.
      this.$emit('exit', { err, metadata, result: 'plaid_error' });
    }
    this.$emit('exit', { err, metadata, result: 'exit' });
    // metadata contains information about the institution
    // that the user selected and the most recent API request IDs.
    // Storing this information can be helpful for support.
  }

  onEvent(eventName: any, metadata: any): void {
    // On Event
  }

  beforeDestroy(): void {
    if (!!this.plaidCli) {
      this.plaidCli.exit();
    }
  }

  created(): void {
    this.plaidCli = getPlaidClient(this.onSuccess, this.onExit, this.onEvent)
  }

}
</script>