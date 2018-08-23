const title = 'https://fstwechat.com/fansti/';
// const title = 'http://10.0.0.130:7444/fansti/';
// const title = 'http://120.79.182.43:7444/fansti/';

const api={
  login: title + 'user/login',//用户登录
  changePwd: title + 'user/update_user',//修改密码
  get_inforcode:title + 'user/get_inforcode',//获取验证码
  forget_password:title + 'user/forget_password',//忘记密码
  get_custom:title + 'other/get_custom',//获取客服信息
  update_custom: title + 'other/update_custom',//修改客服信息
  get_user_message: title + 'users/get_user_message',//获取留言信息

  get_news_all: title + 'news/get_all',//获取新闻列表
  new_news: title + 'news/new_news',//创建新闻
  get_abo: title + 'news/get_abo',//获取新闻详情
  update_status: title + 'news/update_status',//改变新闻状态
  update_news: title + 'news/update_news',//编辑新闻

  get_all_scrapy: title + 'scrapy/get_all_scrapy',//用户查询记录

  upload_files: title + 'news/upload_files',//上传图片

  get_phone: title + 'other/get_phone',//查看白名单列表
  update_phone: title + 'other/update_phone',//增/删白名单电话
}

export default api
