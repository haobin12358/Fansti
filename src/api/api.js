import {
  wxRequest
} from '@/utils/wxRequest';
const debug = false;

const host =debug? 'https://dsn.apizza.net/mock/60c954072cfff536376e5acb0392c590' :'http://10.0.0.130:7444/fansti';

//  绑定用户  POST
const userBinding = params => wxRequest(params, host+'/users/user_binding');
//  查看绑定状态
const getBinding = params => wxRequest(params, host+'/users/get_binding');
//  获取微信id  POST
const getOpenid = params => wxRequest(params, host+'/users/get_openid');

//  获取新闻列表  POST
const getAllNews = params => wxRequest(params, host+`/news/get_all?page_size=${params.page_size}&page_num=${params.page_num}`);
//  获取新闻列表  POST
const getNewsAbo = params => wxRequest(params, host+`/news/get_abo?id=${params.id}`);




//  获取货物列表
const getGoodsList = params => wxRequest(params, host+`/goods/get_goods_list?page_size=${params.page_size}&page_num=${params.page_num}`);
//  获取货物详情
const getJcAbo = params => wxRequest(params, host+'/goods/get_jc_abo');
//  确认照片  POST
const retrueGoods = params => wxRequest(params, host+`/goods/retrue_goods?login_name=${params.login_name}&jcno=${params.jcno}`);

//  查询cas
const getCas = params => wxRequest(params, host+'/scrapy/get_cas');
//  查询hscode
const getHs = params => wxRequest(params, host+'/scrapy/get_hs');

//  获取红包全部内容
const getAllRed = params => wxRequest(params, host+'/reds/get_all_red');
//  留言
const makeUserMessage = params => wxRequest(params, host+`/users/make_user_message?openid=${params.openid}`);
//  获取客服信息
const getCustom = params => wxRequest(params, host+`/other/get_custom?login_name=${params.login_name}`);
//  获取个人名片
const getMyInfo = params => wxRequest(params, host+`/users/get_my_info?openid=${params.openid}`);
//  更新个人名片
const updateMyInfo = params => wxRequest(params, host+`/users/update_my_info?openid=${params.openid}`);
//  邀请用户
const addInvate = params => wxRequest(params, host+`/users/add_invate?openid=${params.openid}`);



export default {
  userBinding,
  getBinding,
  getOpenid,
  getAllNews,
  getNewsAbo,
  getGoodsList,
  getJcAbo,
  retrueGoods,
  getCustom,
  getCas,
  getHs,
  getAllRed,
  makeUserMessage,
  getMyInfo,
  updateMyInfo,
  addInvate
}
