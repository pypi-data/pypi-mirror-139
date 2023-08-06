import requests
import json
import base64
import datetime


class UrlsWorkerMixin:
    """ Миксина для работы с юрлами """
    link_host = None
    port = None

    def get_full_endpoint(self, link):
        print(self.link_host, self.port, link)
        return "".join((self.link_host, ':' + self.port, link))


class ExSys(UrlsWorkerMixin):
    link_host = None
    link_auth = None
    port = None
    link_create_act = None
    ex_sys_id = None



class SignallMixin(ExSys):
    link_host = "http://83.136.233.111"
    link_auth = '/v1/user/login'
    port = "8080"
    link_create_act = '/v1/acts/create_act'
    ex_sys_id = 1


class AuthMe(UrlsWorkerMixin):
    link_host = None
    link_auth = None
    headers = None

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def set_headers(self, headers):
        self.headers = headers
        return self.headers

    def auth_me(self):
        auth_data = self.get_auth_data()
        auth_data_json = json.dumps(auth_data)
        endpoint = self.get_full_endpoint(self.link_auth)
        response = requests.post(endpoint, data=auth_data_json)
        return response

    def get_auth_data(self):
        data = {'login': self.login,
                'password': self.password}
        return data

    def extract_token(self, auth_result):
        return auth_result

    def get_token(self):
        response = self.auth_me()
        token = self.extract_token(response)
        return token


class SignAllAuthMe(AuthMe):

    def extract_token(self, auth_result_json):
        token = auth_result_json.json()['token']
        self.set_headers({'Authorization': token})
        return token

    def get_auth_data(self):
        data = {'email': self.login,
                'password': self.password}
        return data


class ActToJSONMixin:
    link_host = None
    link_create_act = None

    def get_json(self, car_number: str, ex_id: int, gross: int, tare: int,
                 cargo: int, time_in: str, time_out: str, alerts: list,
                 carrier: str, trash_cat: str, trash_type: str,
                 operator_comments: dict, photo_in: str,
                 photo_out: str):
        data = locals()
        data.__delitem__('self')
        json_data = json.dumps(data)
        return json_data


class ActSenderMixin:
    def send_act(self, link, act_json, headers):
        print(locals())
        response = requests.post(url=link, data=act_json, headers=headers)
        return response


class PhotoEncoderMixin:
    def get_photo_data(self, photo_path):
        """ Извлечь из фото последовательность байтов в кодировке base-64 """
        try:
            with open(photo_path, 'rb') as fobj:
                photo_data = base64.b64encode(fobj.read())
                return photo_data
        except FileNotFoundError:
            pass


class SignallPhotoEncoderMixin(PhotoEncoderMixin):
    def get_photo_data(self, photo_path):
        photo = super().get_photo_data(photo_path)
        data = photo.decode()
        return data


class DataBaseWorker:
    sql_shell = None

    def set_sqlshell(self, sql_shell):
        self.sql_shell = sql_shell


class ActsTableInfo:
    table_name = 'records'
    table_id = 1


class LoggerSQLCommands(ExSys, ActsTableInfo):
    log_id = None

    def get_log_ex_sys_sent(self, record_id: int, sent_time=None):
        if not sent_time:
            sent_time = datetime.datetime.now()
        command = "INSERT INTO ex_sys_data_send_reports (ex_sys_id, " \
                  "local_id, sent, table_id) VALUES " \
                  "({}, {}, '{}', " \
                  "(SELECT id FROM ex_sys_tables WHERE name='{}'))".format(self.ex_sys_id,
                                                                           record_id, sent_time,
                                                                           self.table_name)

        return command

    def get_log_ex_sys_get(self, ex_system_data_id,
                       log_id=None, get_time=None):
        if not get_time:
            get_time = datetime.datetime.now()
        if not log_id:
            log_id = self.log_id
        command = "UPDATE ex_sys_data_send_reports SET get='{}', " \
                  "ex_sys_data_id='{}' " \
                  "WHERE id={}".format(get_time, ex_system_data_id, log_id)
        return command


class ActsSQLCommands:

    def get_acts_all_command(self):
        command = "SELECT r.id as ex_id, r.car_number, r.brutto as gross, " \
                  "r.tara as tare, r.cargo, r.time_in, r.time_out, r.alerts, " \
                  "clients.inn as carrier, tc.cat_name as trash_cat, " \
                  "tt.name as trash_type, oc.gross as gross_comm," \
                  "oc.tare as tare_comm, oc.additional as add_comm, " \
                  "oc.changing as changing_comm, oc.closing as closing_comm " \
                  "FROM records r " \
                  "INNER JOIN clients ON (r.carrier=clients.id) " \
                  "INNER JOIN trash_cats tc ON (r.trash_cat=tc.id) " \
                  "INNER JOIN trash_types tt ON (r.trash_type=tt.id) " \
                  "LEFT JOIN operator_comments oc ON (r.id=oc.record_id)"
        return command

    def get_acts_today_command(self):
        today = datetime.datetime.today()
        return self.get_acts_all_command() + " WHERE time_in::date='{}'".format(today)

    def get_unsend_command(self):
        return self.get_acts_all_command() + \
               "  WHERE r.id NOT IN (SELECT local_id FROM " \
               "ex_sys_data_send_reports WHERE table_id={} and not get is null) " \
               "and tc.cat_name='ТКО' LIMIT 10 ".format(self.table_id)

class DataWorker:
    def get_ex_sys_id(self, response):
        return response['id']


class SignAllActDataWorker(DataWorker):
    table_name = 'records'

    def get_ex_sys_id(self, response):
        response = response.json()
        print(response)
        return response['act_id']
