from utilities.logger import *


def read_last_line():
    file = open(Path(Logger.log_path, LogError.error_log_file), "r")
    lastline = file.readlines()[-1]
    lastline = lastline.strip()
    file.close()
    return lastline

def test_submission_error_flask():
    """" Ensures that that correct format """
    flaskheader = {
        "Access-Control-Request-Method": "POST",
        "Accept": "application/json",
        "Content-Length": "2000",
        "Accept-Charset": "utf-8",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0"
    }

    ErrorAPISubmission("D23478", "Verify failure", ExtraHtmlHeaders(flaskheader)).log_it()
    time = get_date_time()
    assert read_last_line() == \
           f'API_SUB_ERROR, D23478, Verify failure, {time}, Access-Control-Request-Method:POST | Accept:application/json | Content-Length:2000 | Accept-Charset:utf-8 | User-Agent:Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'

def test_verification_error():
    device = "D47848"
    details = "NA"
    ErrorDeviceVerfication(device, details, None).log_it()
    time = get_date_time()
    assert read_last_line() == f'API_VER_ERROR, D47848, NA, {time}, NA'


def test_validation_error():
    ErrorDataVailidation("D47848", "error message", None).log_it()
    time = get_date_time()
    assert read_last_line() == f'API_VAL_ERROR, D47848, error message, {time}, NA'