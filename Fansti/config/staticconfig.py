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
    "aircompany": r"^[\u4e00-\u9fa5]+$",
    "flight": r"^[A-Z0-9]+$",
    "depa": r"^[A-Z]+$",
    "dest": r"^[A-Z/-]+$",
    "mydate": r"^[\d]{4}-[\d]{1,2}-[\d]{1,2}$",
    "etd": r"^[\d]{1,2}:[\d]{1,2}$",
    "eta": r"^[\d]{1,2}:[\d]{1,2}[+\d]*$",
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

SELECT_TYPE = {
    "CAS": "cas",
    "DGR": "dgr",
    "鉴定报告": "jd",
    "TACT": "tact",
    "HS code": "HScode",
    "航班时刻": "flyno",
}