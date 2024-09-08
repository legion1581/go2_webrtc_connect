from enum import Enum

DATA_CHANNEL_TYPE = {
    "VALIDATION": "validation",
    "SUBSCRIBE": "subscribe",
    "UNSUBSCRIBE": "unsubscribe",
    "MSG": "msg",
    "REQUEST": "request",
    "RESPONSE": "response",
    "VID": "vid",
    "AUD": "aud",
    "ERR": "err",
    "HEARTBEAT": "heartbeat",
    "RTC_INNER_REQ": "rtc_inner_req",
    "RTC_REPORT": "rtc_report",
    "ADD_ERROR": "add_error",
    "RM_ERROR": "rm_error",
    "ERRORS": "errors",
}

class WebRTCConnectionMethod(Enum):
    LocalAP = 1
    LocalSTA = 2
    Remote = 3

app_error_messages = {
    "app_error_code_100_1": "DDS message timeout",
    "app_error_code_100_10": "Battery communication error",
    "app_error_code_100_2": "Distribution switch abnormal",
    "app_error_code_100_20": "Abnormal mote control communication",
    "app_error_code_100_40": "MCU communication error",
    "app_error_code_100_80": "Motor communication error",
    "app_error_code_200_1": "Rear left fan jammed",
    "app_error_code_200_2": "Rear right fan jammed",
    "app_error_code_200_4": "Front fan jammed",
    "app_error_code_300_1": "Overcurrent",
    "app_error_code_300_10": "Winding overheating",
    "app_error_code_300_100": "Motor communication interruption",
    "app_error_code_300_2": "Overvoltage",
    "app_error_code_300_20": "Encoder abnormal",
    "app_error_code_300_4": "Driver overheating",
    "app_error_code_300_8": "Generatrix undervoltage",
    "app_error_code_400_1": "Motor rotate speed abnormal",
    "app_error_code_400_10": "Abnormal dirt index",
    "app_error_code_400_2": "PointCloud data abnormal",
    "app_error_code_400_4": "Serial port data abnormal",
    "app_error_code_500_1": "UWB serial port open abnormal",
    "app_error_code_500_2": "Robot dog information retrieval abnormal",
    "app_error_code_600_4": "Overheating software protection",
    "app_error_code_600_8": "Low battery software protection",
    "app_error_source_100": "Communication firmware malfunction",
    "app_error_source_200": "Communication firmware malfunction",
    "app_error_source_300": "Motor malfunction",
    "app_error_source_400": "Radar malfunction",
    "app_error_source_500": "UWB malfunction",
    "app_error_source_600": "Motion Control",
    "app_error_wheel_300_100": "Motor Communication Interruption",
    "app_error_wheel_300_40": "Calibration Data Abnormality",
    "app_error_wheel_300_80": "Abnormal Reset"
}
