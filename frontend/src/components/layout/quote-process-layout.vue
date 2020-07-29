<template>
  <div>
    <div
      class="main-content"
    >
      <!-- Container -->
      <div class="container">
        <div class="content">
          <breadcrumbs
          v-if="!hideBreadcrumbs"
          ></breadcrumbs>
          <div
            class="header"
            :class="{'simple-header': simpleHeader}"
          >
            <h1>Stable</h1>
            <p v-if="showSubText">Lets get you a TLC Insurance Quote!</p>
          </div>
          <slot></slot>
        </div>

        <div
          class="footer"
          :class="{'footer--simple': !showBack && !hideLogin}"
        >
          <basic-button
            class="back-button"
            text="Back"
            @click="back()"
            v-if="showBack"
          >
            <icon-arrow-left size="16" class="icon--grey-darker" slot="before"></icon-arrow-left>
          </basic-button>
          <basic-button
            class="back-button"
            text="Log In"
            @click="login()"
            v-if="!hideLogin"
          >
            <icon-user size="16" class="icon--grey-darker"></icon-user>
          </basic-button>
      
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import BasicButton from '@/components/buttons/basic-button.vue'
import Breadcrumbs from '@/apps/quote/components/layout/breadcrumbs.vue'
import IconArrowLeft from '@/components/icons/icon-arrow-left.vue'
import IconUser from '@/components/icons/icon-user.vue'

import { OrderedQuoteRouteName, QuoteProcessRouter } from '@/router/quote'
import { RouteName } from '@/router';

@Component({
  components: {
    BasicButton, Breadcrumbs, IconArrowLeft, IconUser
  }
})
export default class QuoteProcessLayout extends Vue {
  @Prop({ default: false })
  simpleHeader!: boolean

  @Prop({ default: false })
  showSubText!: boolean

  @Prop({ default: false })
  hideBack!: boolean

  @Prop({ default: false })
  hideLogin!: boolean

  @Prop({ default: false })
  hideBreadcrumbs!: boolean

  @Prop()
  onBack?: () => void

  get showBack(): boolean {
    return !this.hideBack && QuoteProcessRouter.hasPrevious(this.$route.name!);
  }

  back(): void {
    if (!!this.onBack) {
      this.onBack()
    } else {
      this.$router.push(QuoteProcessRouter.previousRoute(this.$route.name!))
    }
  }

  login(): void {
    this.$router.push({ name: RouteName.LOGIN })
  }
}
</script>


<style lang="scss" scoped>
  .icon--grey-darker {
    color: $grey-darker;
  }

  .main-content {
    background-color: $grey-light;

    &.main-content--columns {
      align-items: flex-start;
      display: flex;
      justify-content: center;
      @media screen and (max-width: 62rem){
        flex-direction: column;
        justify-content: flex-start;
        min-height: 100vh;
        position: relative;
        .container{
          min-height: initial;
          .footer{
            bottom: 0;
            position: absolute;
          }
        }

      }
      .right-column {
        background-color: $white;
        border-radius: 8px;
        margin-left: 1rem;
        margin-top: 3.75rem;
        position: relative;
        width: 28.13rem;
        @media screen and (max-width: 62rem){
          margin: 0 auto 5rem;
          max-width: 35.63rem;
          width: calc(100vw - 2rem);
        }
        .divider {
          margin-top: 2.5rem;
          padding-bottom: 1.75rem;
        }
      }
      .container {
        margin: 0 1rem 0 0;
        @media screen and (max-width: 62rem){
          margin: 0 auto;
        }
        .form-container {
          margin-top: 1rem;
        }
      }
    }
    .container {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      margin: 0 auto;
      max-width: 75rem;
      min-height: 100vh;
      padding-top: 3.75rem;
      .content {
        background-color: $white;
        border-radius: 8px;
        min-height: 22rem;
        margin: 0 auto 1.875rem;
        padding: 0.625rem;
        position: relative;
        width: 35.63rem;
        @media screen and (max-width: 62rem){
          max-width: 35.63rem;
          width: calc(100vw - 2rem);
        }

        .header {
          background-color: $blue;
          background-image: url("~@/assets/Header.png");
          background-repeat: no-repeat;
          background-size: cover;
          border-radius: 4px;
          padding: 3.125rem 0;
          &.simple-header {
            background-image: url("~@/assets/Bg.png");
            padding: 0.72rem 0;
            h1 {
              font-size: $fs-xxl;
              padding-bottom: 0;
            }
          }
          h1 {
            font-size: $fs-xxxl;
            font-weight: $fw-bold;
            line-height: 1.2;
            padding-bottom: 0.625rem;
          }
          p {
            font-size: $fs-lg;
            font-weight: $fw-semibold;
            opacity: 0.8;
          }
          h1,
          p {
            color: $white;
            margin: 0;
            text-align: center;
          }
        }

        .form-container {
          text-align: center;
          .inputForm {
            align-items: center;
            background-color: $grey-opacity;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            margin: 1.25rem auto;
            padding: 0.75rem 1.2rem;
            .inputForm-label {
              font-size: $fs-lg;
              font-weight: $fw-semibold;
              opacity: 0.8;
            }
            .tlcLicenseField {
              width: 10rem;
              .error {
                font-size: $fs-xs;
                margin-top: 0.5rem;
              }
            }
          }
          .form-input {
            margin: 1.75rem auto 2.5rem;
          }
          p {
            &.form-info {
              color: $grey-darker;
              font-size: $fs-md;
              margin-bottom: 1rem;
              &:not(:first-child) {
                margin-top: 1rem;
              }
              &.form-info--capitalize {
                text-transform: capitalize;
              }
            }
            &.form-question {
              color: $blue-dark;
              margin-top: 1.75rem;
              span {
                text-transform: capitalize;
              }
            }
          }
        }
      }
      .form-explain {
        line-height: 1.5;
        font-size: $fs-lg;
        margin-left: auto;
        margin-right: auto;
        span {
          font-weight: $fw-semibold;
        }
      }
      .footer {
        align-items: center;
        background-color: $grey-medium;
        border-radius: 8px 8px 0 0;
        display: flex;
        flex-flow: row;
        justify-content: space-between;
        height: 3.75rem;
        margin: 0 auto;
        padding: 0.75rem;
        position: relative;
        width: 35.63rem;
        &.footer--simple {
          justify-content: flex-end;
        }
        .back-button {
          margin: 0;
        }
        .footer-comments {
          align-items: center;
          background-color: #f8f9fa;
          border-radius: 1.125rem;
          display: flex;
          height: 2.25rem;
          justify-content: center;
          width: 2.25rem;
        }
      }
    }
    .divider {
      border-top: 2px dashed $grey-medium;
      margin: 1rem 0;
      width: 100%;
    }
  }
  .form-container {
    margin: 1.875rem auto 0.625rem;
  }
  .simple-header + div .form-container {
    margin-top: 1rem;
  }
</style>