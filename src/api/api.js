// const title = 'http://10.0.0.197:7443/sharp/manager/';
// const title = 'http://120.79.182.43:7443/sharp/manager/';
// const title ='http://192.168.0.100:7443/sharp/manager/';
const title = 'http://120.79.182.43:7443/fansti/';

const api={
  login: title + 'user/login',//用户登录
  changePwd: title + 'user/update_user',//修改密码
  get_inforcode:title + 'user/get_inforcode',//获取验证码
  forget_password:title + 'user/forget_password',//忘记密码
  get_custom:title + 'other/get_custom',//获取客服信息
  update_custom: title + 'other/update_custom',//修改客服信息
}

export default api
