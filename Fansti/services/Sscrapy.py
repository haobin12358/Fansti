# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from Fansti.models.model import AIR_HWYS_JD, AIR_HWYS_LINES, SELECT_INFO, AIR_HWYS_DGR, AIR_HWYS_DGR_LEVEL, \
    AIR_HWYS_DGR_CONTAINER, AIR_HWYS_TACT, AIR_HWYS_ENQUIRY, D_ACCOUNTS, D_PORT
from Fansti.services.SBase import SBase, close_session
from sqlalchemy import or_

class Sscrapy(SBase):

    @close_session
    def get_jd_by_name(self, name):
        return self.session.query(AIR_HWYS_JD.chinesename, AIR_HWYS_JD.englishname, AIR_HWYS_JD.unno,
                                  AIR_HWYS_JD.appearance, AIR_HWYS_JD.appearance2, AIR_HWYS_JD.principal,
                                  AIR_HWYS_JD.identificationunits, AIR_HWYS_JD.endtime)\
            .filter(AIR_HWYS_JD.chinesename.like('%{0}%'.format(name))).first()

    @close_session
    def get_chinessname_by_englishname(self, englishname):
        return self.session.query(AIR_HWYS_JD.chinesename).filter_by(englishname=englishname).first()

    @close_session
    def get_all_by_depa_dest(self, depa=None, dest=None):
        return self.session.query(AIR_HWYS_LINES.depa, AIR_HWYS_LINES.dest, AIR_HWYS_LINES.flight, AIR_HWYS_LINES.mydate,
                                  AIR_HWYS_LINES.aircraft, AIR_HWYS_LINES.etd, AIR_HWYS_LINES.eta)\
            .filter_by(depa=depa).filter_by(dest=dest).all()

    @close_session
    def get_all_select(self, page_num, page_size, select_name):
        return self.session.query(
            SELECT_INFO.login_name, SELECT_INFO.openid, SELECT_INFO.select_name,
            SELECT_INFO.create_time, SELECT_INFO.select_value).filter_by(
            select_name=select_name).order_by(SELECT_INFO.create_time.desc()).offset(
            page_size * (page_num - 1)).limit(page_size).all()

    @close_session
    def get_dgr_by_unno_unname(self, unno, unname):
        return self.session.query(AIR_HWYS_DGR.id, AIR_HWYS_DGR.unno, AIR_HWYS_DGR.unname, AIR_HWYS_DGR.untype)\
            .filter(AIR_HWYS_DGR.unno==unno, AIR_HWYS_DGR.unname==unname).first()

    @close_session
    def get_dgr_by_unno2(self, unno):
        return self.session.query(AIR_HWYS_DGR.id, AIR_HWYS_DGR.unno, AIR_HWYS_DGR.unname, AIR_HWYS_DGR.untype) \
            .filter(AIR_HWYS_DGR.unno == unno).all()

    @close_session
    def get_dgr_level_by_dgrid(self, dgr_id):
        return self.session.query(AIR_HWYS_DGR_LEVEL.id, AIR_HWYS_DGR_LEVEL.airfreighter_capacity,
                                  AIR_HWYS_DGR_LEVEL.airfreighter_description_no,
                                  AIR_HWYS_DGR_LEVEL.airfreighter_is_single, AIR_HWYS_DGR_LEVEL.airliner_capacity,
                                  AIR_HWYS_DGR_LEVEL.airliner_description_no, AIR_HWYS_DGR_LEVEL.airliner_is_single,
                                  AIR_HWYS_DGR_LEVEL.message, AIR_HWYS_DGR_LEVEL.dgr_level)\
            .filter_by(dgr_id=dgr_id).all()

    @close_session
    def get_dgr_container_by_levelid(self, dgr_level_id):
        return self.session.query(AIR_HWYS_DGR_CONTAINER.dgr_container, AIR_HWYS_DGR_CONTAINER.dgr_container_capacity,
                                  AIR_HWYS_DGR_CONTAINER.dgr_type)\
            .filter_by(dgr_level_id=dgr_level_id).all()

    @close_session
    def get_airline_by_flight(self, airflight):
        return self.session.query(
            AIR_HWYS_LINES.id, AIR_HWYS_LINES.airline, AIR_HWYS_LINES.aircompany, AIR_HWYS_LINES.airname,
            AIR_HWYS_LINES.flight, AIR_HWYS_LINES.depa, AIR_HWYS_LINES.dest, AIR_HWYS_LINES.mydate, AIR_HWYS_LINES.etd,
            AIR_HWYS_LINES.eta, AIR_HWYS_LINES.supporttime, AIR_HWYS_LINES.aircraft, AIR_HWYS_LINES.remark
        ).filter(AIR_HWYS_LINES.flight == airflight).first()

    @close_session
    def update_airline(self, airflight, airlines):
        return self.session.query(AIR_HWYS_LINES).filter(AIR_HWYS_LINES.flight == airflight).update(airlines)

    @close_session
    def get_tact_by_three_code(self, three_code):
        return self.session.query(AIR_HWYS_TACT.three_code, AIR_HWYS_TACT.city, AIR_HWYS_TACT.state, AIR_HWYS_TACT.id,
                                  AIR_HWYS_TACT.country, AIR_HWYS_TACT.freight, AIR_HWYS_TACT.chinese_position)\
            .filter_by(three_code=three_code).first()

    @close_session
    def get_id_by_time(self, date, name, openid):
        return self.session.query(SELECT_INFO.id).filter_by(create_time=date).filter_by(select_name=name).filter_by(openid=openid).all()

    @close_session
    def update_dgr(self, dgrid, dgr):
        # 删除关联表内容
        dgrlevelid_list = self.session.query(AIR_HWYS_DGR_LEVEL.id).filter(AIR_HWYS_DGR_LEVEL.dgr_id == dgrid).all()
        self.session.query(AIR_HWYS_DGR_LEVEL).filter(AIR_HWYS_DGR_LEVEL.dgr_id == dgrid).delete()

        for dgrlevel in dgrlevelid_list:
            self.session.query(AIR_HWYS_DGR_CONTAINER).filter(AIR_HWYS_DGR_CONTAINER.dgr_level_id == dgrlevel.id).delete()
        # 更新
        return self.session.query(AIR_HWYS_DGR).filter(AIR_HWYS_DGR.id == dgrid).update(dgr)

    @close_session
    def get_tact_by_three_code(self, threecode):
        return self.session.query(
            AIR_HWYS_TACT.id, AIR_HWYS_TACT.three_code, AIR_HWYS_TACT.city, AIR_HWYS_TACT.state,
            AIR_HWYS_TACT.country, AIR_HWYS_TACT.freight, AIR_HWYS_TACT.chinese_position)\
            .filter(AIR_HWYS_TACT.three_code == threecode).first()

    @close_session
    def update_tact(self, tactid, tact):
        return self.session.query(AIR_HWYS_TACT).filter(AIR_HWYS_TACT.id == tactid).update(tact)

    @close_session
    def update_enquiry(self, tactid, tact):
        return self.session.query(AIR_HWYS_ENQUIRY).filter(AIR_HWYS_ENQUIRY.id == tactid).update(tact)

    @close_session
    def get_jds_by_name(self, name):
        return self.session.query(AIR_HWYS_JD.chinesename, AIR_HWYS_JD.englishname, AIR_HWYS_JD.unno,
                                  AIR_HWYS_JD.appearance, AIR_HWYS_JD.appearance2)\
            .filter(AIR_HWYS_JD.chinesename.like('%{0}%'.format(name))).offset(0).limit(20).all()

    @close_session
    def get_all_select_count(self, name):
        from sqlalchemy import func
        return self.session.query(func.count(SELECT_INFO.id)).filter(SELECT_INFO.select_name == name).scalar()

    @close_session
    def get_id_by_dep_des_com_pwkh(self, departure, destination, company, pwkh):
        return self.session.query(AIR_HWYS_ENQUIRY.id)\
            .filter_by(departure=departure).filter_by(destination=destination)\
            .filter_by(company=company).filter_by(pwkh=pwkh)\
            .first()

    @close_session
    def get_des(self, select_name):
        return self.session.query(D_PORT.port_aircode).filter(or_(D_PORT.port_aircode.like("%{0}%".format(select_name)),
                                                                  D_PORT.port_cname.like("%{0}%".format(select_name))))\
            .filter(not D_PORT.port_aircode).all()

    @close_session
    def get_accounts(self, select_name):
        return self.session.query(D_ACCOUNTS.accounts_code)\
            .filter(or_(D_ACCOUNTS.accounts_code.like("%{0}%".format(select_name)),
                        D_ACCOUNTS.accounts_name.like("%{0}%".format(select_name))))\
            .filter(D_ACCOUNTS.b_airway == "1").all()

    @close_session
    def get_mn_price(self, des, dep, accounts, pwkh, gtyt):
        price = self.session.query(AIR_HWYS_ENQUIRY.weight_m, AIR_HWYS_ENQUIRY.weight_m_custom,
                                   AIR_HWYS_ENQUIRY.weight_n, AIR_HWYS_ENQUIRY.weight_n_custom, AIR_HWYS_ENQUIRY.fuel,
                                   AIR_HWYS_ENQUIRY.fuel_min, AIR_HWYS_ENQUIRY.safe, AIR_HWYS_ENQUIRY.safe_min,
                                   AIR_HWYS_ENQUIRY.awb, AIR_HWYS_ENQUIRY.attach, AIR_HWYS_ENQUIRY.attach_min)\
            .filter(AIR_HWYS_ENQUIRY.destination == des, AIR_HWYS_ENQUIRY.departure == dep,
                    AIR_HWYS_ENQUIRY.pwkh == pwkh, AIR_HWYS_ENQUIRY.gtyt == gtyt)
        if accounts:
            price = price.filter(AIR_HWYS_ENQUIRY.company == accounts)
        return price.all()

    @close_session
    def get_q45_price(self, des, dep, accounts, pwkh, gtyt):
        price = self.session.query(AIR_HWYS_ENQUIRY.weight_q45, AIR_HWYS_ENQUIRY.weight_q45_custom, AIR_HWYS_ENQUIRY.fuel,
                                   AIR_HWYS_ENQUIRY.fuel_min, AIR_HWYS_ENQUIRY.safe, AIR_HWYS_ENQUIRY.safe_min,
                                   AIR_HWYS_ENQUIRY.awb, AIR_HWYS_ENQUIRY.attach, AIR_HWYS_ENQUIRY.attach_min) \
            .filter(AIR_HWYS_ENQUIRY.destination == des, AIR_HWYS_ENQUIRY.departure == dep,
                    AIR_HWYS_ENQUIRY.pwkh == pwkh, AIR_HWYS_ENQUIRY.gtyt == gtyt)
        if accounts:
            price = price.filter(AIR_HWYS_ENQUIRY.company == accounts)
        return price.all()

    @close_session
    def get_q100_price(self, des, dep, accounts, pwkh, gtyt):
        price = self.session.query(AIR_HWYS_ENQUIRY.weight_q100, AIR_HWYS_ENQUIRY.weight_q100_custom,
                                   AIR_HWYS_ENQUIRY.fuel,
                                   AIR_HWYS_ENQUIRY.fuel_min, AIR_HWYS_ENQUIRY.safe, AIR_HWYS_ENQUIRY.safe_min,
                                   AIR_HWYS_ENQUIRY.awb, AIR_HWYS_ENQUIRY.attach, AIR_HWYS_ENQUIRY.attach_min) \
            .filter(AIR_HWYS_ENQUIRY.destination == des, AIR_HWYS_ENQUIRY.departure == dep,
                    AIR_HWYS_ENQUIRY.pwkh == pwkh, AIR_HWYS_ENQUIRY.gtyt == gtyt)
        if accounts:
            price = price.filter(AIR_HWYS_ENQUIRY.company == accounts)
        return price.all()

    @close_session
    def get_q300_price(self, des, dep, accounts, pwkh, gtyt):
        price = self.session.query(AIR_HWYS_ENQUIRY.weight_q300, AIR_HWYS_ENQUIRY.weight_q300_custom,
                                   AIR_HWYS_ENQUIRY.fuel,
                                   AIR_HWYS_ENQUIRY.fuel_min, AIR_HWYS_ENQUIRY.safe, AIR_HWYS_ENQUIRY.safe_min,
                                   AIR_HWYS_ENQUIRY.awb, AIR_HWYS_ENQUIRY.attach, AIR_HWYS_ENQUIRY.attach_min) \
            .filter(AIR_HWYS_ENQUIRY.destination == des, AIR_HWYS_ENQUIRY.departure == dep,
                    AIR_HWYS_ENQUIRY.pwkh == pwkh, AIR_HWYS_ENQUIRY.gtyt == gtyt)
        if accounts:
            price = price.filter(AIR_HWYS_ENQUIRY.company == accounts)
        return price.all()

    @close_session
    def get_q500_price(self, des, dep, accounts, pwkh, gtyt):
        price = self.session.query(AIR_HWYS_ENQUIRY.weight_q500, AIR_HWYS_ENQUIRY.weight_q500_custom,
                                   AIR_HWYS_ENQUIRY.fuel,
                                   AIR_HWYS_ENQUIRY.fuel_min, AIR_HWYS_ENQUIRY.safe, AIR_HWYS_ENQUIRY.safe_min,
                                   AIR_HWYS_ENQUIRY.awb, AIR_HWYS_ENQUIRY.attach, AIR_HWYS_ENQUIRY.attach_min) \
            .filter(AIR_HWYS_ENQUIRY.destination == des, AIR_HWYS_ENQUIRY.departure == dep,
                    AIR_HWYS_ENQUIRY.pwkh == pwkh, AIR_HWYS_ENQUIRY.gtyt == gtyt)
        if accounts:
            price = price.filter(AIR_HWYS_ENQUIRY.company == accounts)
        return price.all()

    @close_session
    def get_q1000_price(self, des, dep, accounts, pwkh, gtyt):
        price = self.session.query(AIR_HWYS_ENQUIRY.weight_q1000, AIR_HWYS_ENQUIRY.weight_q1000_custom,
                                   AIR_HWYS_ENQUIRY.fuel,
                                   AIR_HWYS_ENQUIRY.fuel_min, AIR_HWYS_ENQUIRY.safe, AIR_HWYS_ENQUIRY.safe_min,
                                   AIR_HWYS_ENQUIRY.awb, AIR_HWYS_ENQUIRY.attach, AIR_HWYS_ENQUIRY.attach_min) \
            .filter(AIR_HWYS_ENQUIRY.destination == des, AIR_HWYS_ENQUIRY.departure == dep,
                    AIR_HWYS_ENQUIRY.pwkh == pwkh, AIR_HWYS_ENQUIRY.gtyt == gtyt)
        if accounts:
            price = price.filter(AIR_HWYS_ENQUIRY.company == accounts)
        return price.all()