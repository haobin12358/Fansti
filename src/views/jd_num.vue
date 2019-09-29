<template>
  <div class="container">
    <el-form>
      <el-form-item label="鉴定报告数">
        <el-input v-model="num"></el-input>
        <el-button @click="doSave" type="primary" size="mini" style="background: #f7cf5e;border: none;">保存</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
  import axios from 'axios';
  import api from '../api/api';

  export default {
    name: 'jd_num',

    components: {},

    data() {
      return {
        num: 0
      };
    },

    computed: {},

    created() {
      axios.get(api['get_jd_num']).then(
        res => {
          this.num = res.data.data.jd_num || 0
        }
      )
    },

    methods: {
      doSave(){
        let checkRst = /^[1-9]\d*$/.test(this.num)

        if (checkRst) {
          axios.post(api['update_jd_num'], {jd_num: this.num}).then(
            res=>{
              if(res.data.status == 200){
                this.$message.success('保存成')
              }else{
                this.$message({
                  type: 'error',
                  message: res.data.message
                });
              }
            }
          )
        } else{
          this.$message.warning('请填写合理的数字')
        }
      }
    }
  };
</script>

<style lang="less" scoped>
  .container {

  }
</style>
