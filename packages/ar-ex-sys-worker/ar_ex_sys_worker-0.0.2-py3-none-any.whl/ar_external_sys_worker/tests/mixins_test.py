import unittest
import os
from wsqluse.wsqluse import Wsqluse
from ar_external_sys_worker import mixins


class TestCase(unittest.TestCase):
    sql_shell = Wsqluse(dbname=os.environ.get('DB_NAME'),
                        user=os.environ.get('DB_USER'),
                        password=os.environ.get('DB_PASS'),
                        host=os.environ.get('DB_HOST'))

    @unittest.SkipTest
    def testSignallAuthMe(self):
        login = '1@signal.com'
        password = 'd4GExhec'
        inst = mixins.SignAllAuthMe(login=login,
                                    password=password)
        response = inst.auth_me()
        self.assertTrue(response.status_code == 200)
        token = inst.get_token()
        print(token)

    def test_ActsGetter(self):
        inst = mixins.ActsSQLCommands()
        inst.table_id = 1
        response = self.sql_shell.try_execute_get(inst.get_unsend_command())
        print(response)



if __name__ == "__main__":
    unittest.main()
