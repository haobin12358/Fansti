<template>
    <div class="table">
      <tabs :tabs="tabs_data" @tabClick="tabClick"></tabs>
      <div class="table-container">
        <div class="table-title-tr">
          <div class="table-title">时&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;间</div>
          <div class="table-title">用 户 名</div>
          <div class="table-title-one">查询内容</div>
        </div>
        <div class="table-tr" v-for="item in query">
          <div class="table-td">{{item.create_time}}</div>
          <div class="table-td">{{item.login_name}}</div>
          <div class="table-td-one">{{item.select_name}}</div>
        </div>
      </div>
      <div class="page-box">
        <page :total="total_page" @pageChange="pageChange"></page>
      </div>
    </div>
</template>

<script>
  import tabs from '../components/common/tabs';
  import page from '../components/common/page';
  import api from "../api/api";
  import axios from 'axios';

  export default {
    name: "user_query",
    data() {
      return {
        query: [],
        query1: [],
        query2: [],
        query2Status: true,
        tabs_data:[
          { name: 'DGR', click: true, url: '' },
          { name: '鉴定报告', click: false, url: '' },
          { name: 'TACT', click: false, url: '' },
          { name: 'HS code', click: false, url: '' },
          { name: 'CAS', click: false, url: '' },
          { name: '航班时刻', click: false, url: '' }
        ],
        select_name: 'DGR',
        page_size:10,
        total_num:5,
        current_page:1,
        total_page:0
      }
    },
    components:{ tabs, page },
    methods: {
      getData(v){
        let params = {
          page_size: this.page_size,
          page_num: Number(v || this.current_page),
          select_name: this.select_name
        }
        axios.get(api.get_all_scrapy, { params: params }).then(res => {
          if (res.data.status == 200){
            this.query = res.data.data.all_select;
            // console.log(this.query)
            this.total_num = res.data.data.count;
            this.total_page = Math.ceil(this.total_num / this.page_size);
          }else{
            this.$message.error(res.data.message);
          }
        },error => {
          this.$message.error(error.data.message);
        })
      },
      /*分页点击*/
      pageChange(v){
        if(v == this.current_page){
          this.$message({ message: '这已经是第' + v + '页数据了', type: 'warning' });
          return false;
        }
        this.current_page = v;
        this.getData(v);
      },
      tabClick(index){
        let _arr = this.tabs_data;
        for(let i = 0; i < _arr.length; i ++){
          _arr[i].click = false;
        }
        _arr[index].click = true;
        this.tabs_data = [].concat(_arr);
        this.select_name = this.tabs_data[index].name
        this.getData(1);
      },
    },
    created() {
      this.getData(1);
    }
  }
</script>

<style lang="less" rel="stylesheet/less" scoped>
  @import "../common/css/_variate.less";
  .table {
    .table-container {
      width: 95%;
      .table-title-tr {
        display: flex;
        .table-title {
          width: 15%;
          color: #545454;
          padding: 0.2rem 0;
          font-weight: bold;
          text-align: center;
        }
        .table-title-one {
          width: 60%;
          color: #545454;
          padding: 0.2rem 0.6rem;
          font-weight: bold;
        }
      }
      .table-tr {
        display: flex;
        align-items: center;
        line-height: 0.2rem;
        border-bottom: 1px solid @borderColor;
        .table-td {
          width: 15%;
          height: auto;
          padding: 0.2rem 0;
          text-align: center;
        }
        .table-td-one {
          width: 60%;
          height: auto;
          padding: 0.2rem 0.6rem;
        }
      }
    }
    .page-box {
      margin-top: 0.3rem;
    }
  }
</style>
