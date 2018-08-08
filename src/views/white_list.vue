<template>
  <div>
    <div class="page-box">
      <el-button class="add-btn" @click="dialogFormVisible = true">添加白名单</el-button>
      <el-dialog title="添加白名单" :visible.sync="dialogFormVisible">
        <el-form :model="dynamicValidateForm" ref="dynamicValidateForm" label-width="100px" class="demo-dynamic">
          <el-form-item prop="phone" label="手机号："
                        :rules="[
                          { required: true, message: '请输入手机号', trigger: 'blur' }
                        ]">
            <el-input v-model="dynamicValidateForm.phone" class="phone-input"></el-input>
          </el-form-item>
          <el-form-item v-for="(domain, index) in dynamicValidateForm.phones" label="手机号：" :key="domain.key" :prop="'phones.' + index + '.value'"
            :rules="{ required: true, message: '请输入手机号', trigger: 'blur' }">
            <el-input v-model="domain.value" class="phone-input"></el-input>
            <el-button @click.prevent="removeDomain(domain)" class="cancel-btn" size="small">删除</el-button>
          </el-form-item>
          <el-form-item class="bottom-button">
            <el-button @click="addDomain" class="cancel-btn" size="medium">新增</el-button>
            <el-button @click="editPhone('dynamicValidateForm', 'add')" class="add-done" size="medium">提交</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>
    </div>
    <div class="m-table">
      <table width="100%">
        <thead>
        <tr>
          <td width="35%">序号</td>
          <td width="35%">手机号</td>
          <td>操作</td>
        </tr>
        </thead>
        <tbody>
        <template v-for="(item,index) in query">
          <tr>
            <td>{{index+1}}</td>
            <td>{{item}}</td>
            <td>
              <div @click="editPhone(item, 'delete')" style="color: #5A738A">删除</div>
            </td>
          </tr>
        </template>
        </tbody>
      </table>
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
        query: [],
        dialogFormVisible: false,
        dynamicValidateForm: {
          phones: [
            // { value: '' }
          ],
          phone: ''
        },
      }
    },
    components:{ page },
    methods: {
      editPhone(formName, control) {
        if(control == 'add') {
          let that = this
          let phoneList = []
          this.$refs[formName].validate((valid) => {
            if (valid) {
              phoneList.push(that.dynamicValidateForm.phone)
              for(let i=0;i<that.dynamicValidateForm.phones.length;i++) {
                phoneList.push(that.dynamicValidateForm.phones[i].value)
              }
              let params = {
                control: control,
                phone_list: phoneList
              }
              axios.post(api.update_phone, params).then(res=>{
                if(res.data.status == 200){
                  this.getData()
                  this.dialogFormVisible = false
                  this.$message({ type: 'success', message: res.data.message });
                  this.$refs[formName].resetFields();
                }else{
                  this.$message.error(res.data.message);
                }
              }, res=>{
                this.$message.error(res.data.message);
              });
            } else {
              console.log('error submit!!');
              return false;
            }
          });
        }else if(control == 'delete') {
          let phone_list = []
          phone_list[0] = formName
          let params = {
            control: control,
            phone_list: phone_list
          }
          axios.post(api.update_phone, params).then(res=>{
            console.log(res)
            if(res.data.status == 200){
              // this.getData()
              // this.dialogFormVisible = false
              this.$message({ type: 'success', message: res.data.message });
              // this.$refs[formName].resetFields();
            }else{
              this.$message.error(res.data.message);
            }
          }, res=>{
            this.$message.error(res.data.message);
          });
        }
      },
      removeDomain(item) {
        var index = this.dynamicValidateForm.phones.indexOf(item)
        if (index !== -1) {
          this.dynamicValidateForm.phones.splice(index, 1)
        }
      },
      addDomain() {
        this.dynamicValidateForm.phones.push({
          value: '',
          key: Date.now()
        });
      },
      getData(){
        axios.get(api.get_phone).then(res => {
          if (res.data.status == 200){
            this.query = res.data.data
            // console.log(this.query)
          }else{
            this.$message.error(res.data.message);
          }
        },error => {
          this.$message.error(error.data.message);
        })
      }
    },
    created() {
      this.getData()
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
      }
    }
  }
  .page-box{
    .add-btn {
      margin: 0 0 1% 86%;
      color: @bgMainColor;
      background-color: @btnActiveColor;
    }
    .bottom-button {
      margin-bottom: 0;
      margin-left: 42%;
      .add-done {
        color: @bgMainColor;
        background-color: @btnActiveColor;
      }
    }
    .phone-input {
      width: 78%;
    }
    .cancel-btn {
      color: #000000;
      margin-left: 5%;
      border-color: @blueBorderColor;
      background-color: #ffffff;
    }
  }
</style>
