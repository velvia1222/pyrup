import logging


class AbstractView(object):
    def __init__(self, request):
        self.request = request
        self.logger = logging.getLogger(
            self.__module__ + '.' + self.__class__.__name__)

    def __call__(self):
        self.logger.info('begin')
        result = self.execute()
        self.request.dbsession.flush()
        self.logger.info('end')
        return result
