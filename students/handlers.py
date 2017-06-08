import logging
from django.utils import timezone


class DbLogHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        # instantiate the model
        try:
            from students.models.log_entry import LogEntry
            log_entry = LogEntry(error_level=record.levelname, date=timezone.now(), error_message=record.message)

            log_entry.save()
        except:
            pass

        return
