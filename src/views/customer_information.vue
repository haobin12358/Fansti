<template>
    <div class="m-customer">
        <tabs :tabs="tabs_data" @tabClick="tabClick"></tabs>
        <div>
          123123
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
                name:'上传',
                click:true,
                url:''
              },
              {
                name:'编辑',
                click:false,
                url:''
              }
            ]
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
