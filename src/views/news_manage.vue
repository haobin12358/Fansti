<template>
  <div>
    <tabs :tabs="tabs_data" @tabClick="tabClick"></tabs>
    <div class="news-manage" v-for="item in news">
      <div class="news-container">
        <img class="news-image" v-bind:src="item.imageUrl" />
        <div class="news-text">
          <div class="news-title">{{item.title}}</div>
          <div class="news-from-date">{{item.newsFrom}}&nbsp;&nbsp;&nbsp;&nbsp;{{item.date}}</div>
          <div class="news-body">摘要：{{item.body}}</div>
        </div>
        <div class="news-edit">编辑</div>
      </div>
    </div>




    <!--<el-button @click="goPage">新闻编辑</el-button>-->
  </div>
</template>

<script>
  import news from '../common/json/news';
  import tabs from '../components/common/tabs';

  export default {
    name: "news_manage",
    data() {
      return {
        news: news,
        tabs_data:[
          {
            name:'上传',
            click:false,
            url:''
          },
          {
            name:'管理',
            click:true,
            url:''
          }
        ],
      }
    },
    components:{ tabs },
    methods: {
      goPage() {
        this.$router.push({ path: '/upload_news' })
      },
      tabClick(index){
        let _arr = this.tabs_data;
        for(let i =0;i<_arr.length;i++){
          _arr[i].click = false;
        }
        _arr[index].click = true;
        this.tabs_data = [].concat(_arr);
        console.log(index)
      }
    },
    created() {
      console.log(this.news)
    }
  }
</script>

<style lang="less" rel="stylesheet/less" scoped>
  @import "../common/css/_variate.less";
  .news-manage {
    .news-container {
      display: flex;
      margin: 0.2rem 0.5rem 0.2rem 0;
      border: solid 1px #707070;
      .news-image {
        margin: 0.2rem;
        min-width: 3.5rem;
        height: 1.4rem;
        display: flex;
        -webkit-align-items: center;
        -webkit-justify-content: center;
      }
      .news-text {
        margin: 0.2rem 0;
        .news-title {
          color: #545454;
          font-size: 20px;
          font-weight: bold;
        }
        .news-from-date {
          color: #545454;
          margin: 0.15rem 0;
          font-size: 14px;
        }
        .news-body {
          width: 95%;
          height: 0.6rem;
          font-size: 14px;
          line-height: 30px;
          display: -webkit-box;
          -webkit-box-orient: vertical;
          -webkit-line-clamp: 2;
          overflow: hidden;
          color: #7e7e7e;
        }
      }
      .news-edit {
        min-width: 1rem;
        font-size: 20px;
        color: @bgMainColor;
        background-color: @btnActiveColor;
        display: flex;
        -webkit-align-items: center;
        -webkit-justify-content: center;
      }
    }
  }
</style>
