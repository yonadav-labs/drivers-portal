<template>
    <div class="banner" :class="{'banner--bg': active}">
        <div class="banner-header">
            <h2>{{title}}</h2>
            <a href="#" v-if="hasInfo">+ info</a>
        </div>
        <div class="banner-body">
            <p>{{text}}</p>
            <slot></slot>
        </div>
    </div>
</template>


<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

@Component
export default class Banner extends Vue {
  @Prop()
  title?: string;

  @Prop()
  text?: string;
  
  @Prop({ default: false })
  active!: boolean;

  @Prop({ default: false })
  hasInfo!: boolean

}
</script>

<style lang="scss" scoped>
.banner{
  padding: 1.25rem;
  &.banner--bg{
    background-image: url('~@/assets/Bg-cta.png');
    background-repeat: no-repeat;
    background-size: cover; 
    border-radius: 4px;
    min-height: 8.5rem;
  }
  .banner-header{
      display: flex;
      justify-content: space-between;
      h2{
          color:$blue-dark;
          font-size: $fs-lg;
          font-weight: $fw-bold;
          line-height: 1.22;
      }
      a{
          color: $blue;
          font-size: $fs-sm;
          font-weight: $fw-bold;
          line-height: 1.22;
          text-decoration: none;
      }
  }
  .banner-body{
      align-items: flex-start;
      display: flex;
      justify-content: space-between;
      margin-top: 0.5rem;
      p{
          line-height: 1.37;
          margin-right: 1.75rem;
          text-align: left;
      }
      .basic-select{
          flex-shrink: 0;
      }
  }
}
</style>
