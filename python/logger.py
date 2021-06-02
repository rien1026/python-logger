import os
import logging
import datetime

class Logger():
    def __init__(self, prodMode):
        # create logs folder
        if os.path.isdir('logs') is False:
            os.mkdir('logs')

        # set prodMode param
        self.prodMode = prodMode

        # init logger
        self.logger = logging.getLogger()
        self.infoLogger = logging.getLogger('info')
        self.errLogger = logging.getLogger('error')

        # set info level to root logger
        self.logger.setLevel(logging.INFO)

        # init fomatter, timestr
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.timestr = datetime.datetime.now().strftime('%y%m%d')

        # add console handler
        self._addStreamHandler()

        # add file handler
        self._addFileHandler()

    def _addStreamHandler(self):
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(self.formatter)
        streamHandler.setLevel(logging.INFO if self.prodMode == 'dev' else logging.ERROR)
        self.infoLogger.addHandler(streamHandler)
        self.errLogger.addHandler(streamHandler)

    def _addFileHandler(self):
        infoFileHandler = logging.FileHandler('logs/info-%s.log' %self.timestr)
        errFileHandler = logging.FileHandler('logs/err-%s.log' %self.timestr)
        infoFileHandler.setFormatter(self.formatter)
        errFileHandler.setFormatter(self.formatter)
        self.infoLogger.addHandler(infoFileHandler)
        self.errLogger.addHandler(errFileHandler)

    def _checkTime(self):
        if self.timestr == datetime.datetime.now().strftime('%y%m%d'):
            return

        self.timestr = datetime.datetime.now().strftime('%y%m%d')
        self._addFileHandler()

    def info(self,message):
        self._checkTime()
        self.infoLogger.info(message)

    def err(self,message):
        self._checkTime()
        self.errLogger.error(message)


logger = Logger('dev')
