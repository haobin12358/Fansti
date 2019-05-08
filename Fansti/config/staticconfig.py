# *- coding:utf8 *-


AIRLINE_DB_TO_EXCEL = {
    "airline": "AIRLINE",
    "airname": "NAME",
    "aircompany": "COMPANY",
    "flight": "FLIGHT",
    "depa": "DEPA",
    "dest": "DEST",
    "mydate": "DATE",
    "etd": "ETD",
    "eta": "ETA",
    "supporttime": "交单时间",
    "aircraft": "AIRCRAFT",
    "remark": "REMARK"
}



AIRLINE_EXCEL_ROLE = {
    "airline": r"^[A-Z0-9-/]+$",
    "airname": r"^[\u4e00-\u9fa5]+$",
    "aircompany": r"^[a-zA-Z]*[\u4e00-\u9fa5]*$",
    "flight": r"^[A-Z0-9/]+$",
    "depa": r"^[A-Z]+$",
    "supporttime": "",
    "aircraft": r"^[A-Z0-9]{3,4}[/-]{0,1}[A-Z0-9/]*$",
    "remark": ""
}


DGR_DB_TO_EXCEL = {
    "unno": "UN号",
    "unname": "运输专用名称",
    "untype": "类别",
    }


DGR_LEVEL_DB_TO_EXCEL = {
    "dgr_level": "等级",
    "airliner_capacity": "客机容量",
    "airliner_description_no": "客机说明号",
    "airliner_is_single": "客机是否可单一",
    "airfreighter_capacity": "货机容量",
    "airfreighter_description_no": "货机说明号",
    "airfreighter_is_single": "货机是否可单一",
    "message": "备注",
    # "dgr_container": "容器类型",
    # "dgr_container_capacity": "容量",
    # "dgr_type": "客机/货机",
}

DGR_KEY = ["UN号", "运输专用名称", "类别"]

DGR_LEVEL_KEY = ["等级", "客机容量", "客机说明号", "客机是否可单一", "货机容量", "货机说明号", "货机是否可单一", "备注"]

CONTAINER_KEY = ['客机容器类型', '客机容器类型对应容量', '货机容器类型', '货机容器类型对应容量']

TACT_DB_TO_EXCEL = {
    "three_code": "三字码",
    "city": "城市名",
    "state": "州名",
    "country": "国家",
    "freight": "运费",
    "chinese_position": "中文名称及地理位置",
}

TACT_KEYS = ["城市名", "三字码", "州名", "中文名称及地理位置", "国家", "运费"]

ENQUIRY_DB_TO_EXCEL = {
    "departure": "起运地",
    "destination": "目的地",
    "company": "航空公司",
    "pwkh": "普危客货",
    "usetime": "有效期",
    "weight_m": "M",
    "weight_m_custom": "M客户",
    "weight_n": "N",
    "weight_n_custom": "N客户",
    "weight_q45": "Q45",
    "weight_q45_custom": "Q45客户",
    "weight_q100": "Q100",
    "weight_q100_custom": "Q100客户",
    "weight_q300": "Q300",
    "weight_q300_custom": "Q300客户",
    "weight_q500": "Q500",
    "weight_q500_custom": "Q500客户",
    "weight_q1000": "Q1000",
    "weight_q1000_custom": "Q1000客户",
    "gtyt": "固体/液体",
    "fuel": "燃油费用",
    "fuel_min": "燃油费用MIN",
    "safe": "安全费用",
    "safe_min": "安全费用MIN",
    "awb": "AWB",
    "attach": "附加费用",
    "attach_min": "附加费用MIN",
    "remarks": "备注"
}

ENQUIRY_KEYS = ["起运地","目的地","航空公司","普危客货","有效期","M","M客户","N","N客户","Q45",
                "Q45客户","Q100","Q100客户","Q300","Q300客户","Q500","Q500客户","Q1000","Q1000客户",
                "固体/液体","燃油费用","燃油费用MIN","安全费用","安全费用MIN","AWB","附加费用","附加费用MIN","备注"]

SELECT_TYPE = {
    "CAS": "cas",
    "DGR": "dgr",
    "鉴定报告": "jd",
    "TACT": "tact",
    "HS code": "HScode",
    "航班时刻": "flyno",
}