<template>
  <div>
    新闻管理页
    <el-button @click="goPage">新闻编辑</el-button>
  </div>
</template>

<script>
    export default {
      name: "news_manage",
      data() {
        return {

        }
      },
      methods: {
        goPage() {
          this.$router.push({ path: '/upload_new' })
        }
      }
    }
</script>

<style scoped>

</style>
