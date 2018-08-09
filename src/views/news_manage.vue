<template>
  <div>
    <tabs :tabs="tabs_data" @tabClick="tabClick"></tabs>
    <div v-if="newsManage">
      <div class="page-box">
        <page :total="total_page"></page>
      </div>
      <div class="news-manage" v-for="item in news">
        <div class="news-container">
          <img class="news-image" :src="item.news_picture" :onerror="errorImg"/>
          <div class="news-text">
            <div class="news-title">{{item.news_title}}</div>
            <div class="news-from-date">{{item.news_from}}&nbsp;&nbsp;&nbsp;&nbsp;{{item.news_time}}</div>
            <div class="news-body">摘要：{{item.abstract}}</div>
          </div>
          <div class="news-edit" @click="editNews(item)">编 辑</div>
          <div class="news-close" @click="closeNews(item)">删 除</div>
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
                     <!--:on-remove="handleRemove"-->
            <img v-if="imageUrl" :src="imageUrl" class="avatar">
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
          </el-upload>
          <div class="image-upload-done" v-if="imageUrlStatus">
            <p>注意：</p>
            <p>1、图片文件大小不超过 2MB</p>
            <p>2、图片的格式须为 JPG 或 PNG</p>
            <p>3、图片宽高比的适宜范围为 2.1~2.7</p>
          </div>
        </div>
        <div class="news-upload-body">
          <div class="left-text">新闻正文：</div>
          <div class="ueditor">
            <UE :defaultMsg=defaultMsg ref="ue"></UE>
          </div>
        </div>
        <!--<div v-if="editNewsStatus">-->
          <el-tooltip content="放弃本次编辑" placement="top">
            <el-button class="give-up-btn" @click="giveUpEdit">放弃编辑</el-button>
          </el-tooltip>
          <el-button class="upload-two-btn" @click="uploadNews">上 传</el-button>
        <!--</div>-->
        <!--<div v-if="!editNewsStatus">
          <el-tooltip content="放弃本次编辑" placement="top">
            <el-button class="give-up-btn" @click="giveUpEdit">放弃编辑</el-button>
          </el-tooltip>
          <el-button class="upload-two-btn" @click="updateNews">上 传</el-button>
        </div>-->
      </div>
    </div>
  </div>
</template>

<script>
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
        imageUrlStatus: true,
        // editor: null
        errorImg: 'this.src="' + require('../assets/images/newsPic.jpg') + '"',
        abstract: '',
        editNewsStatus: false,
        newsId: ''
      }
    },
    components:{ tabs, UE, page },
    methods: {
      getData(v){
        axios.get(api.get_news_all,{params:{
            page_size: this.page_size,
            page_num: Number(v || this.current_page)
          }}).then(res => {
          if (res.data.status == 200){
            this.news = res.data.data
            for(let i=0;i<this.news.length;i++) {
              // 去除html中的标签和&nbsp;
              this.abstract = this.news[i].news_all.replace(/<[^<>]+?>/g, '').replace(/(\s|&nbsp;)+/g,'')
              this.news[i].abstract = this.abstract
            }
            // console.log(this.news)
            this.total_num = res.data.data.length;
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
      // 顶部的tab标签
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
      // 上传标题图片
      uploadPicture(res, file) {
        let form = new FormData();
        form.append("file", file.raw);
        form.append("FileType", 'NewsPic');
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
      // 上传图片前的限制方法
      beforeAvatarUpload(file) {
        // 上传前限制图片的宽高比
        var _this = this;
        return new Promise(function(resolve, reject) {
          var reader = new FileReader();
          reader.onload = function(event) {
            var image = new Image();
            image.onload = function () {
              if(this.width/this.height>2.7 || this.width/this.height<2.1) {
                // _this.$message.warning('请上传宽高比为2.1~2.7的图片');
                _this.$notify({ title: '提示', message: '建议上传宽高比为2.1~2.7的图片', type: 'warning' });
                // reject();
              }
              resolve();
            };
            image.src = event.target.result;
          }
          reader.readAsDataURL(file);
        });
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
      // 放弃编辑
      giveUpEdit() {
        if(this.titleInput == '' && this.fromInput == '' && this.imageUrl == '' && this.defaultMsg == '') {
          this.tabClick(1)
        }else if(this.titleInput != '' || this.fromInput != '' || this.imageUrl != '' || this.defaultMsg != ''){
          this.$confirm('此操作将不保存本页变化的内容', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            this.newsId = ''
            this.titleInput = ''
            this.fromInput = ''
            this.imageUrl = ''
            this.defaultMsg = ''
            this.tabClick(1)
          });
        }
      },
      // 上传新闻
      uploadNews() {
        if(this.newsId != '') {
          this.updateNews()
        }else {
          this.newsContent = this.$refs.ue.getUEContent()
          if(this.titleInput == '') {
            this.$message.error('请填写新闻标题');
          }else if(this.fromInput == '') {
            this.$message.error('请填写新闻来源');
          }else if(this.imageUrl == '') {
            this.$message.error('请上传标题图片');
          }else if(this.newsContent == '') {
            this.$message.error('请撰写新闻正文');
          }else {
            let params = {
              news_title: this.titleInput,
              news_from: this.fromInput,
              news_picture: this.imageUrl,
              news_all: this.newsContent
            }
            axios.post(api.new_news, params).then(res => {
              if(res.data.status == 200){
                this.$message({ type: 'success', message: res.data.message });
                this.getData(1)
                this.tabClick(1)
                this.titleInput = ''
                this.fromInput = ''
                this.imageUrl = ''
              }else{
                this.$message({ type: 'error', message: res.data.message });
              }
            },error =>{
              this.$message({ type: 'error', message: '服务器请求失败，请稍后再试' });
            })
          }
        }
      },
      updateNews() {
        this.newsContent = this.$refs.ue.getUEContent()
        if(this.titleInput == '') {
          this.$message.error('请填写新闻标题');
        }else if(this.fromInput == '') {
          this.$message.error('请填写新闻来源');
        }else if(this.imageUrl == '') {
          this.$message.error('请上传标题图片');
        }else if(this.newsContent == '') {
          this.$message.error('请撰写新闻正文');
        }else {
          let params = {
            news_title: this.titleInput,
            news_from: this.fromInput,
            news_picture: this.imageUrl,
            news_all: this.newsContent
          }
          axios.post(api.update_news+'?id='+this.newsId, params).then(res => {
            if(res.data.status == 200){
              this.$message({ type: 'success', message: res.data.message });
              this.getData(1)
              this.tabClick(1)
              this.titleInput = ''
              this.fromInput = ''
              this.imageUrl = ''
              this.defaultMsg = ''
            }else{
              this.$message({ type: 'error', message: res.data.message });
            }
          },error =>{
            this.$message({ type: 'error', message: '服务器请求失败，请稍后再试' });
          })
        }
      },
      /*handleRemove(file, fileList) {
        console.log(file, fileList);
      },*/
      // 关闭新闻
      closeNews(news) {
        this.$confirm('此操作将删除该新闻', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          let params = {
            news_status: 0
          }
          axios.post(api.update_status+'?id='+news.id, params).then(res=>{
            if(res.data.status == 200){
              this.getData(1)
              this.$message({ type: 'success', message: res.data.message });
            }else{
              this.$message.error(res.data.message);
            }
          }, error=>{
            console.log(123)
            // this.$message.error(error.data.message);
            console.log(error)
          });
        });
      },
      // 编辑新闻
      editNews(news) {
        // console.log(news)
        this.editNewsStatus = true
        this.newsId = news.id
        this.tabClick(0)
        this.titleInput = news.news_title
        this.fromInput = news.news_from
        this.imageUrl = news.news_picture
        this.defaultMsg = news.news_all
      }
    },
    created() {
      this.getData(1)
    }
  }
</script>

<style lang="less" rel="stylesheet/less" scoped>
  @import "../common/css/_variate.less";
  .page-box {
    margin: -3% 0 0 71%;
  }
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
        width: 72%;
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
      .news-close {
        height: 0.9rem;
        min-width: 0.9rem;
        /*font-size: 18px;*/
        margin-top: 0.9rem;
        color: @bgMainColor;
        background-color: @mainColor;
        display: flex;
        -webkit-align-items: center;
        -webkit-justify-content: center;
      }
      .news-edit {
        height: 0.9rem;
        min-width: 0.9rem;
        /*font-size: 18px;*/
        margin-right: -0.9rem;
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
      width: 1.2rem;
      height: 0.4rem;
      margin: 4.6rem 0 0.6rem 2.5rem;
      color: @bgMainColor;
      background-color: @btnActiveColor;
    }
    .give-up-btn {
      width: 1.2rem;
      height: 0.4rem;
      margin: 4.6rem 0 0.6rem 1.6rem;
      color: #000000;
    }
    .upload-two-btn {
      width: 1.2rem;
      height: 0.4rem;
      margin: 4.6rem 0 0.6rem 0.7rem;
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
      margin: -1.1rem 0 0.5rem 5.25rem;
    }
    .right-input {
      width: 6rem;
      margin-bottom: 0.4rem;
    }
  }
</style>
