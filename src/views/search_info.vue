<template>
  <div class="m-search">
    <template v-for="(item,index) in list_data">
      <div class="m-one-upload">
        <h3>{{item.label}}</h3>
        <div class="m-select-input">
          <div class="inputbg">
            {{item.name || '选择文件上传,只支持excel文件'}}
            <input type="file" :id="item.url"
                   accept=".csv, application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                   @change="selectFile($event,item,index)">
          </div>
          <span class="m-btn" @click="uploadFile(index)">上传</span>
          <u class="m-down" @click="downloadFile(index)">点击下载模板</u>
        </div>
      </div>
    </template>

  </div>
</template>

<script>
  import axios from 'axios';
  import api from '../api/api';

  export default {
    data() {
      return {
        list_data: [
          {
            label: 'DGR',
            name: '',
            value: null,
            url: 'upload_dgr',
            down: 'DGR'
          },
          // {
          //   label:'鉴定报告',
          //   name:'',
          //   value:null,
          //   url:''
          // },
          {
            label: 'TACT',
            name: '',
            value: null,
            url: 'upload_tact',
            down: 'TACT'
          },
          // {
          //   label:'HS code',
          //   name:'',
          //   value:null,
          //   url:''
          // },
          // {
          //   label:'CAS',
          //   name:'',
          //   value:null,
          //   url:''
          // },
          {
            label: '航班信息',
            name: '',
            value: null,
            url: 'update_airline',
            down: 'AIRLINE'
          },
          {
            label: '询价模板',
            name: '',
            value: null,
            url: 'upload_enquiry',
            down: 'enquiry'
          }
        ]
      };
    },
    methods: {
      selectFile(e, item, index) {
        let form = new FormData();

        this.list_data[index].name = e.target.files[0].name;
        form.append('file', e.target.files[0]);
        this.list_data[index].value = form;
      },
      uploadFile(index) {
        if (this.list_data[index].value == null || this.list_data[index].value == '') {
          this.$message({
            type: 'warning',
            message: '请先选择文件'
          });
          return false;
        }

        axios.post(api[this.list_data[index].url], this.list_data[index].value).then(res => {
          if (res.data.status == 200) {
            this.$message({
              type: 'success',
              message: '上传成功'
            });
            // this.list_data[index].value = '';
            // this.list_data[index].name = '';
            // let file = document.getElementById(this.list_data[index].url);
            // file.value = '';
          } else {
            this.$message({
              type: 'error',
              message: res.data.message
            });
          }
        });
      },
      downloadFile(index) {
        window.open(api.get_template_file + '?filetype=' + this.list_data[index].down);
      }
    }
  };
</script>

<style lang="less" rel="stylesheet/less" scoped>
  @import "../common/css/index";

  .m-one-upload {
    margin-top: 0.2rem;
    h3 {
      margin-bottom: 0.2rem;
    }
    .m-select-input {
      .flex-row(flex-start);
      .inputbg {
        margin-right: 10px;
        border: 1px solid @borderColor;
        color: @greyColor;
        background-color: #fbfdff;
        -webkit-box-sizing: border-box;
        box-sizing: border-box;
        position: relative;
        width: 9rem;
        height: 0.4rem;
        line-height: 0.4rem;
        padding-left: 0.2rem;
      }
      .inputbg input {
        position: absolute;
        top: 0;
        left: 0;
        opacity: 0;
        filter: alpha(opacity=0);
        width: 9rem;
        height: 0.4rem;
        line-height: 0.4rem;
        cursor: pointer;
      }
      .m-btn {
        display: block;
        width: 1.6rem;
        height: 0.4rem;
        line-height: 0.4rem;
        text-align: center;
        background-color: @btnActiveColor;
        color: #fff;
        margin: 0 0.3rem;
        cursor: pointer;
      }
      .m-down {
        color: #a0afba;
        cursor: pointer;
      }
    }

  }

</style>
