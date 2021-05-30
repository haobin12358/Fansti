import wepy from 'wepy';
import tip from './tip';

const wxRequest = async (params = {}, url) => {
  let showLoading = true;
  showLoading = !params._noLoading;
  if (showLoading) {
    tip.loading('数据加载中...');
    // wepy.showNavigationBarLoading();
  }
  // request api没有分query和data字段,因此在post时就比较有些不合理
  let data = params.query || {};
  // data.time = TIMESTAMP;

  let res = null;

  res = await wepy.request({
    url: url,
    method: params.method || 'GET',
    data: data,
    header: { 'Content-Type': params.contentType || 'application/json' }
  });

  if (showLoading) {
    tip.loaded();
    // wepy.hideNavigationBarLoading();
  }

  if(res.data.status != 200){
    tip.alert(res.data.message)
  }
  return res;
};


module.exports = {
  wxRequest
};
