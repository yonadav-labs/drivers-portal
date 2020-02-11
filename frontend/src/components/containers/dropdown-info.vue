<template>
  <div class="dropdownInfo">
    <div class="dropdownInfo-header" @click="toggle()">
        <h2>{{title}}</h2>
        <icon-caret-down size="16" class="icon" v-if="!openDropdown"></icon-caret-down>
        <icon-caret-up size="16" class="icon" v-else></icon-caret-up>
    </div>
    <div class="dropdownInfo-body" v-show="openDropdown">
      <div class="dropdown-info__content">
        <p class="price">{{price}}</p>
        <p class="description"><slot></slot></p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import IconCaretDown from '@/components/icons/icon-caret-down.vue'
import IconCaretUp from '@/components/icons/icon-caret-up.vue'

@Component({
  components: {
    IconCaretDown, IconCaretUp
  }
})
export default class DropdownInfo extends Vue {
  @Prop({ default: ''})
  title?: string;

  @Prop({ default: '' })
  price?: string;

  openDropdown = false;

  toggle(): void {
    this.openDropdown = !this.openDropdown;
  }

}
</script>

<style lang="scss" scoped>
  .dropdownInfo{
    background-color: $white;
    border-bottom: 1px solid $grey-medium;
    padding: 1.125rem 0.75rem;
    .dropdownInfo-header{
      align-items: center;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
        h2{
          color: $blue;
          font-size: $fs-md;
          line-height: 1.25;
          font-weight: $fw-semibold;
        }
        .icon{
            cursor:pointer;
            color: $blue;
            z-index: 1;
        }
    }
    .dropdown-info__content{
      padding:0.5rem 0 0;
      .price,.description{
        line-height: 1.5;
        text-align: left;
      }
      .price{
        font-weight: $fw-semibold;
        margin-bottom: 0.5rem;
      }
    }
  }
</style>