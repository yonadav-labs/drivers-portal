<template>
<p v-if="invalidLink">This link is not valid. Redirecting to quote page...</p>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import { Getter, Action, namespace } from 'vuex-class';

import { QuoteProcessRouter } from '@/router/quote'

import { DashboardRouteName } from '@/router/dashboard'

const users = namespace('Users')

@Component
export default class MagicLinkView extends Vue {
  @Prop({ default: '' })
  id!: string;

  @users.Getter
  isAuthenticated!: boolean

  @users.Action
  useMagickLink!: (id: string) => Promise<void>

  invalidLink = false;

  onInvalidLink(): void {
    this.invalidLink = true;
    setTimeout(() => {
      this.$router.replace(QuoteProcessRouter.getRouteByOrder(0))
    }, 3000)
  }

  onValidLink(): void {
    // TODO: Change me
    this.$router.replace({ name: DashboardRouteName.DOCS })
  }

  async created(): Promise<void> {
    if (!this.id) {
      this.onInvalidLink();
    }

    await this.useMagickLink(this.id);
    if (!this.isAuthenticated) {
      this.onInvalidLink();
    } else {
      this.onValidLink();
    }
  }
}
</script>