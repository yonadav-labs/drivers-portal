<template>
  <modal @close="$emit('close')">
    <div class="modal-premium">
      <div class="modal-header">
        <span>How is my premium calculated?</span>
        <div @click="$emit('close')" class="close">
          <icon-cross size="16"></icon-cross>
        </div>
      </div>
      <div class="modal-content">
        <div class="dropdown" @click="opened == 'driver' ? opened = '' : opened = 'driver'">
          <div class="dropdown--header">
            <span>driver(s) information</span>
            <span>{{ tlcName }}</span>
            <icon-chevron-up v-if="opened == 'driver'" size="12"></icon-chevron-up>
            <icon-chevron-down v-else size="12"></icon-chevron-down>
          </div>
          <div class="dropdown--content" v-if="opened == 'driver'">
            <div class="dropdown--content-row">
              <span class="label">Name</span>
              <span class="value">{{ tlcName }}</span>
            </div>
            <div class="dropdown--content-row">
              <span class="label">TLC License Number</span>
              <span class="value">{{ tlcNumber }}</span>
            </div>
            <div class="dropdown--content-row">
              <span class="label">Defensive Driving Course</span>
              <span class="value">{{ defensive }}</span>
            </div>
            <div class="dropdown--content-row">
              <span class="label">Points in Last 36 Months</span>
              <span class="value">{{ points }}</span>
            </div>
            <div class="dropdown--content-row">
              <span class="label">At Fault Accidents in Last 36 Months</span>
              <span class="value">{{ accidents }}</span>
            </div>
          </div>
        </div>
        <div class="dropdown" @click="opened == 'vehicle' ? opened = '' : opened = 'vehicle'">
          <div class="dropdown--header">
            <span>vehicle details</span>
            <span>VIN # - {{ vehicleVin }}</span>
            <icon-chevron-up v-if="opened == 'vehicle'" size="12"></icon-chevron-up>
            <icon-chevron-down v-else size="12"></icon-chevron-down>
          </div>
          <div class="dropdown--content" v-if="opened == 'vehicle'">
            <div class="dropdown--content-row">
              <span class="label">VIN #</span>
              <span class="value">{{ vehicleVin }}</span>
            </div>
            <div class="dropdown--content-row">
              <span class="label">Owner</span>
              <span class="value">{{ vehicleOwner }}</span>
            </div>
            <div class="dropdown--content-row">
              <span class="label">Plate</span>
              <span class="value">{{ vehiclePlate }}</span>
            </div>
            <div class="dropdown--content-row">
              <span class="label">Year</span>
              <span class="value">{{ vehicleYear }}</span>
            </div>
            <div class="dropdown--content-row">
              <span class="label">Insurance (Policy)</span>
              <span class="value">{{ insuranceName }} ({{ insurancePolicy }}) </span>
            </div>
            <div class="dropdown--content-row">
              <span class="label">Base Name (Base Number)</span>
              <span class="value">{{ baseName }} ({{ baseNumber }})</span>
            </div>
          </div>
        </div>
        <div class="dropdown" @click="opened == 'price' ? opened = '' : opened = 'price'">
          <div class="dropdown--header">
            <span>price breakdown</span>
            <icon-chevron-up v-if="opened == 'price'" size="12"></icon-chevron-up>
            <icon-chevron-down v-else size="12"></icon-chevron-down>
          </div>
          <div class="dropdown--content" v-if="opened == 'price'">
            <div class="dropdown--content-row">
              <span class="label">Deductible</span>
              <span class="value"  v-if="hasDeductible">{{ deductibleOption | currency }}</span>
              <span class="value" v-else>$--</span>
            </div>
            <div class="dropdown--content-row">
              <span class="label">Downpayment</span>
              <span class="value">{{ hasDeposit ? depositOption:'--' }}%</span>
            </div>
            <div class="dropdown--content-row">
              <span class="label">Hereford Monthly Fee</span>
              <span class="value"  v-if="hasDeposit">{{ herefordFee | currency }}</span>
              <span class="value" v-else>$--</span>
            </div>
          </div>
        </div>
        <div class="dropdown" @click="opened == 'liability' ? opened = '' : opened = 'liability'" v-if="!!variations">
          <div class="dropdown--header">
            <span>liability coverage</span>
            <span>{{ variations.liability_total | currency }}</span>
            <icon-chevron-up v-if="opened == 'liability'" size="12"></icon-chevron-up>
            <icon-chevron-down v-else size="12"></icon-chevron-down>
          </div>
          <div class="dropdown--content" v-if="opened == 'liability'">
            <div class="dropdown--content-row">
              <span class="label">Bodily Injury</span>
              <span class="value">{{ variations.body_injury | currency }}</span>
            </div>
            <div class="dropdown--content-row">
              <span class="label">Property Damage</span>
              <span class="value">{{ variations.property_damage | currency }}</span>
            </div>
            <div class="dropdown--content-row">
              <span class="label">Uninsored Motorist</span>
              <span class="value">{{ variations.uninsured_motorist | currency }}</span>
            </div>
            <div class="dropdown--content-row">
              <span class="label">Personal Injury protection</span>
              <span class="value">{{ variations.personal_injury_protection | currency }}</span>
            </div>
            <div class="dropdown--content-row">
              <span class="label">Aggregate no-fault</span>
              <span class="value">{{ variations.aditional_personal_injury_protection | currency }}</span>
            </div>
            <div class="dropdown--content-row">
              <span class="label">Total Liability</span>
              <span class="value">{{ variations.liability_total | currency }}</span>
            </div>
          </div>
        </div>
        <div class="dropdown" @click="opened == 'physical' ? opened = '' : opened = 'physical'" v-if="hasDeductible && physical">
          <div class="dropdown--header">
            <span>physical coverage</span>
            <span>{{ physical.physical_total | currency }}</span>
            <icon-chevron-up v-if="opened == 'physical'" size="12"></icon-chevron-up>
            <icon-chevron-down v-else size="12"></icon-chevron-down>
          </div>
          <div class="dropdown--content" v-if="opened == 'physical'">
            <div class="dropdown--content-row">
              <span class="label">Comprehensive</span>
              <span class="value">{{ physical.physical_comprehensive | currency }}</span>
            </div>
            <div class="dropdown--content-row">
              <span class="label">Collision</span>
              <span class="value">{{ physical.physical_collision | currency }}</span>
            </div>
            <div class="dropdown--content-row">
              <span class="label">Physical Total</span>
              <span class="value">{{ physical.physical_total | currency }}</span>
            </div>
          </div>
        </div>
        <div class="dropdown" @click="opened == 'total' ? opened = '' : opened = 'total'">
          <div class="dropdown--header">
            <span>total amount</span>
            <span v-if="total">{{ total | currency }}</span>
            <span class="value" v-else>$--</span>
            <icon-chevron-up v-if="opened == 'total'" size="12"></icon-chevron-up>
            <icon-chevron-down v-else size="12"></icon-chevron-down>
          </div>
          <div class="dropdown--content" v-if="opened == 'total'">
            <div class="dropdown--content-row">
              <span class="label">Deposit</span>
              <span class="value" v-if="hasDeposit">{{ deposit | currency }}</span>
              <span class="value" v-else>$--</span>
            </div>
            <div class="dropdown--content-row">
              <span class="label">Monthly Payment</span>
              <span class="value" v-if="hasDeposit">{{ (monthlyPayment + herefordFee) | currency }} ({{ monthlyPayment | currency }} + {{ herefordFee | currency }})</span>
              <span class="value" v-else>$--</span>
            </div>
          </div>
        </div>
        <div class="insurance-resume">
          <div class="insurance-estimated">
            <p>Monthly payment</p>
            <p class="estimated-price">{{ monthlyPaymentText }}<sup v-if="herefordFee">+{{ herefordFee | beautyCurrency }}</sup></p>
            <span class="estimated-date">9 payments starting on
              <br>
              {{ firstPaymentDue }}
            </span>
          </div>
          <div class="insurance-estimated">
            <p>Deposit</p>
            <p class="estimated-price">{{ depositText }}</p>
            <span class="estimated-date">{{ hasDeposit ? `${depositOption}%`:'--%' }} of total price</span>
          </div>
        </div>
      </div>
    </div>
  </modal>
</template>

<script lang="ts">

import { Component, Vue, Prop, } from 'vue-property-decorator';

import Modal from '@/components/modals/modal.vue'
import IconCross from '@/components/icons/icon-cross.vue'
import IconChevronUp from '@/components/icons/icon-chevron-up.vue';
import IconChevronDown from '@/components/icons/icon-chevron-down.vue';

import { QuoteProcessCalcVariations, QuoteProcessVariationPhysical } from '@/@types/quote';

import { currency, beautyCurrency } from '@/utils/text'
import { getHerefordFee } from '@/utils/quote'

@Component({
  components: {
    Modal, IconCross, IconChevronUp, IconChevronDown
  },
  filters: {
    currency,
    beautyCurrency
  }
})
export default class ModalPremium extends Vue {
  @Prop({ default: '' })
  tlcName!: string;

  @Prop({ default: '' })
  tlcNumber!: string;

  @Prop({ default: false })
  hasDefensive!: boolean;

  @Prop({ default: '' })
  points!: string;

  @Prop({ default: '' })
  accidents!: string;

  @Prop({ default: '' })
  vehicleVin!: string;

  @Prop({ default: '' })
  vehicleOwner!: string;

  @Prop({ default: '' })
  vehiclePlate!: string;

  @Prop({ default: '' })
  vehicleYear!: string;

  @Prop({ default: '' })
  baseName!: string;

  @Prop({ default: '' })
  baseNumber!: string;

  @Prop({ default: '' })
  insuranceName!: string;

  @Prop({ default: '' })
  insurancePolicy!: string;

  @Prop({ default: 0 })
  deductibleOption!: number;

  @Prop({ default: 0 })
  depositOption!: number;

  @Prop()
  variations?: QuoteProcessCalcVariations

  @Prop()
  physical?: QuoteProcessVariationPhysical

  @Prop({ default: 0 })
  total!: number;

  @Prop({ default: 0 })
  monthlyPayment!: number;

  @Prop({ default: 0 })
  deposit!: number;

  @Prop({ default: '--' })
  firstPaymentDue!: string;
  
  opened = ''

  get defensive(): string {
    return !!this.hasDefensive ? 'Yes': 'No'
  }

  get herefordFee(): number {
    return !!this.depositOption ? getHerefordFee(this.depositOption):0;
  }

  get hasDeposit(): boolean {
    return this.depositOption > 0;
  }

  get hasDeductible(): boolean {
    return this.deductibleOption > 0;
  }

  get depositText(): string {
    return this.hasDeposit ? beautyCurrency(this.deposit):'$--'
  }
  get monthlyPaymentText(): string {
    return this.hasDeposit ? beautyCurrency(this.monthlyPayment):'$--'
  }

 dateFunc(): string {
    return 'Oct 7, 2018';
  }
}
</script>

<style lang="scss" scoped>
.modal-premium {
  background-color: $white;
  border: 1px solid $blue;
  border-radius: 4px;
  box-shadow: 0 10px 20px 0 rgba(206,212,218,0.4);
  max-width: 43.5rem;
  min-height: 33.25rem;
  width: calc(100vw - 8rem);
  z-index: 1;

  .modal-header {
    background-color: $blue;
    background-image: url("~@/assets/headerModal.png");
    background-repeat: no-repeat;
    background-size: cover;
    border-radius: 4px 4px 0 0;
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
    max-height: calc(100vh - 4rem);
    overflow-y: auto;
    padding: 1.5rem 4.5rem;

    .dropdown {
      margin-bottom: 0.75rem;

      &--header {
        align-items: center;
        border: 1px solid rgba(206,212,218,0.4);
        cursor: pointer;
        display: flex;
        justify-content: flex-start;
        padding: 0.75rem 1.5rem 0.625rem;

        span {
          font-size: $fs-xs;
          font-weight: $fw-bold;
          letter-spacing: 1px;
          text-transform: uppercase;
          width: 40%;

          &:nth-of-type(2) {
            color: $grey-darker;
            font-style: italic;
            font-weight: $fw-regular;
          }
        }

        .svg-icon-center {
          margin-left: auto;
        }
      }

      &--content {
        align-items: center;
        background-color: rgba($blue, 0.05);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-top: 0.75rem;
        padding: 0 1.5rem;

        &-row {
          align-items: center;
          border-bottom: 1px solid $grey;
          display: flex;
          justify-content: flex-start;
          width: 100%;

          &:last-of-type {
            border-bottom: none;
          }

          span {
            align-items: center;
            display: flex;
            justify-content: flex-start;
            padding: 0.75rem 0;
            
            &.label {
              flex: 0 0 60%;
              font-weight: $fw-bold;
            }

            &.value {
              font-weight: $fw-regular;
            }
          }
        }
      }
    }

    .insurance-resume {
      background-color: rgba(241, 243, 245, 0.92);
      display: flex;
      justify-content: space-between;
      margin: 0 auto;
      max-width: 23rem;
      padding: 1.25rem;
      
      .insurance-estimated {
        background-color: $white;
        border-radius: 2px;
        text-align: center;
        display: flex;
        flex-direction: column;
        padding: 1rem 0.875rem 0.875rem;
        width: 10rem;

        span {
          font-size: $fs-lg;
        }

        p {
          text-align: center;

          &.estimated-price {
            color: $blue;
            font-size: $fs-xl;
            font-weight: $fw-semibold;
            margin-top: 1rem;
            margin-bottom: 1rem;

            sup {
              font-size: $fs-sm;
              font-weight: $fw-semibold;
            }
          }
        }
        .estimated-date {
          background-color: $grey-light;
          font-size: $fs-sm;
          margin: 0 auto;
          opacity: 0.5;
          padding: 0.5rem;
        }
      }
    }
  }
  .close {
    cursor: pointer;
    float: right;
    transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    transform-origin: center center;
    &:hover {
      -webkit-transform: scale3d(1.2, 1.2, 1.2);
      transform: scale3d(1.2);
    }
  }
}
</style>