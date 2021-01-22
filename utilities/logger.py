from pathlib import Path
from datetime import datetime


class Logger:
    """"Simple error logger which right errors to log/error_log.csv"""
    log_path = Path.joinpath(Path(__file__).parent.absolute(),
                             Path('log'))
    # the first time the logger has been run
    first_run = True

    @staticmethod
    def write(info, file_name, newline=True):
        """" writes an error entry to the error log file"""

        if Logger.first_run:
            setup_directory_file(Logger.log_path, file_name)
            Logger.first_run = False

        log = open(str(Path(Logger.log_path, file_name)), 'a')

        if newline:
            info += '\n'

        log.write(info)
        log.close()


class LogError:
    """A base class for error logging objects"""
    error_code = None
    error_log_file = "error_log.csv"

    def __init__(self, actor: str, details: str, extra=None):
        """
        :param actor: describe the actor (user or device) which caused the
        error to be shown.
        :param details: provide details about the error
        :param extra: pass an instance of IExtra, this can be used to add
        additional information to the error log
        """
        self.actor = actor
        self.details = details
        self.date_time = get_date_time()
        if extra is None:
            self.extra = ExtraNothing().get_extra()
        elif isinstance(extra, IExtra):
            self.extra = extra.get_extra()

    def get_error(self):
        """get a string representation of the error"""
        return f'{self.error_code}, ' \
               f'{self.actor}, ' \
               f'{self.details}, ' \
               f'{self.date_time}, ' \
               f'{self.extra}'

    def log_it(self):
        """This method is used to write an error log to a file"""
        Logger.write(self.get_error(), self.error_log_file)


class ErrorAPISubmission(LogError):
    """Used for to create and log errors caused during the submission process
    to an API"""
    def __init__(self, actor, details, extra):
        super().__init__(actor, details, extra)
        self.error_code = "API_SUB_ERROR"


class ErrorDataVailidation(LogError):
    """Used for to create an log errors caused by failed data validation"""
    def __init__(self, actor, details, extra):
        super().__init__(actor, details, extra)
        self.error_code = "API_VAL_ERROR"


class ErrorDeviceVerfication(LogError):
    """Used for to create and log errors caused by failed device verification"""
    def __init__(self, actor, details, extra):
        self.error_code = "API_VER_ERROR"
        super().__init__(actor, details, extra)


class IExtra:
    """A base class for implementing a number of strategies regrading extra
    information"""

    extra_info = "NA"

    def format_extra(self):
        """format the extra data"""
        pass

    def get_extra(self):
        """
        get extra information in a specified format, the formatted text will
        likely not include any commas.
        :return: string
        """
        return str(self.format_extra())


class ExtraHtmlHeaders(IExtra):
    """Provides extra information concerning html headers"""
    def __init__(self, extra_info, headertype='Flask'):
        super().__init__()
        self.extra_info = extra_info
        self.headertype = headertype

    def format_extra(self):
        obj = self.extra_info
        extra_text = ""
        if self.headertype == 'Flask':
            extra_text = f'Access-Control-Request-Method:' \
                         f'{obj.get("Access-Control-Request-Method")} | ' \
                         f'Accept:{obj.get("Accept")} | ' \
                         f'Content-Length:{obj.get("Content-Length")} | ' \
                         f'Accept-Charset:{obj.get("Accept-Charset")} | ' \
                         f'User-Agent:{obj.get("User-Agent")}'

        return extra_text


class ExtraList(IExtra):
    """Provide extra information originating from a list"""
    def __init__(self, alist: list):
        self.extra_info = alist

    def format_extra(self):
        temp = ""
        for item in self.extra_info:
            temp += f'{item} | '
        return temp[:-3]


class ExtraNothing(IExtra):
    """"Provide not extra information"""
    def format_extra(self):
        return self.extra_info


def get_date_time():
    """return current iso date time"""
    return datetime.now().isoformat()[:21]


def setup_directory_file(log_path, file_name):
    """used to set up the default log file in relation to this script"""
    if not log_path.exists():
        log_path.mkdir()
        file = open(str(Path(Logger.log_path, file_name)), "w")
        file.write("ErrorCode, Actor, Details, DateTime, Other\n")
        file.close()
