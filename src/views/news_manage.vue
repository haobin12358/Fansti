<template>
  <div>
    新闻管理页
    <el-button @click="goPage">新闻编辑</el-button>
  </div>
</template>

<script>
  import news from '../common/json/news'
  export default {
    name: "news_manage",
    data() {
      return {
        news: news
      }
    },
    methods: {
      goPage() {
        this.$router.push({ path: '/upload_new' })
      }
    },
    created() {
      console.log(this.news)
    }
  }
</script>

<style scoped>

</style>
