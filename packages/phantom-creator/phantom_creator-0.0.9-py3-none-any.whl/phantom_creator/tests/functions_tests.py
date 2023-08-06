import datetime
import os
import unittest
from phantom_creator import functions
from phantom_creator import main
from wsqluse.wsqluse import Wsqluse


class TestCase(unittest.TestCase):
    sqlshell = Wsqluse(dbname=os.environ.get('DBNAME'),
                       user=os.environ.get('DBUSER'),
                       password=os.environ.get('DBPASS'),
                       host=os.environ.get('DBHOST'))

    def test_get_last_phantoms(self):
        response = functions.check_last_phantoms(self.sqlshell, 'Н266ХО102')
        self.assertTrue(isinstance(response, int))
        response = functions.check_last_phantoms(self.sqlshell, 'В060ХА702')
        self.assertTrue(isinstance(response, int))

    def test_get_time_out_rand(self):
        response = functions.get_rand_minutes(10, 16)
        self.assertTrue(response in range(10, 16))

    @unittest.SkipTest
    def test_main_worker(self):
        main.work(self.sqlshell, work_start_time=datetime.timedelta(hours=8),
                  work_end_time=datetime.timedelta(hours=20), phantoms_need=15)

    def test_check_last_record_time_in(self):
        time_in = datetime.datetime.now()
        time_out = time_in + datetime.timedelta(minutes=15)
        functions.create_phantom(self.sqlshell, time_in=time_in,
                                 time_out=time_out)
        result = functions.check_last_record_time_in(self.sqlshell)
        self.assertEqual(result, 1)
        functions.delete_phantoms(sql_shell=self.sqlshell)

    def test_check_last_record_time_out(self):
        time_in = datetime.datetime.now() - datetime.timedelta(minutes=15)
        time_out = datetime.datetime.now()
        functions.create_phantom(self.sqlshell, time_in=time_in,
                                 time_out=time_out)
        result = functions.check_last_record_time_out(self.sqlshell, time_out)
        self.assertEqual(result, 1)
        functions.delete_phantoms(sql_shell=self.sqlshell)

    def test_check_last_record_time_out_min3(self):
        time_in = datetime.datetime.now() - datetime.timedelta(minutes=15)
        time_out = datetime.datetime.now() - datetime.timedelta(minutes=3)
        functions.create_phantom(self.sqlshell, time_in=time_in,
                                 time_out=time_out)
        time_out = datetime.datetime.now()
        result = functions.check_last_record_time_out(self.sqlshell, time_out)
        self.assertEqual(result, 0)
        functions.delete_phantoms(sql_shell=self.sqlshell)

    def test_check_last_record_time_out_plus_three(self):
        time_in = datetime.datetime.now() - datetime.timedelta(minutes=15)
        time_out = datetime.datetime.now() + datetime.timedelta(minutes=3)
        functions.create_phantom(self.sqlshell, time_in=time_in,
                                 time_out=time_out)
        time_out = datetime.datetime.now()
        result = functions.check_last_record_time_out(self.sqlshell, time_out)
        self.assertEqual(result, 0)
        functions.delete_phantoms(sql_shell=self.sqlshell)

    def test_check_last_record_time_out_plus_one(self):
        time_in = datetime.datetime.now() - datetime.timedelta(minutes=15)
        time_out = datetime.datetime.now() + datetime.timedelta(minutes=1)
        functions.create_phantom(self.sqlshell, time_in=time_in,
                                 time_out=time_out)
        time_out = datetime.datetime.now()
        result = functions.check_last_record_time_out(self.sqlshell, time_out)
        self.assertEqual(result, 1)
        functions.delete_phantoms(sql_shell=self.sqlshell)

    def test_check_last_record_time_out_min_one(self):
        time_in = datetime.datetime.now() - datetime.timedelta(minutes=15)
        time_out = datetime.datetime.now() - datetime.timedelta(minutes=1)
        functions.create_phantom(self.sqlshell, time_in=time_in,
                                 time_out=time_out)
        time_out = datetime.datetime.now()
        result = functions.check_last_record_time_out(self.sqlshell, time_out)
        self.assertEqual(result, 1)
        functions.delete_phantoms(sql_shell=self.sqlshell)

    def test_check_last_record_time(self):
        class AR:
            status_ready = True

        ar = AR()
        time_in = datetime.datetime.now() - datetime.timedelta(minutes=15)
        time_out = datetime.datetime.now()
        functions.create_phantom(self.sqlshell, time_in, time_out,
                                 test_mode=None)
        time_out = datetime.datetime.now() + datetime.timedelta(minutes=3)
        result = functions.check_can_create_phantom(sql_shell=self.sqlshell,
                                                    ar_instance=ar,
                                                    time_out=time_out,
                                                    time_in=time_in,
                                                    work_end_hour=datetime.timedelta(
                                                        hours=8))
        self.assertTrue(result)

    def test_check_time_in_work_hours(self):
        result = functions.check_time_in_work_hours(time_in=datetime.datetime.now() - datetime.timedelta(hours=1),
                                                    time_out=datetime.datetime.now() - datetime.timedelta(hours=2, minutes=15),
                                                    work_end_hour=datetime.timedelta(hours=datetime.datetime.now().hour))
        self.assertTrue(result['status'])
        result = functions.check_time_in_work_hours(time_in=datetime.datetime.now() + datetime.timedelta(hours=1),
                                                    time_out=datetime.datetime.now() - datetime.timedelta(hours=2, minutes=15),
                                                    work_end_hour=datetime.timedelta(hours=datetime.datetime.now().hour))
        self.assertFalse(result['status'])
        self.assertTrue(result['info'] == 'time_in after wh')
        result = functions.check_time_in_work_hours(time_in=datetime.datetime.now() - datetime.timedelta(hours=1),
                                                    time_out=datetime.datetime.now() + datetime.timedelta(hours=2, minutes=15),
                                                    work_end_hour=datetime.timedelta(hours=datetime.datetime.now().hour))
        self.assertTrue(result['info'] == 'time_out after wh')
        self.assertFalse(result['status'])


if __name__ == '__main__':
    unittest.main()
