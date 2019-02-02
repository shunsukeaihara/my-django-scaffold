import traceback
import logging
from datetime import datetime
import json
import pytz
import uuid


class JSONFormatter(logging.Formatter):
    """
    JSON formatter for python logging
    You can pass additional tags on a per message basis using the key "tags" in the extra parameter.
    eg: logger.error('hello world!', extra={"tags": ["hello=world"]})
    """

    def __init__(self, tags=None, hostname=None, fqdn=False, message_type='JSON', indent=None):
        """
        :param tags: a list of tags to add to every messages
        :hostname: force a specific hostname
        :fqdn: a boolean to use the FQDN instead of the machine's hostname
        :message_type: the message type for Logstash formatters
        :indent: indent level of the JSON output
        """
        self.indent = False

    def get_extra_fields(self, record):
        # The list contains all the attributes listed in
        # http://docs.python.org/library/logging.html#logrecord-attributes
        skip_list = [
            'asctime', 'created', 'exc_info', 'exc_text', 'filename', 'args',
            'funcName', 'id', 'levelname', 'levelno', 'lineno', 'module', 'msg',
            'msecs', 'msecs', 'message', 'name', 'pathname', 'process',
            'processName', 'relativeCreated', 'thread', 'threadName', 'extra']

        easy_types = (str, bool, dict, float, int, list, type(None))

        fields = {}

        if record.args:
            fields['msg'] = record.msg

        for key, value in record.__dict__.items():
            if key not in skip_list:
                if isinstance(value, easy_types):
                    fields[key] = value
                else:
                    fields[key] = repr(value)

        return fields

    def get_debug_fields(self, record):
        if record.exc_info:
            exc_info = self.format_exception(record.exc_info)
        else:
            exc_info = record.exc_text
        return {
            'exc_info': exc_info,
            'filename': record.filename,
            'lineno': record.lineno,
        }

    @classmethod
    def format_timestamp(cls, time):
        return datetime.fromtimestamp(time, tz=pytz.utc).isoformat()

    @classmethod
    def format_exception(cls, exc_info):
        return ''.join(traceback.format_exception(*exc_info)) if exc_info else ''

    @classmethod
    def serialize(cls, message, indent=None):
        return json.dumps(message)

    def format(self, record, serialize=True):
        # Create message dict
        timestamp = self.format_timestamp(record.created)
        message = {
            'timestamp': timestamp,
            'message': record.getMessage(),
            'level': record.levelname,
            'logger': record.name,
            'uuid': uuid.uuid4().hex,
        }

        # Add extra fields
        message.update(self.get_extra_fields(record))

        # If exception, add debug info
        if record.exc_info or record.exc_text:
            message.update(self.get_debug_fields(record))

        if serialize:
            return self.serialize(message, indent=self.indent)
        return message
