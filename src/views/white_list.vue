<template>
  <div>
    <div class="m-table">
      <table width="100%">
        <thead>
        <tr>
          <td width="15%">序号</td>
          <td width="35%">姓名</td>
          <td width="35%">手机号</td>
          <td>操作</td>
        </tr>
        </thead>
        <tbody>
        <template v-for="(item,index) in query">
          <tr>
            <td>{{index+1}}</td>
            <td>{{item.name}}</td>
            <td>{{item.telephone}}</td>
            <td>
              <div class="edit-btn" @click="editPhone(item)">编辑</div>
              <div @click="deletePhone(item)" style="color: #5A738A">删除</div>
            </td>
          </tr>
        </template>
        </tbody>
      </table>
    </div>
    <div class="page-box">
      <page :total="total_page"></page>
      <el-button class="add-btn" @click="dialogFormVisible = true">添加白名单</el-button>
      <el-dialog title="添加白名单" :visible.sync="dialogFormVisible">
        <el-form :model="form" :rules="rules" ref="form">
          <el-form-item label="姓 名：" :label-width="formLabelWidth">
            <el-input v-model="form.name" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="手机号：" :label-width="formLabelWidth">
            <el-input v-model="form.telephone" auto-complete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible = false" class="cancel-btn">取 消</el-button>
          <el-button @click="addDone('form')" class="add-done">确 定</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
  import page from '../components/common/page';
  import api from "../api/api";
  import axios from 'axios';

  export default {
    name: "white_list",
    data() {
      return {
        query: [
          { name: '张三', telephone: '17756978822' },
          { name: '李四', telephone: '17756978822' },
          { name: '王五', telephone: '17756978822' },
          { name: '李四', telephone: '17756978822' },
          { name: '王五', telephone: '17756978822' },
          { name: '李四', telephone: '17756978822' },
          { name: '王五', telephone: '17756978822' },
          { name: '李四', telephone: '17756978822' },
          { name: '王五', telephone: '17756978822' },
          { name: '李四', telephone: '17756978822' }
        ],
        page_size:10,
        total_num:5,
        current_page:1,
        total_page:0,
        dialogFormVisible: false,
        form: {
          name: '',
          telephone: ''
        },
        rules: {
          name: [
            { required: true, message: '请输入姓名', trigger: 'blur' }
          ],
          telephone:[
            { required: true, message: '请输入手机号', trigger: 'blur' }
          ]
        },
        formLabelWidth: '120px'
      }
    },
    components:{ page },
    methods: {
      getData(v){
        let params = {
          page_size: this.page_size,
          page_num: Number(v || this.current_page),
          select_name: this.select_name
        }
        /*axios.get(api.get_all_scrapy, { params: params }).then(res => {
          if (res.data.status == 200){
            this.query = res.data.data
            console.log(this.query)
            this.total_num = res.data.data.count;
            this.total_page = Math.ceil(this.total_num / this.page_size);
            console.log(this.total_page)
          }else{
            this.$message.error(res.data.message);
          }
        },error => {
          this.$message.error(error.data.message);
        })*/
      },
      /*分页点击*/
      pageChange(v){
        console.log(v)
        if(v == this.current_page){
          this.$message({ message: '这已经是第' + v + '页数据了', type: 'warning' });
          return false;
        }
        this.current_page = v;
        this.getData(v);
      },
      editPhone(item) {
        console.log('editPhone', item)
      },
      deletePhone(item) {
        console.log('deletePhone', item)
      },
      addDone(formName) {
        // this.dialogFormVisible = false
        let that = this;
        this.$refs[formName].validate((valid) => {
          if (valid) {
            axios.post(api.forget_password,that.ruleForm).
            then(res=>{
              if(res.data.status == 200){
                this.$router.push('/login');
                //清空Cookie

                let exdate = new Date(); //获取时间
                exdate.setTime(exdate.getTime() + 24 * 60 * 60 * 1000 * -1); //保存的天数
                //字符串拼接cookie
                window.document.cookie = "userName" + "=" + '' + ";path=/;expires=" + exdate.toGMTString();
                window.document.cookie = "userPwd" + "=" + '' + ";path=/;expires=" + exdate.toGMTString();

              }else{
                MessageBox({ title:'提示', message:res.data.message,
                  callback: action => {

                  }
                })
              }
            }, res=>{
              MessageBox({ title:'提示', message:res.data.message,
                callback: action => {

                }
              })
            });
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      }
    },
    created() {
      this.getData(1)
      this.total_page = 10
    }
  }
</script>

<style lang="less" rel="stylesheet/less" scoped>
  @import "../common/css/_variate.less";
  .m-table{
    width: 14.4rem;
    table{
      thead{
        td{
          text-align: center;
          font-size: 0.18rem;
          font-weight: 600;
          padding-bottom: 0.2rem;
        }
      }
      tbody{
        td{
          text-align: center;
          border-bottom: 1px solid @borderColor;
          padding: 0.23rem 0;
        }
        .edit-btn {
          width: 50%;
          float: left;
          color: @sidebarBgColor;
        }
      }
    }
  }
  .page-box{
    .add-btn {
      margin: -2% 0 0 86%;
      color: @bgMainColor;
      background-color: @btnActiveColor;
    }
    .dialog-footer {
      .cancel-btn {
        color: #000000;
        border-color: @blueBorderColor;
        background-color: #ffffff;
      }
      .add-done {
        color: @bgMainColor;
        background-color: @btnActiveColor;
      }
    }
  }
</style>
