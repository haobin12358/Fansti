import {
  wxRequest
} from '@/utils/wxRequest';
const mock = false;

const host =mock? 'https://dsn.apizza.net/mock/60c954072cfff536376e5acb0392c590' :'https://fstwechat.com/fansti';

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

//  查询dgr
const getDgr = params => wxRequest(params, host+'/scrapy/get_dgr');
//  查询鉴定信息
const getJd = params => wxRequest(params, host+'/scrapy/get_jd');
//  模糊查询鉴定信息
const getJdList = params => wxRequest(params, host+'/scrapy/get_jd_names');
//  查询tact
const getTact = params => wxRequest(params, host+'/scrapy/get_tact');
//  查询hscode 爬虫
const getHs = params => wxRequest(params, host+'/scrapy/get_hs');
//  查询cas 爬虫
const getCas = params => wxRequest(params, host+'/scrapy/get_cas');
//  查询航班信息
const getFlyno = params => wxRequest(params, host+'/scrapy/get_flyno');


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
//  获取邀请人列表
const getInvateList = params => wxRequest(params, host+`/users/get_invate_list`);

//  查询问卷
const getVote = params => wxRequest(params, host+`/votes/get_vote?VSid=${params.VSid}&VOno=${params.VOno}`);
//  做问卷 POST
const makeVote = params => wxRequest(params, host+`/votes/make_vote`);





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
  getDgr,
  getJd,
  getJdList,
  getTact,
  getFlyno,
  getAllRed,
  makeUserMessage,
  getMyInfo,
  updateMyInfo,
  addInvate,
  getInvateList,
  getVote,
  makeVote,
}
