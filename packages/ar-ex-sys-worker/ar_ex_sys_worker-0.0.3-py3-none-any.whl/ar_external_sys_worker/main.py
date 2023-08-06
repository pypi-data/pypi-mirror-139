import datetime

from ar_external_sys_worker import mixins


class SignallActWorker(mixins.SignallMixin, mixins.SignAllAuthMe,
                       mixins.SignAllActDataWorker,
                       mixins.ActToJSONMixin, mixins.ActSenderMixin,
                       mixins.SignallPhotoEncoderMixin, mixins.ActsSQLCommands,
                       mixins.LoggerSQLCommands):
    def __init__(self, sql_shell, login, password):

        self.sql_shell = sql_shell
        super().__init__(login=login, password=password)

    def send_today_acts(self):
        today_acts = self.sql_shell(self.get_acts_today_command())
        for act in today_acts:
            self.send_and_log_act(**act)

    def send_unsend_acts(self):
        for act in self.sql_shell.get_table_dict(self.get_unsend_command())['info']:
            print(act)
            if act['alerts']:
                act['alerts'] = act.pop('alerts').split('|')
            act['operator_comments'] = {'gross_comm': act.pop('gross_comm'),
                                        'tare_comm': act.pop('tare_comm'),
                                        'add_comm': act.pop('add_comm'),
                                        'changing_comm': act.pop('changing_comm'),
                                        'closing_comm': act.pop('closing_comm')}
            act['time_in'] = act['time_in'].strftime('%Y-%m-%d %H:%M:%S')
            act['time_out'] = act['time_out'].strftime('%Y-%m-%d %H:%M:%S')
            act['photo_in'] = self.get_photo_data(
                self.get_photo_path(act['ex_id'], 1))
            act['photo_out'] = self.get_photo_data(
                self.get_photo_path(act['ex_id'], 2))
            self.send_and_log_act(**act)

    def get_photo_path(self, record_id, photo_type):
        command = "SELECT p.path FROM photos p " \
                  "INNER JOIN record_photos rp ON (p.photo_type = rp.id) " \
                  "WHERE p.photo_type={} and rp.record_id={} LIMIT 1".format(photo_type,
                                                           record_id)
        response = self.sql_shell.try_execute_get(command)
        return response[0][0]

    def send_and_log_act(self, car_number: str, ex_id: int, gross: int,
                         tare: int, cargo: int, time_in: str, time_out: str,
                         alerts: list, carrier: str, trash_cat: str,
                         trash_type: str, operator_comments: dict,
                         photo_in: str = None, photo_out: str = None) -> object:
        token = self.get_token()
        if photo_in:
            photo_in = self.get_photo_data(photo_in)
        if photo_out:
            photo_out = self.get_photo_data(photo_out)
        act_json = self.get_json(car_number=car_number, ex_id=ex_id,
                                 gross=gross, tare=tare, cargo=cargo,
                                 time_in=time_in, time_out=time_out,
                                 alerts=alerts, carrier=carrier,
                                 trash_cat=trash_cat,
                                 trash_type=trash_type,
                                 operator_comments=operator_comments,
                                 photo_in=photo_in, photo_out=photo_out)
        headers = {'Authorization': token}
        link = self.get_full_endpoint(self.link_create_act)
        log_id = self.sql_shell.try_execute(
            self.get_log_ex_sys_sent(ex_id))['info'][0][0]
        act_send_response = self.send_act(link, act_json, headers)
        ex_sys_data_id = self.get_ex_sys_id(act_send_response)
        self.sql_shell.try_execute(
            self.get_log_ex_sys_get(ex_sys_data_id, log_id))
        return act_send_response.json()