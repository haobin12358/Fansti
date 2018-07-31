import {
  wxRequest
} from '@/utils/wxRequest';

const host = 'https://h878.cn:7444/fansti';

//  绑定用户  POST
const userBinding = params => wxRequest(params, host+'/users/user_binding');
//  查看绑定状态
const getBinding = params => wxRequest(params, host+'/users/get_binding');
//  获取微信id  POST
const getOpenid = params => wxRequest(params, host+'/users/get_openid');

//  获取货物列表
const getGoodsList = params => wxRequest(params, host+'/goods/get_goods_list');
//  获取货物详情
const getJcAbo = params => wxRequest(params, host+'/users/get_jc_abo');

//  获取客服信息
const getCustom = params => wxRequest(params, host+'/other/get_custom');

//  查询cas
const getCas = params => wxRequest(params, host+'/scrapy/get_cas');
//  查询hscode
const getHs = params => wxRequest(params, host+'/scrapy/get_hs');

//  获取红包全部内容
const getAllRed = params => wxRequest(params, host+'/reds/get_all_red');
//  留言
const makeUserMessage = params => wxRequest(params, host+'/users/make_user_message');



export default {
  userBinding,
  getBinding,
  getOpenid,
  getGoodsList,
  getJcAbo,
  getCustom,
  getCas,
  getHs,
  getAllRed,
  makeUserMessage
}
