import {
  wxRequest
} from '@/utils/wxRequest';

const mock = false;

const host = mock ? 'https://dsn.apizza.net/mock/60c954072cfff536376e5acb0392c590' : 'https://fstwechat.com/fansti';

// 计划
const getTodayList = params => wxRequest(params, host + `/control/get_today_list`);
const getCJcAbo = params => wxRequest(params, host + `/control/get_jc_abo`);
const getHandoverList = params => wxRequest(params, host + `/control/get_handover_list`);
const getJcPic = params => wxRequest(params, host + `/control/get_jc_pic`);
const getJcCb = params => wxRequest(params, host + `/control/get_jc_cb`);
const getFkdw = params => wxRequest(params, host + `/control/get_fkdw`);
const getFyzl = params => wxRequest(params, host + `/control/get_fyzl`);
const getInAbo = params => wxRequest(params, host + `/control/get_in_abo`);
const getOutAbo = params => wxRequest(params, host + `/control/get_out_abo`);
const getHcAbo = params => wxRequest(params, host + `/control/get_hc_abo`);
const getSbList = params => wxRequest(params, host + `/control/get_sb_list`);
const getBzsmList = params => wxRequest(params, host + `/control/get_bzsm_list`);
const getCJdList = params => wxRequest(params, host + `/control/get_jd_list`);
const getSbnoList = params => wxRequest(params, host + `/control/get_sbno_list`);

// 修改 都是post
const updateWts = params => wxRequest(params, host + `/control/update_wts?login_name=${params.login_name}&jcno=${params.jcno}`);  // 交单
const saveRoyalty = params => wxRequest(params, host + `/control/save_royalty?login_name=${params.login_name}&jcno=${params.jcno}`);  // 保存包装人员
const updateRoyalty = params => wxRequest(params, host + `/control/update_royalty?login_name=${params.login_name}&jcno=${params.jcno}`);  // 确认包装/完成
const updateDzjjd = params => wxRequest(params, host + `/control/update_dzjjd?login_name=${params.login_name}&jcno=${params.jcno}`);  // 库房/货场确认
const addIn = params => wxRequest(params, host + `/control/add_in?login_name=${params.login_name}&jcno=${params.jcno}`);  // 保存入库明细
const retrueOuthc = params => wxRequest(params, host + `/control/retrue_outhc?login_name=${params.login_name}&jcno=${params.jcno}`);  // 出库/货场确认
const makeSb = params => wxRequest(params, host + `/control/make_sb?login_name=${params.login_name}&jcno=${params.jcno}`);  // 提交申报单
const updateQrd = params => wxRequest(params, host + `/control/update_qrd?login_name=${params.login_name}&jcno=${params.jcno}&qrd_type=${params.qrd_type}`);  // 添加/编辑/删除成本
const userLoginLocal = params => wxRequest(params, host + `/users/user_login_local`);  // 内部办公登录

const uploadFilesUrl = host + `/control/upload_files`; // post 上传文件 url


//  绑定用户  POST
const userBinding = params => wxRequest(params, host + '/users/user_binding');
//  查看绑定状态
const getBinding = params => wxRequest(params, host + '/users/get_binding');
//  获取微信id  POST
const getOpenid = params => wxRequest(params, host + '/users/get_openid');

//  获取新闻列表  POST
const getAllNews = params => wxRequest(params, host + `/news/get_all?page_size=${params.page_size}&page_num=${params.page_num}`);
//  获取新闻列表  POST
const getNewsAbo = params => wxRequest(params, host + `/news/get_abo?id=${params.id}`);

//  获取支付数据
const payService = params => wxRequest(params, host + `/pay/pay_service`);


//  获取货物列表
const getGoodsList = params => wxRequest(params, host + `/goods/get_goods_list`);
//  获取货物详情
const getJcAbo = params => wxRequest(params, host + '/goods/get_jc_abo');
//  确认照片  POST
const retrueGoods = params => wxRequest(params, host + `/goods/retrue_goods?login_name=${params.login_name}&jcno=${params.jcno}`);

//  查询dgr
const getDgr = params => wxRequest(params, host + '/scrapy/get_dgr');
//  查询鉴定信息
const getJd = params => wxRequest(params, host + '/scrapy/get_jd');
//  模糊查询鉴定信息
const getJdList = params => wxRequest(params, host + '/scrapy/get_jd_names');
//  查询tact
const getTact = params => wxRequest(params, host + '/scrapy/get_tact');
//  查询hscode 爬虫
const getHs = params => wxRequest(params, host + '/scrapy/get_hs');
//  查询cas 爬虫
const getCas = params => wxRequest(params, host + '/scrapy/get_cas');
//  查询航班信息
const getFlyno = params => wxRequest(params, host + '/scrapy/get_flyno');


//  获取红包全部内容
const getAllRed = params => wxRequest(params, host + '/reds/get_all_red');
const receiveRed = params => wxRequest(params, host + '/reds/receive_red');
const receiveRedQuery = params => wxRequest(params, host + '/reds/receive_red_query');
//  留言
const makeUserMessage = params => wxRequest(params, host + `/users/make_user_message?openid=${params.openid}`);
//  获取客服信息
const getCustom = params => wxRequest(params, host + `/other/get_custom?login_name=${params.login_name}`);
//  获取个人名片
const getMyInfo = params => wxRequest(params, host + `/users/get_my_info?openid=${params.openid}`);
//  更新个人名片
const updateMyInfo = params => wxRequest(params, host + `/users/update_my_info?openid=${params.openid}`);
//  邀请用户
const addInvate = params => wxRequest(params, host + `/users/add_invate?openid=${params.openid}`);
//  获取邀请人列表
const getInvateList = params => wxRequest(params, host + `/users/get_invate_list`);

//  查询问卷
const getVote = params => wxRequest(params, host + `/votes/get_vote?VSid=${params.VSid}&VOno=${params.VOno}`);
//  做问卷 POST
const makeVote = params => wxRequest(params, host + `/votes/make_vote`);


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
  receiveRed,
  receiveRedQuery,
  payService,
  getTodayList,
  getCJcAbo,
  getHandoverList,
  getJcPic,
  getJcCb,
  getFkdw,
  getFyzl,
  getInAbo,
  getOutAbo,
  getHcAbo,
  getSbList,
  getBzsmList,
  getCJdList,
  getSbnoList,

  updateWts,
  uploadFilesUrl,
  updateDzjjd,
  addIn,
  retrueOuthc,
  makeSb,
  updateQrd,
  userLoginLocal,
  saveRoyalty,
  updateRoyalty
};
