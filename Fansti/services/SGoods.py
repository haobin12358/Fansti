# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from Fansti.models.model import AIR_HWYS_WTS, AIR_HWYS_DCD, AIR_HWYS_PHOTOS, AIR_HWYS_FILE, AIR_HWYS_DCD_JLD, \
    GOODS_RETRUE, AIR_HWYS_DZJJD, AIR_HWYS_QRD, D_CHARGE_COMPANY, D_CHARGE_TYPE, AIR_HWYS_CKMXD, AIR_HWYS_OUTWAREHOUSE, \
    AIR_HWYS_INGOODYARD, AIR_HWYS_DGD_UPLOAD
from Fansti.services.SBase import SBase, close_session
from sqlalchemy import func, or_

class SGoods(SBase):

    @close_session
    def get_all_goods_by_user(self, accounts, page_size, page_num):
        return self.session.query(AIR_HWYS_WTS.ydno, AIR_HWYS_WTS.jcno, AIR_HWYS_WTS.destination, AIR_HWYS_WTS.hxno,
                                  AIR_HWYS_WTS.jsbzcc)\
            .filter_by(accounts=accounts).offset((page_num - 1) * page_size).limit(page_size).all()

    @close_session
    def get_all_goods_by_filter(self, wtsfilter, page_size, page_num):
        return self.session.query(
            AIR_HWYS_WTS.ydno, AIR_HWYS_WTS.jcno, AIR_HWYS_WTS.destination, AIR_HWYS_WTS.hxno, AIR_HWYS_WTS.jsbzcc,
            AIR_HWYS_WTS.accounts, AIR_HWYS_WTS.xsr, AIR_HWYS_WTS.flag_date, AIR_HWYS_WTS.transtime, AIR_HWYS_WTS.isphoto,
            AIR_HWYS_WTS.wphw)\
                .order_by(func.nvl(AIR_HWYS_WTS.jd_date, AIR_HWYS_WTS.jd_time).desc(), AIR_HWYS_WTS.jcno.desc())\
                .filter(*wtsfilter).offset((page_num - 1) * page_size).limit(page_size).all()

    @close_session
    def get_xsr_by_user(self, accounts):
        return self.session.query(AIR_HWYS_WTS.xsr).filter_by(accounts=accounts).first()

    @close_session
    def get_AIR_HWYS_WTS_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_WTS.jd_date, AIR_HWYS_WTS.jd_time).filter(AIR_HWYS_WTS.jcno == jcno).first()

    @close_session
    def get_dctime_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_DCD.hbdate1).filter_by(jcno=jcno).first()

    @close_session
    def get_in_order_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_PHOTOS.photourl, AIR_HWYS_PHOTOS.czr, AIR_HWYS_PHOTOS.createtime)\
            .filter_by(jcno=jcno).filter_by(phototype='in').all()

    @close_session
    def get_out_order_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_PHOTOS.photourl, AIR_HWYS_PHOTOS.czr, AIR_HWYS_PHOTOS.createtime) \
            .filter_by(jcno=jcno).filter_by(phototype='out').all()

    @close_session
    def get_weight_order_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_PHOTOS.photourl, AIR_HWYS_PHOTOS.czr, AIR_HWYS_PHOTOS.createtime) \
            .filter_by(jcno=jcno).filter_by(phototype='weight').all()

    @close_session
    def get_by_order_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_PHOTOS.photourl, AIR_HWYS_PHOTOS.czr, AIR_HWYS_PHOTOS.createtime) \
            .filter_by(jcno=jcno).filter_by(phototype='by').all()

    @close_session
    def get_content_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_FILE.content)\
            .filter(AIR_HWYS_FILE.content.like("%报关单%"), AIR_HWYS_FILE.jcno == jcno).first()

    @close_session
    def get_awb_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_FILE.content)\
            .filter_by(content='AWB').filter_by(jcno=jcno).first()

    @close_session
    def get_jd_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_WTS.jd_date, AIR_HWYS_WTS.jd_time).filter_by(jcno=jcno).first()

    @close_session
    def get_hbdate_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_DCD_JLD.mes1).filter_by(jcno=jcno).first()

    @close_session
    def get_dhmes_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_DCD_JLD.dhmes).filter_by(jcno=jcno).first()

    @close_session
    def get_goods_abo_by_jcno(self, jcno):
        return self.session.query(
            AIR_HWYS_WTS.ydno, AIR_HWYS_WTS.destination, AIR_HWYS_WTS.jcno, AIR_HWYS_WTS.enhwpm, AIR_HWYS_WTS.czr,
            AIR_HWYS_WTS.company, AIR_HWYS_WTS.contract).filter_by(jcno=jcno).first()

    @close_session
    def get_goods_abo_by_filter(self, dcdfilter):
        return self.session.query(AIR_HWYS_WTS.ydno, AIR_HWYS_WTS.destination, AIR_HWYS_WTS.jcno, AIR_HWYS_WTS.enhwpm) \
            .filter(*dcdfilter).first()

    @close_session
    def get_quantity_weight_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_DCD.quantity, AIR_HWYS_DCD.weight).filter_by(jcno=jcno).first()

    @close_session
    def get_accounts_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_WTS.accounts).filter_by(jcno=jcno).first()

    @close_session
    def get_in_out_weight_by_jcno(self, jcno):
        return self.session.query(GOODS_RETRUE.in_pic, GOODS_RETRUE.out_pic, GOODS_RETRUE.weight_pic)\
            .filter_by(jcno=jcno).all()

    @close_session
    def get_retrue_by_jcno_in(self,jcno):
        return self.session.query(GOODS_RETRUE.id).filter_by(in_pic="1").filter_by(jcno=jcno).first()

    @close_session
    def get_retrue_by_jcno_out(self, jcno):
        return self.session.query(GOODS_RETRUE.id).filter_by(out_pic="1").filter_by(jcno=jcno).first()

    @close_session
    def get_retrue_by_jcno_weight(self, jcno):
        return self.session.query(GOODS_RETRUE.id).filter_by(weight_pic="1").filter_by(jcno=jcno).first()

    @close_session
    def get_retrue_by_jcno_loginname(self, jcno, login_name):
        return self.session.query(GOODS_RETRUE.id).filter_by(jcno=jcno).filter_by(login_name=login_name).first()

    @close_session
    def update_goods_retrue_by_id(self, id, goods_retrue):
        self.session.query(GOODS_RETRUE).filter_by(id=id).update(goods_retrue)
        return True

    @close_session
    def get_retrue_by_login_name(self, login_name):
        return self.session.query(GOODS_RETRUE.id).filter_by(login_name=login_name).all()

    @close_session
    def get_std(self, jcno):
        return self.session.query(AIR_HWYS_DCD_JLD.mes1).filter_by(jcno=jcno).first()

    @close_session
    def get_awbfile_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_FILE.filename) \
            .filter_by(content='AWB').filter_by(jcno=jcno).all()

    @close_session
    def get_contentfile_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_FILE.filename).filter_by(content='报关单').filter_by(jcno=jcno).all()

    @close_session
    def get_contentsb_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_FILE.filename).filter_by(content='申报单').filter_by(jcno=jcno).all()

    @close_session
    def get_contentfx_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_FILE.filename).filter_by(content='放行单').filter_by(jcno=jcno).all()

    @close_session
    def get_contentdgd_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_FILE.filename).filter_by(content='DGD').filter_by(jcno=jcno).all()

    @close_session
    def get_yanwu_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_DCD_JLD.id).filter_by(jcno=jcno).filter_by(is_delay="1").all()

    @close_session
    def get_control_goods(self, jcno):
        return self.session.query(AIR_HWYS_WTS.jcno, AIR_HWYS_WTS.ydno, AIR_HWYS_WTS.czr, AIR_HWYS_WTS.destination,
                                  AIR_HWYS_WTS.jsbzcc, AIR_HWYS_WTS.company, AIR_HWYS_WTS.contract, AIR_HWYS_WTS.hwpm,
                                  AIR_HWYS_WTS.wh_require, AIR_HWYS_WTS.instruction, AIR_HWYS_WTS.arrivetime,
                                  AIR_HWYS_WTS.hxno, AIR_HWYS_WTS.jd_date, AIR_HWYS_WTS.jd_time, AIR_HWYS_WTS.contract)\
            .filter_by(jcno=jcno).first()

    @close_session
    def get_dzjjd(self, jcno):
        return self.session.query(AIR_HWYS_DZJJD.hc_bz, AIR_HWYS_DZJJD.kf_bz).filter_by(jcno=jcno).first()

    @close_session
    def get_dcd_flight(self, jcno):
        return self.session.query(AIR_HWYS_DCD.flightdate, AIR_HWYS_DCD.hbdate1, AIR_HWYS_DCD.flight)\
            .filter_by(jcno=jcno).first()

    @close_session
    def get_wts_handover(self, jcno):
        return self.session.query(AIR_HWYS_WTS.jcno, AIR_HWYS_WTS.ydno, AIR_HWYS_WTS.czr, AIR_HWYS_WTS.xsr)\
            .filter_by(jcno=jcno).first()

    @close_session
    def get_dzjjd_handover(self, jcno):
        return self.session.query(AIR_HWYS_DZJJD.kfqr_date, AIR_HWYS_DZJJD.hcqr_date, AIR_HWYS_DZJJD.rkd_flag,
                                  AIR_HWYS_DZJJD.ungoods_flag,
                                  AIR_HWYS_DZJJD.sjwj_flag, AIR_HWYS_DZJJD.goods_file, AIR_HWYS_DZJJD.tp_mass,
                                  AIR_HWYS_DZJJD.state_goods, AIR_HWYS_DZJJD.tp_size, AIR_HWYS_DZJJD.temperature,
                                  AIR_HWYS_DZJJD.dtp, AIR_HWYS_DZJJD.gb_flag, AIR_HWYS_DZJJD.gb_num,
                                  AIR_HWYS_DZJJD.lb_flag, AIR_HWYS_DZJJD.lb_num,
                                  AIR_HWYS_DZJJD.in_mark, AIR_HWYS_DZJJD.out_mark, AIR_HWYS_DZJJD.ybzbl_flag,
                                  AIR_HWYS_DZJJD.nbzsm, AIR_HWYS_DZJJD.bzpm, AIR_HWYS_DZJJD.kf_ry,
                                  AIR_HWYS_DZJJD.kf_bz, AIR_HWYS_DZJJD.hc_ry, AIR_HWYS_DZJJD.hc_bz)\
            .filter_by(jcno=jcno).first()

    def get_jc_qrd(self, jcno):
        return self.session.query(AIR_HWYS_QRD.id, AIR_HWYS_QRD.jcno, AIR_HWYS_QRD.ydno, AIR_HWYS_QRD.fkdw,
                                  AIR_HWYS_QRD.byzd1,
                                  AIR_HWYS_QRD.byzd3, AIR_HWYS_QRD.curr, AIR_HWYS_QRD.amount, AIR_HWYS_QRD.doc)\
            .filter_by(jcno=jcno).filter_by(byzd1="1").all()

    def get_fkdw(self, company):
        return self.session.query(D_CHARGE_COMPANY.id, D_CHARGE_COMPANY.code, D_CHARGE_COMPANY.company)\
            .filter(D_CHARGE_COMPANY.company.like("%{0}%".format(company))).all()

    def get_fkzl(self, charge_cname):
        return self.session.query(D_CHARGE_TYPE.charge_code, D_CHARGE_TYPE.charge_cname, D_CHARGE_TYPE.d_price)\
            .filter(D_CHARGE_TYPE.charge_cname.like("%{0}%".format(charge_cname))).all()

    def get_ckmxd_wts(self, jcno):
        return self.session.query(AIR_HWYS_WTS.jcno, AIR_HWYS_WTS.czr, AIR_HWYS_WTS.hwpm, AIR_HWYS_WTS.ydno)\
            .filter_by(jcno=jcno).first()

    def get_ckmxd_abo(self, jcno):
        return self.session.query(AIR_HWYS_CKMXD.warehouse_address, AIR_HWYS_CKMXD.enter_time,
                                  AIR_HWYS_CKMXD.goods_quantity, AIR_HWYS_CKMXD.delivery_unit,
                                  AIR_HWYS_CKMXD.goods_weight, AIR_HWYS_CKMXD.cargo_size, AIR_HWYS_CKMXD.client_name,
                                  AIR_HWYS_CKMXD.remark)\
            .filter_by(jcno=jcno).first()

    def get_outwarehouse(self, ydno):
        return self.session.query(AIR_HWYS_OUTWAREHOUSE.submitter, AIR_HWYS_OUTWAREHOUSE.submit_time)\
            .filter_by(ydno=ydno).first()

    def get_ingoodyard(self, ydno):
        return self.session.query(AIR_HWYS_INGOODYARD.submitter, AIR_HWYS_INGOODYARD.submit_time)\
            .filter_by(ydno=ydno).first()

    def get_sb_list(self, jcno):
        return self.session.query(AIR_HWYS_DGD_UPLOAD.id, AIR_HWYS_DGD_UPLOAD.file_name, AIR_HWYS_DGD_UPLOAD.file_url)\
            .filter_by(jcno=jcno).filter_by(file_type="申报单").all()

    def get_bzsm_list(self, jcno):
        return self.session.query(AIR_HWYS_DGD_UPLOAD.id, AIR_HWYS_DGD_UPLOAD.file_name, AIR_HWYS_DGD_UPLOAD.file_url) \
            .filter_by(jcno=jcno).filter_by(file_type="包装明细").all()

    def get_jd_list(self, jcno):
        return self.session.query(AIR_HWYS_DGD_UPLOAD.id, AIR_HWYS_DGD_UPLOAD.file_name, AIR_HWYS_DGD_UPLOAD.file_url) \
            .filter_by(jcno=jcno).filter_by(file_type="鉴定文件").all()

    def get_sbno_list_like_ydno_jcno(self, select_name, page_size, page_num):
        return self.session.query(AIR_HWYS_WTS.jcno, AIR_HWYS_WTS.czr, AIR_HWYS_WTS.ydno, AIR_HWYS_WTS.destination)\
            .filter(or_(AIR_HWYS_WTS.jcno.like("%{0}%".format(select_name)), AIR_HWYS_WTS.ydno.like("%{0}%".format(select_name)))) \
            .offset((page_num - 1) * page_size).limit(page_size)\
            .all()

    def update_wts(self, wts_id, wts):
        self.session.query(AIR_HWYS_WTS).filter_by(id=wts_id).update(wts)
        self.session.commit()
        return True

    def get_id_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_WTS.id, AIR_HWYS_WTS.ydno).filter_by(jcno=jcno).first()

    def update_dzjjd(self, dzjjd_id, dzjjd):
        self.session.query(AIR_HWYS_DZJJD).filter_by(jjd_id=dzjjd_id).update(dzjjd)
        self.session.commit()
        return True

    def get_jjdid_by_jcno(self, jcno):
        return self.session.query(AIR_HWYS_DZJJD.jjd_id).filter_by(jcno=jcno).first()
