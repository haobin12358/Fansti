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
    "airname": ur"^[\u4e00-\u9fa5]+$",
    "aircompany": ur"^[\u4e00-\u9fa5]+$",
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
