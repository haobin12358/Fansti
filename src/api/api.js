import {
  wxRequest
} from '@/utils/wxRequest';

const mock = true;

const host = mock ? 'https://fansti.sanbinit.cn/fansti' : 'https://fstwechat.com/fansti';

// 三期
const getReceivedList = params => wxRequest(params, host + `/control/get_received`);
const getHistoryList = params => wxRequest(params, host + `/control/get_history`);
const getReceivingList = params => wxRequest(params, host + `/control/get_receiving`);
const deleteFree = params => wxRequest(params, host + `control/delete_free?login_name=${params.login_name}`); // post
const getTruckCurr = params => wxRequest(params, host + `/control/get_truck_curr`);
const getFree = params => wxRequest(params, host + `/control/get_free?login_name=${params.login_name}`);
const updateFreeList = params => wxRequest(params, host + `control/update_free_list?login_name=${params.login_name}`);
const freeList = params => wxRequest(params, host + `/control/free_list`);
const getOutedList = params => wxRequest(params, host + `/control/get_outed_list`);
const getOutingList = params => wxRequest(params, host + `/control/get_outing_list`);

const getBzjhAbo = params => wxRequest(params, host + `/control/get_bzjh_abo`);
const getBzjhList = params => wxRequest(params, host + `/control/get_bzjh_list`);
const picOcr = params => wxRequest(params, host + `/control/pic_ocr?login_name=${params.login_name}`);
const getLevel = params => wxRequest(params, host + `/control/get_level`);
const getInJcno = params => wxRequest(params, host + `/control/get_in_jcno`);
const getInAboNojcno = params => wxRequest(params, host + `/control/get_in_abo_nojcno`);
const getInNoJcno = params => wxRequest(params, host + `/control/get_in_no_jcno`);

const updateNojcno = params => wxRequest(params, host + `/control/update_nojcno?login_name=${params.login_name}&temporary_no=${params.temporary_no}`);
const getInAboJcno = params => wxRequest(params, host + `/control/get_in_abo_jcno`);



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
const getPacker = params => wxRequest(params, host + `/control/get_packer`);
const getJcInPhotoHead = params => wxRequest(params, host + `/control/get_jc_in_photohead`);
const getJcPicIn = params => wxRequest(params, host + `/control/get_jc_pic_in`);
const exportZip = params => wxRequest(params, host + `/goods/export_zip`);
const getOpenid = params => wxRequest(params, host + '/users/get_openid2');

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
const addNewFile = params => wxRequest(params, host + `/control/add_new_file?login_name=${params.login_name}&jcno=${params.jcno}&file_type=${params.file_type}`);  // 新增文件
const deleteFile = params => wxRequest(params, host + `/control/delete_file?login_name=${params.login_name}&jcno=${params.jcno}&file_type=${params.file_type}`);  // 删除文件

const uploadFilesUrl = host + `/control/upload_files`; // post 上传文件 url


//  绑定用户  POST
const userBinding = params => wxRequest(params, host + '/users/user_binding');
//  查看绑定状态
const getBinding = params => wxRequest(params, host + '/users/get_binding');


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
const getJdNum = params => wxRequest(params, host + '/other/get_jd_num');
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
  getReceivedList,
  getHistoryList,
  getReceivingList,
  deleteFree,
  getTruckCurr,
  getFree,
  updateFreeList,
  freeList,
  getOutedList,
  getOutingList,
  getBzjhAbo,
  getBzjhList,
  picOcr,
  getLevel,
  getInJcno,
  getInAboNojcno,
  getInNoJcno,
  updateNojcno,
  getInAboJcno,

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
  getPacker,
  getJcInPhotoHead,
  getJcPicIn,

  updateWts,
  uploadFilesUrl,
  updateDzjjd,
  addIn,
  retrueOuthc,
  makeSb,
  updateQrd,
  userLoginLocal,
  saveRoyalty,
  updateRoyalty,
  exportZip,
  addNewFile,
  deleteFile,
  getJdNum,
};
