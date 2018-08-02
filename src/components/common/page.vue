
<template>
  <div class="m-page" :class="position">
    <el-pagination
      layout="prev, pager, next"
      :total="total"
    @current-change="pageChange">
    </el-pagination>
  </div>
</template>

<script>
  export default {
    name: 'Pagination',

    data () {
      return {

      }
    },
    props:{
      total:{
        type:Number,
        default:1
      },
     position:{
        type:String,
       default:'center'
     }
    },
    methods:{
      pageChange(v) {
        this.$emit('pageChange',v)
      }
    }
  }
</script>

<style lang="less" rel="stylesheet/less" scoped>
  @import "../../common/css/_variate.less";
  .m-page{
    &:after{
      display: block;
      content: '';
      clear: both;
    }
  }

</style>
