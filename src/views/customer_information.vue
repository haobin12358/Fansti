<template>
    <div class="m-customer">
        <p class="m-title">客服信息编辑</p>
        <div class="m-edit-content">
          <ul class="m-card">
            <li @click="show_modal">
              <img src="" alt="" class="m-img">
              <p>姓名</p>
              <p>454512454545</p>
              <!--<span class="m-close"></span>-->
            </li>
          </ul>
        </div>
      <el-dialog
        title="编辑"
        :visible.sync="showModal"
        width="50%"
        center>
        <el-form  :model="form" ref="form" :rules="rules" label-width="2rem" class="demo-ruleForm" >
          <el-form-item label="客服名称：" prop="name">
            <el-input v-model="form.name" class="m-input-l" placeholder="此处为客服名称" maxlength="10"></el-input>
          </el-form-item>

          <el-form-item label="客服电话：" prop="qq">
            <el-input v-model="form.telphone" class="m-input-l" placeholder="此处为客服电话" type="number"></el-input>
          </el-form-item>
          <el-form-item label="客服qq：" prop="qq">
            <el-input v-model="form.qq" class="m-input-l" placeholder="此处为客服qq" type="number"></el-input>
          </el-form-item>
          <el-form-item label="客服邮箱：" prop="email">
            <el-input v-model="form.email" class="m-input-l" placeholder="此处为客服邮箱" ></el-input>
          </el-form-item>

          <div class="m-bottom-btn m-flex-center">
            <span class="m-btn active" @click="updateData">修改</span>
          </div>
        </el-form>
      </el-dialog>
    </div>
</template>

<script>
    import api from '../api/api';
    import axios from 'axios';
    export default {
      data(){
          return {
            form:{
              name:'',
              qq:'',
              telphone:'',
              email:''
            },
            rules:{
              name:[
                { required: true, message: '请输入客服名称', trigger: 'blur' }
              ],
              qq:[
                {required:true,message:'请输入客户qq',trigger:'blur'}
              ],
              telphone:[
                {required:true,message:'请输入客户电话',trigger:'blur'}
              ],
              email:[
                {required:true,message:'请输入客户邮箱',trigger:'blur'}
              ]
            },
            showModal:false,
            customer_data:{
              name:'',
              qq:'',
              telphone:'',
              email:''
            }
          }
      },
      methods:{
        show_modal(){
          this.showModal = true;
          this.from.name = this.customer_data.name;
          this.from.qq = this.customer_data.qq;
          this.from.telphone= this.customer_data.telphone;
          this.from.email = this.customer_data.email;
        },
        getData(){
          axios.get(api.get_custom).then(res => {
            if(res.data.status == 200){
              this.customer_data = res.data.data;
            }else{
              this.$message.error(res.data.message);
            }
          },error => {
            this.$message.error(error.data.message);
          })
        },
        updateData(){
          let that = this;
          this.$refs['form'].validate((valid) => {
            if (valid) {
              axios.post(api.update_custom,this.form).then(res => {
                if(res.data.status == 200){
                  this.$message({
                    type:'success',
                    message:'修改信息成功'
                  });
                }else{
                  this.$message.error(res.data.message);
                }
              },error => {
                this.$message.error(error.data.message);
              })
            }
          })
        }

      }
    }
</script>

<style lang="less" rel="stylesheet/less" scoped>
  @import "../common/css/_variate";
.m-input-l{
  width: 6rem;
}
  .m-customer{
    .m-title{
      font-size: 0.18rem;
      margin-bottom: 0.3rem;
    }
    ul.m-card{
      display: flex;
      flex-flow: row;
      align-content: center;
      flex-wrap: wrap;
      li{
        position: relative;
        width: 2.6rem;
        padding: 0.2rem;
        height: 3.6rem;
        border: 1px solid @borderColor;
        margin-right: 0.6rem;
        margin-bottom: 0.3rem;
        cursor: pointer;
        .m-img{
          display: block;
          width: 2.6rem;
          height: 2.6rem;
          border: 1px solid @borderColor;
          margin-bottom: 0.2rem;
        }
        p{
          font-size: 0.14rem;
          text-align: center;
          line-height: 0.34rem;
        }
        .m-close{
          position: absolute;
          top:0;
          right: -0.4rem;
          width: 0.3rem;
          height: 0.3rem;
          background: url("../common/images/icon-close.png");
          background-size: 100%;
        }
      }
    }
  }
  .m-bottom-btn{
    margin: 0.5rem;
    .m-btn{
      display: inline-block;
      width: 0.8rem;
      height: 0.4rem;
      line-height: 0.4rem;
      text-align: center;
      background-color: @btnColor;
      margin-right: 0.4rem;
      cursor: pointer;
      color: #fff;
      &.active{
        background-color: @btnActiveColor;
      }
    }
  }
</style>
