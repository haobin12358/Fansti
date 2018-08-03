<template>
  <div>
    <tabs :tabs="tabs_data" @tabClick="tabClick"></tabs>
    <div class="page-box">
      <page :total="total_page"></page>
    </div>
    <div v-if="newsManage">
      <div class="news-manage" v-for="item in news">
        <div class="news-container">
          <img class="news-image" :src="item.news_picture" />
          <div class="news-text">
            <div class="news-title">{{item.news_title}}</div>
            <div class="news-status" v-if="item.newsStatus">该新闻已关闭</div>
            <div class="news-status" v-if="!item.newsStatus">该新闻已上传</div>
            <div class="news-from-date">{{item.news_from}}&nbsp;&nbsp;&nbsp;&nbsp;{{item.news_time}}</div>
            <div class="news-body">摘要：{{item.news_all}}</div>
          </div>
          <div class="news-edit" v-if="item.newsStatus" @click="editNews(item)">编 辑</div>
          <div class="news-close" v-if="!item.newsStatus" @click="closeNews(item)">关 闭</div>
        </div>
      </div>
    </div>
    <div v-if="!newsManage">
      <div class="news-upload">
        <div class="news-upload-title">
          <div class="left-text">新闻标题：</div>
          <el-input class="right-input" v-model="titleInput" placeholder="此处为新闻标题"></el-input>
        </div>
        <div class="news-upload-from">
          <div class="left-text">新闻来源：</div>
          <el-input class="right-input" v-model="fromInput" placeholder="此处为新闻来源"></el-input>
        </div>
        <div class="news-upload-image">
          <div class="left-text">标题图片：</div>
          <el-upload class="avatar-uploader" action="http://10.0.0.130:7444/fansti/news/upload_files" :show-file-list="false"
                     :on-success="uploadPicture"
                     :before-upload="beforeAvatarUpload">
            <img v-if="imageUrl" :src="imageUrl" class="avatar">
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
          </el-upload>
          <div class="image-upload-done" v-if="imageUrlStatus">
            <p>注意：</p>
            <p>1、请确认所上传图片的宽高比在2~3之间</p>
            <p>2、请确认所上传图片为 JPG 或 PNG格式</p>
            <p>3、请确认所上传图片文件大小不超过 2MB</p>
          </div>
        </div>
        <div class="news-upload-body">
          <div class="left-text">新闻正文：</div>
          <div class="ueditor">
            <UE :defaultMsg=defaultMsg ref="ue"></UE>
          </div>
        </div>
        <el-button class="upload-btn" @click="uploadNews">上 传</el-button>
      </div>
    </div>
  </div>
</template>

<script>
  import news from '../common/json/news'
  import tabs from '../components/common/tabs';
  import UE from '../components/common/ueditor';
  import page from '../components/common/page';
  import api from "../api/api";
  import axios from 'axios';

  export default {
    name: "news_manage",
    data() {
      return {
        news: [],
        newsManage: true,
        tabs_data:[
          { name:'上传', click:false, url:'' },
          { name:'管理', click:true, url:'' }
        ],
        titleInput: '',
        fromInput: '',
        imageUrl: '',
        defaultMsg: '',
        page_size:10,
        total_num:5,
        current_page:1,
        total_page: 0,
        newsContent: '',
        imageUrlStatus: true
      }
    },
    components:{ tabs, UE, page },
    methods: {
      newNews() {
        let news = {
          titleInput: this.titleInput,
          fromInput: this.fromInput,
          imageUrl: this.imageUrl,
        }
        console.log(news)
      },
      getData(v){
        axios.get(api.get_news_all,{params:{
            page_size:this.page_size,
            page_num:Number(v || this.current_page)
          }}).then(res => {
          if (res.data.status == 200){
            this.news = res.data.data
            this.total_num = res.data.data.count;
            this.total_page = Math.ceil(this.total_num / this.page_size);
            // console.log('news', this.news)
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
        if(index == 0) {
          this.newsManage = false
        }else if(index == 1) {
          this.newsManage = true
        }
      },
      uploadPicture(res, file) {
        let form = new FormData();
        form.append("file", file.raw);
        form.append("FileType", 'NewsPic');
        // form.append("contentId",  '123');
        form.append("index", 1);
        axios.post(api.upload_files, form).then(res => {
          if(res.data.status == 200){
            console.log(res)
            this.$message({ type: 'success', message: res.data.message });
          }else{
            this.$message({ type: 'error', message: res.data.message });
          }
        },error =>{
          this.$message({ type: 'error', message: '服务器请求失败，请稍后再试' });
        })
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
      uploadNews() {
        // this.newsContent = this.$refs.ue.getUEContent()
        this.newsContent = "<p>\n" +
          "    &nbsp; &nbsp; &nbsp; &nbsp;本报讯：今日十点，在萧山区发生一起精神病案\n" +
          "</p>\n" +
          "<p>\n" +
          "    <br/>\n" +
          "</p>\n" +
          "<p>\n" +
          "    <img src=\"http://img.jdzj.com/UserDocument/2017z/5789139/Picture/20171027153429285.jpg\" width=\"350\" height=\"140\"/>\n" +
          "</p>\n" +
          "<p>\n" +
          "    <strong style=\"color: rgb(255, 0, 0); background-color: rgb(255, 255, 255); font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 14px; margin: 0px; padding: 0px;\"><br/></strong>\n" +
          "</p>\n" +
          "<p>\n" +
          "    <strong style=\"color: rgb(255, 0, 0); background-color: rgb(255, 255, 255); font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 14px; margin: 0px; padding: 0px;\">写在最前面的话：鉴于近期很多的博友讨论，说我按照文章的一步一步来，弄好之后，怎么会提示后端配置项http错误，文件上传会提示上传错误。这里提别申明一点，ueditor在前端配置好后，需要与后端部分配合进行，然后将配置ueditor.config.js 里的serverUrl的前缀改陈你自己的后端访问的请求路径地址，文件上传的后端部分，只提供了demo，具体对接文件服务器的部分需要自己修改完成。</strong>\n" +
          "</p>\n" +
          "<p style=\"margin: 10px auto; padding: 0px; color: rgb(51, 51, 51); font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 14px; white-space: normal; background-color: rgb(255, 255, 255);\">\n" +
          "    首先，谈下这篇文章中的前后端所涉及到的技术框架内容。\n" +
          "</p>\n" +
          "<p style=\"margin: 10px auto; padding: 0px; color: rgb(51, 51, 51); font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 14px; white-space: normal; background-color: rgb(255, 255, 255);\">\n" +
          "    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp; 虽然是后端的管理项目，但整体项目，是采用前后端分离的方式完成，这样做的目的也是产品化的需求；\n" +
          "</p>\n" +
          "<p style=\"margin: 10px auto; padding: 0px; color: rgb(51, 51, 51); font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 14px; white-space: normal; background-color: rgb(255, 255, 255);\">\n" +
          "    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;<strong style=\"margin: 0px; padding: 0px;\">前端，vue+vuex+vue router+webpack+elementUI的方案完成框架的搭建，其中用到了superUI来作为后端登陆之后的主页面框架，中间集成vue的大型单页应用；</strong>\n" +
          "</p>\n" +
          "<p style=\"margin: 10px auto; padding: 0px; color: rgb(51, 51, 51); font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 14px; white-space: normal; background-color: rgb(255, 255, 255);\">\n" +
          "    <strong style=\"margin: 0px; padding: 0px;\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp; 后端，springboot+spring+springmvc+spring serurity+mybatis+maven+redis+dubbo</strong>\n" +
          "</p>"
        if(this.titleInput == '') {
          this.$message.error('请填写新闻标题');
        }else if(this.fromInput == '') {
          this.$message.error('请填写新闻来源');
        }else if(this.imageUrl == '') {
          this.$message.error('请上传标题图片');
        }else if(this.newsContent == '') {
          this.$message.error('请撰写新闻正文');
        }
        for(let i=0;i<this.news.length;i++) {
          // 去除html中的标签和&nbsp;
          this.news[i].news_all = this.newsContent.replace(/<[^<>]+?>/g, '').replace(/(\s|&nbsp;)+/g,'')
        }
        let params = {
          news_title: this.titleInput,
          news_from: this.fromInput,
          news_picture: this.imageUrl,
          news_all: this.newsContent
        }
  /*      axios.post(api.new_news, params).then(res => {
          if(res.data.status == 200){
            console.log(res)
            this.$message({ type: 'success', message: res.data.message });
            this.newsManage = true
          }else{
            this.$message({ type: 'error', message: res.data.message });
          }
        },error =>{
          this.$message({ type: 'error', message: '服务器请求失败，请稍后再试' });
        })*/


      },
      editNews(news) {
        this.newsManage = false
        this.titleInput = news.news_title
        this.fromInput = news.news_from
        this.imageUrl = news.news_picture
        this.newsContent = news.news_all
        console.log(news.id)
      },
      closeNews(news) {
        console.log(news.id)
      }
    },
    created() {
      this.news = news
      // this.getData(1)
    }
  }
</script>

<style lang="less" rel="stylesheet/less" scoped>
  @import "../common/css/_variate.less";
  .page-box {
    /*margin: -3% 0 0 60%;*/
  }
  .news-manage {
    .news-container {
      display: flex;
      margin: 0.2rem 0.5rem 0.2rem 0;
      border: solid 1px #707070;
      .news-image {
        margin: 0.2rem;
        /*min-width: 3.5rem;*/
        max-height: 1.4rem;
        width: 20%;
        display: flex;
        -webkit-align-items: center;
        -webkit-justify-content: center;
      }
      .news-text {
        width: 72%;
        margin: 0.2rem 0;
        .news-title {
          color: #545454;
          font-size: 20px;
          font-weight: bold;
        }
        .news-status {
          float: right;
          color: #7e7e7e;
          font-size: 14px;
          margin-right: 5%;
          margin-top: -0.23rem;
        }
        .news-from-date {
          color: #545454;
          margin: 0.15rem 0;
          font-size: 14px;
        }
        .news-body {
          /*min-width: 10rem;*/
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
      .news-close {
        min-width: 1rem;
        font-size: 18px;
        color: @bgMainColor;
        background-color: @mainColor;
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
    .image-upload-done {
      color: #7e7e7e;
      font-size: 12px;
      margin: -1.1rem 0 0.5rem 5rem;
    }
    .right-input {
      width: 6rem;
      margin-bottom: 0.4rem;
    }
  }
</style>
