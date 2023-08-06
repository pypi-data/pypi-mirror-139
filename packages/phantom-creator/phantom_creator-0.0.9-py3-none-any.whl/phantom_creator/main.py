from phantom_creator import functions
from phantom_creator import settings
import datetime
import time
import random


def work(sqlshell, work_start_time: datetime.timedelta,
         work_end_time: datetime.timedelta, ar_instance, phantoms_need=None,
         test_mode=False):
    alert_too_fast = 0
    if not phantoms_need:
        phantoms_need = functions.get_today_phantoms_amount()
    while alert_too_fast < 3:  # Предохранитель спама
        if functions.if_work_started(work_start_time):
            work_hours_last = functions.get_work_hours_last(work_end_time)
            print("WHL", work_hours_last)
            phantoms_already_created = functions.check_last_phantoms(
                sqlshell, settings.ph_car_number)
            print("PAC", phantoms_already_created)
            phantoms_last = phantoms_need - phantoms_already_created
            print("PC", phantoms_last)
            cycle_time_minutes = functions.get_cycle_time(work_hours_last,
                                                          phantoms_last)

            if cycle_time_minutes < 5:  # Предохранитель спама
                alert_too_fast += 1
            else:
                alert_too_fast = 0
            cycle_minutes_rand = functions.get_rand_minutes(cycle_time_minutes-(cycle_time_minutes/100 * 30),
                                                            cycle_time_minutes)
            cycle_seconds = cycle_minutes_rand * 60 + random.randrange(0, 55)
            if test_mode:
                cycle_seconds = 5
            print("To WAIT:", cycle_seconds)
            # Ждем начала цикла
            time.sleep(cycle_seconds)
            time_in = datetime.datetime.now()
            time_out_rand = functions.get_rand_minutes(4, 21)
            time_out = time_in + datetime.timedelta(minutes=time_out_rand,
                                                    seconds=random.randrange(0,
                                                                             55))
            check_result = functions.check_can_create_phantom(sqlshell,
                                                              ar_instance,
                                                              time_out,
                                                              time_in,
                                                              work_end_time
                                                              )
            while True:
                if check_result['status']:
                    functions.create_phantom(sqlshell, time_in=time_in,
                                             time_out=time_out,
                                             test_mode=test_mode)
                    break
                elif check_result['info'] == 'time_in' or check_result['info'] == 'ar_busy':
                    check_result = functions.check_can_create_phantom(sqlshell,
                                                                      ar_instance,
                                                                      time_out,
                                                                      time_in,
                                                                      work_end_time)
                elif check_result['info'] == 'time_out':
                    time_out_rand = functions.get_rand_minutes(14, 21)
                    time_out = time_in + datetime.timedelta(
                        minutes=time_out_rand,
                        seconds=random.randrange(0,
                                                 55))
                    check_result = functions.check_can_create_phantom(sqlshell,
                                                                      ar_instance,
                                                                      time_out,
                                                                      time_in,
                                                                      work_end_time)
                elif check_result['info'] == 'time_in after wh':
                    time_in = time_in - datetime.timedelta(minutes=2)
                    check_result = functions.check_can_create_phantom(sqlshell,
                                                                      ar_instance,
                                                                      time_out,
                                                                      time_in,
                                                                      work_end_time)
                elif check_result['info'] == 'time_out after wh':
                    time_out = time_out - datetime.timedelta(minutes=2)
                    check_result = functions.check_can_create_phantom(sqlshell,
                                                                      ar_instance,
                                                                      time_out,
                                                                      time_in,
                                                                      work_end_time)
                time.sleep(2)
        else:
            time.sleep(2)
