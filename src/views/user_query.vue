<template>
    <div>
      <tabs :tabs="tabs_data" @tabClick="tabClick"></tabs>
      <div class="table-container">
        <div class="table-title-tr">
          <div class="table-title">时间</div>
          <div class="table-title">用户名</div>
        </div>
        <div class="table-tr" v-for="item in query1">
          <div class="table-td">{{item.date}}</div>
          <div class="table-td">{{item.userName}}</div>
        </div>
      </div>
      <div class="line"></div>
      <div class="table-container" v-if="query2Status">
        <div class="table-title-tr">
          <div class="table-title">时间</div>
          <div class="table-title">用户名</div>
        </div>
        <div class="table-tr" v-for="item in query2">
          <div class="table-td">{{item.date}}</div>
          <div class="table-td">{{item.userName}}</div>
        </div>
      </div>
      <div class="page-box">
        <page :total="total_page"></page>
      </div>
    </div>
</template>

<script>
  import query from '../common/json/query';
  import tabs from '../components/common/tabs';
  import page from '../components/common/page';
  import api from "../api/api";
  import axios from 'axios';

  export default {
    name: "user_query",
    data() {
      return {
        query: query,
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
        page_size:20,
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
          select_name: this.tabs_data.name
        }
        console.log(params)
        axios.get(api.get_all_scrapy, { params: params }).then(res => {
          if (res.data.status == 200){
            this.news = res.data.data
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
        console.log(v)
        if(v == this.current_page){
          this.$message({
            message: '这已经是第' + v + '页数据了',
            type: 'warning'
          });
          return false;
        }
        this.current_page = v;
        this.getData(v);
      },
      tabClick(index){
        let _arr = this.tabs_data;
        for(let i =0;i<_arr.length;i++){
          _arr[i].click = false;
        }
        _arr[index].click = true;
        this.tabs_data = [].concat(_arr);
      },
    },
    created() {
      if(this.query.length <= 10) {
        this.query2Status = false
        this.query1 = this.query
      }else if(this.query.length > 10) {
        for(let i=0;i<10;i++) {
          this.query1.push(this.query[i])
        }
        for(let j=10;j<this.query.length;j++) {
          this.query2.push(this.query[j])
        }
      }
    }
  }
</script>

<style lang="less" rel="stylesheet/less" scoped>
  @import "../common/css/_variate.less";
  .table-container {
    width: 40%;
    float: left;
    height: 7rem;
    .table-title-tr {
      .table-title {
        width: 50%;
        float: left;
        color: #545454;
        margin: 0.3rem 0;
        font-weight: bold;
        text-align: center;
      }
    }
    .table-tr {
      .table-td {
        width: 50%;
        float: left;
        margin: 0.2rem 0;
        text-align: center;
      }
    }
  }
  .page-box {

  }
  .line {
    width: 1px;
    float: left;
    height: 5.7rem;
    margin-top: 1rem;
    background-color: @borderColor;
  }
</style>
