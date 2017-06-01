import logging


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value
        logging.debug("created token: {0}".format(self))

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=str(self.value)
        )

    def __repr__(self):
        return str(self)
