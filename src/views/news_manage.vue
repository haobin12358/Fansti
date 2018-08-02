<template>
  <div>
    <tabs :tabs="tabs_data" @tabClick="tabClick"></tabs>
    <div v-if="!newsManage">
      <div class="news-manage" v-for="item in news">
        <div class="news-container">
          <img class="news-image" :src="item.imageUrl" />
          <div class="news-text">
            <div class="news-title">{{item.title}}</div>
            <div class="news-from-date">{{item.newsFrom}}&nbsp;&nbsp;&nbsp;&nbsp;{{item.date}}</div>
            <div class="news-body">摘要：{{item.body}}</div>
          </div>
          <div class="news-edit">编辑</div>
        </div>
      </div>
    </div>
    <div v-if="newsManage">
      <div class="news-upload">
        <div class="news-upload-title">
          <div class="left-text">新闻标题：</div>
          <el-input class="right-input" v-model="input" placeholder="此处为新闻标题"></el-input>
        </div>
        <div class="news-upload-from">
          <div class="left-text">新闻来源：</div>
          <el-input class="right-input" v-model="input" placeholder="此处为新闻来源"></el-input>
        </div>
        <div class="news-upload-image">
          <div class="left-text">标题图片：</div>
          <el-upload class="avatar-uploader" action="https://jsonplaceholder.typicode.com/posts/"
            :show-file-list="false" :on-success="handleAvatarSuccess" :before-upload="beforeAvatarUpload">
            <img v-if="imageUrl" :src="imageUrl" class="avatar">
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
          </el-upload>
        </div>
        <div class="news-upload-body">
          <div class="left-text">新闻正文：</div>
          <div class="ueditor">
            <UE :defaultMsg=defaultMsg ref="ue"></UE>
          </div>
        </div>
        <el-button class="upload-btn" @click="getUEContent">上 传</el-button>
      </div>
    </div>
  </div>
</template>

<script>
  import news from '../common/json/news';
  import tabs from '../components/common/tabs';
  import UE from '../components/common/ueditor';

  export default {
    name: "news_manage",
    data() {
      return {
        news: news,
        newsManage: true,
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
        input: '',
        imageUrl: '',
        defaultMsg: '',
      }
    },
    components:{ tabs, UE },
    methods: {
      tabClick(index){
        let _arr = this.tabs_data;
        for(let i =0;i<_arr.length;i++){
          _arr[i].click = false;
        }
        _arr[index].click = true;
        this.tabs_data = [].concat(_arr);
        if(index == 0) {
          this.newsManage = false
        }else if(index == 1) {
          this.newsManage = true
        }
      },
      handleAvatarSuccess(res, file) {
        this.imageUrl = URL.createObjectURL(file.raw);
      },
      beforeAvatarUpload(file) {
        const isJPG = file.type === 'image/jpeg' || 'image/png';
        const isLt2M = file.size / 1024 / 1024 < 2;

        if (!isJPG) {
          this.$message.error('上传头像图片只能是 JPG 或 PNG 格式!');
        }
        if (!isLt2M) {
          this.$message.error('上传头像图片大小不能超过 2MB!');
        }
        return isJPG && isLt2M;
      },
      getUEContent() {
        let content = this.$refs.ue.getUEContent();
        this.$notify({
          title: '获取成功，可在控制台查看！',
          message: content,
          type: 'success'
        });
        console.log(content)
      }
    },
    created() {
      // console.log(this.news)
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
        max-height: 1.4rem;
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
        font-size: 18px;
        color: @bgMainColor;
        background-color: @btnActiveColor;
        display: flex;
        -webkit-align-items: center;
        -webkit-justify-content: center;
      }
    }
  }
  .news-upload {
    .news-upload-title {

    }
    .news-upload-from {

    }
    .news-upload-image {

    }
    .news-upload-body {
      .ueditor {
        max-height: 3rem;
        margin-left: 1.3rem;
      }
    }
    .upload-btn {
      width: 1rem;
      height: 0.4rem;
      margin: 4.8rem 0 0 2.6rem;
      color: @bgMainColor;
      background-color: @btnActiveColor;
    }
    .left-text {
      float: left;
      min-width: 1.3rem;
      line-height: 0.32rem;
    }
    .right-input {
      width: 6rem;
      margin-bottom: 0.4rem;
    }
  }
</style>
