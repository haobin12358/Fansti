<template>
    <div>
      <div class="m-table">
        <table width="100%">
          <thead>
          <tr>
            <td width="250">序号</td>
            <td width="330">用户名</td>
            <td>内容</td>
          </tr>
          </thead>
          <tbody>
          <tr>
            <td>序号</td>
            <td>用户名</td>
            <td>内容</td>
          </tr>
          <tr>
            <td>序号</td>
            <td>用户名</td>
            <td>内容</td>
          </tr>
          </tbody>
        </table>
      </div>
      <page></page>
    </div>
</template>

<script>
  import page from '../components/common/page';
    export default {
        data(){
          return{
            page_data:{
              page_size:10,
              total_num:0,
              current:1
            }
          }
        },
      components:{
          page
      }
    }
</script>

<style lang="less" rel="stylesheet/less" scoped>
  @import "../common/css/index";
.m-table{
  width: 13.4rem;
  table{
    thead{
      td{
        font-size: 0.18rem;
        font-weight: 600;
        padding-bottom: 0.1rem;
      }
    }
    tbody{
      td{
        border-bottom: 1px solid @borderColor;
        padding: 0.1rem 0;
      }
    }
  }
}
</style>
