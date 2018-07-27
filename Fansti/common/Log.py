from Fansti.config.response import PARAMS_MISS, PARAMS_REDUNDANCE

def make_log(log_name, log_meassage):
    log_cut = "=========={0}=========="
    print(log_cut.format(log_name))
    print(log_meassage)
    print(log_cut.format(log_name))

def judge_keys(true_keys, data_keys, null_keys=None):
    for key in true_keys:
        if key not in data_keys:
            return PARAMS_MISS

    for key in data_keys:
        if key not in true_keys and null_keys and key not in null_keys:
            return PARAMS_REDUNDANCE

    return 200