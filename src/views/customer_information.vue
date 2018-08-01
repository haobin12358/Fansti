<template>
    <div class="m-customer">
        <tabs :tabs="tabs_data" @tabClick="tabClick"></tabs>
        <div class="m-edit-content">
          <el-form  :model="form" ref="form" :rules="rules" label-width="1.2rem" class="demo-ruleForm" >
              <el-form-item label="客服名称：" prop="name">
                <el-input v-model="form.name" class="m-input-l" placeholder="最多10个字" maxlength="10"></el-input>
              </el-form-item>

            <el-form-item label="客服电话：" prop="qq">
              <el-input v-model="form.telphone" class="m-input-l" placeholder="最多10个字" type="number"></el-input>
            </el-form-item>
            <el-form-item label="客服qq：" prop="qq">
              <el-input v-model="form.qq" class="m-input-l" placeholder="最多10个字" type="number"></el-input>
            </el-form-item>
            <el-form-item label="客服邮箱：" prop="email">
              <el-input v-model="form.email" class="m-input-l" placeholder="最多10个字" ></el-input>
            </el-form-item>

              <div class="m-bottom-btn m-flex-center">
               <span>删除</span>
              </div>
          </el-form>
        </div>
    </div>
</template>

<script>
  import tabs from '../components/common/tabs';
    export default {
      data(){
          return {
            tabs_data:[
              {
                name:'编辑',
                click:true,
                url:''
              }
            ],
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
            }
          }
      },
      components:{
        tabs
      },
      methods:{
        tabClick(index){
          let _arr = this.tabs_data;
          for(let i =0;i<_arr.length;i++){
            _arr[i].click = false;
          }
          _arr[index].click = true;
          this.tabs_data = [].concat(_arr);
        }
      }
    }
</script>

<style lang="less" rel="stylesheet/less" scoped>

</style>
