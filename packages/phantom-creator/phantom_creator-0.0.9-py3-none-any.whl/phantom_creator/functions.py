import random
import datetime
import wsqluse.wsqluse
from phantom_creator import settings


def create_phantom(sqlshell, time_in, time_out, test_mode=False):
    command = "INSERT INTO records (car_number, brutto, tara, cargo, time_in, " \
              "time_out, inside, carrier, trash_cat, trash_type, operator)" \
              "VALUES ('{}', 1337, 1337, 1337, '{}', '{}', False," \
              "(SELECT id FROM clients WHERE short_name='ЮТК, ООО')," \
              "(SELECT id FROM trash_cats WHERE cat_name='Хвосты'), " \
              "(SELECT id FROM trash_types WHERE name='Прочее'), " \
              "(SELECT max(id) FROM users))"
    command = command.format(settings.ph_car_number, time_in, time_out)
    if test_mode:
        print(command)
        return
    sqlshell.try_execute(command)



def delete_phantoms(sql_shell):
    command = "DELETE FROM records WHERE car_number='{}'"
    command = command.format(settings.ph_car_number)
    return sql_shell.try_execute(command)


def get_cycle_time(work_hours_last: int, phantoms_amount_last: int):
    cycle_time = round(work_hours_last * 60 / phantoms_amount_last)
    return cycle_time


def if_work_started(work_start_time):
    now = datetime.datetime.now().time()
    if datetime.timedelta(hours=now.hour) > work_start_time:
        return True


def get_rand_minutes(minutes_range_start, minutes_range_end):
    rand_round = random.randrange(minutes_range_start, minutes_range_end)
    rand_round = round(rand_round)
    return rand_round


@wsqluse.wsqluse.tryExecuteGetStripper
def check_last_phantoms(sqlshell, phantom_car_number, date=None):
    if not date:
        date = datetime.datetime.today()
    command = "SELECT count(id) FROM records " \
              "WHERE time_in::date='{}' AND car_number='{}'"
    command = command.format(date, phantom_car_number)
    response = sqlshell.try_execute_get(command)
    return response


def get_work_hours_last(work_end_time):
    time_now = datetime.datetime.now().time()
    work_hours_last = (work_end_time - datetime.timedelta(
        hours=time_now.hour))
    whl_int = int(work_hours_last.seconds / 60 / 60)
    return whl_int


def check_can_create_phantom(sql_shell, ar_instance, time_out,
                             time_in: datetime.datetime,
                             work_end_hour: datetime.timedelta):
    if not check_last_record_time_in(sql_shell):
        if check_in_ar(ar_instance):
            if not check_last_record_time_out(sql_shell, time_out):
                check = check_time_in_work_hours(time_in, time_out,
                                                 work_end_hour)
                return check
            else:
                check_result = {'status': False, 'info': 'time_out'}
        else:
            check_result = {'status': False, 'info': 'ar_busy'}
    else:
        check_result = {'status': False, 'info': 'time_in'}
    print("Check_RESULT", check_result)
    return check_result


def check_time_in_work_hours(time_in: datetime.datetime,
                             time_out: datetime.datetime,
                             work_end_hour: datetime.timedelta):
    if datetime.timedelta(hours=time_in.hour) > work_end_hour:
        return {'status': False, 'info': 'time_in after wh'}
    elif datetime.timedelta(hours=time_out.hour) > work_end_hour:
        return {'status': False, 'info': 'time_out after wh'}
    return {'status': True}


@wsqluse.wsqluse.tryExecuteGetStripper
def check_last_record_time_in(sql_shell, wait_minutes=2):
    timenow = datetime.datetime.now() - datetime.timedelta(
        minutes=wait_minutes)
    command = "SELECT count(id) FROM records WHERE time_in>'{}'"
    command = command.format(timenow)
    response = sql_shell.try_execute_get(command)
    return response


@wsqluse.wsqluse.tryExecuteGetStripper
def check_last_record_time_out(sql_shell, time_out, wait_minutes=2):
    time_out_min = time_out - datetime.timedelta(
        minutes=wait_minutes)
    time_out_max = time_out + datetime.timedelta(
        minutes=wait_minutes)
    command = "SELECT count(id) FROM records WHERE time_out>='{}' and time_out<='{}'"
    command = command.format(time_out_min, time_out_max)
    response = sql_shell.try_execute_get(command)
    return response


def check_in_ar(ar_instance):
    if ar_instance.status_ready:
        return True


def get_today_phantoms_amount():
    today = datetime.datetime.today().weekday()
    return settings.daily_phantoms_amount[today]
