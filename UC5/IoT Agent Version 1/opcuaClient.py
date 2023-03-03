from opcua import Client
import logging


class OpcuaClient(object):
    def __init__(self, obj):
        self.client = Client(obj.url)
        if "certificate" in obj.json_data_raw:
            logging.basicConfig(level=logging.WARN)
            self.client.application_uri = obj.server_uri
            self.client.set_user(obj.server_username)
            self.client.set_password(obj.server_password)
            self.certificate_detail = (
                obj.server_security_policy
                + ","
                + obj.server_security_mode
                + ","
                + obj.server_certificate_path
                + ","
                + obj.server_key_path
            )
            self.client.set_security_string(self.certificate_detail)
            self.client.secure_channel_timeout = 10000
            self.client.session_timeout = 10000

