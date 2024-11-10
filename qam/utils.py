def calc_case_status(passed, failed, blocked, remarks, all_items):
    if blocked:
        return ('BLOCKED', '#fff200')
    elif remarks:
        return ('PASSED WITH REMARKS', '#00a65d')
    elif len(passed) == len(all_items):
        return ('PASSED', '#009353')
    elif len(failed) == len(all_items):
        return ('FAILED', '#ce181e')
    elif len(passed) / len(all_items) > 0.6:
        return ('PASSED', '#65c295')
    elif len(passed) / len(all_items) > 0.4:
        return ('FAILED', '#00b6bd')
    else:
        return ('FAILED', '#f37b70')