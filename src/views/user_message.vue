<template>
    <div>
      <div class="m-table">
        <table width="100%">
          <thead>
          <tr>
            <td width="250">序号</td>
            <td width="330">联系方式</td>
            <td>内容</td>
          </tr>
          </thead>
          <tbody>
          <template v-for="(item,index) in table_data">
            <tr>
              <td>{{index+1}}</td>
              <td>{{item.phone}}</td>
              <td>{{item.message}}</td>
            </tr>
          </template>
          </tbody>
        </table>
      </div>
      <div class="m-page-box">
        <page :total="page_data.total_page"></page>
      </div>
    </div>
</template>

<script>
  import page from '../components/common/page';
  import api from "../api/api";
  import axios from 'axios';
    export default {
        data(){
          return{
            page_data:{
              page_size:10,
              total_num:5,
              current_page:1,
              total_page:0
            },
            table_data:[]
          }
        },
      components:{
          page
      },
      mounted(){
          this.getData();
      },
      methods:{
          getData(v){
            axios.get(api.get_user_message,{params:{
                page_size:this.page_data.page_size,
                page_num:Number(v || this.page_data.current_page)
              }}).then(res => {
              if (res.data.status == 200){
                this.table_data = res.data.data.message_list;
                this.page_data.total_num = res.data.data.count;
                this.page_data.total_page = Math.ceil(this.page_data.total_num / this.page_data.page_size);
              }else{
                this.$message.error(res.data.message);
              }
            },error => {
              this.$message.error(error.data.message);
            })
          },
        /*分页点击*/
        pageChange(v){
          if(v == this.page_data.current_page){
            this.$message({
              message: '这已经是第' + v + '页数据了',
              type: 'warning'
            });
            return false;
          }
          this.page_data.current_page = v;
          this.getData(v);
        }
      }
    }
</script>

<style lang="less" rel="stylesheet/less" scoped>
  @import "../common/css/index";
.m-table{
  width: 14.4rem;
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
        padding: 0.23rem 0;
      }
    }
  }
}
  .m-page-box{
    margin-top: 0.6rem;
  }

</style>
