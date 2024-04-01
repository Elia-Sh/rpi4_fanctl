import logging


import time
import shlex

#import io
#import pandas as pd

from utils import system_utils
from utils import i2c_utils



def setup_fanctl_modules():
    module_names = ['i2c_dev', 'i2c_bcm2835']
    is_super_user = system_utils.is_superuser()
    if not is_super_user:
        logging.info('DEBUG ONLY ---> disable superuser check')
        system_utils.print_and_bail('user must be useruser')
    modules_installed_bool = system_utils.test_modules_installed_list(module_names)
    setup_result_flag = False   # setup completed successfully
    #TODO maybe replace status flags with enum for result -> 0 fail + result, 1 success
    if not modules_installed_bool:
        # attempting to fix
        install_fix_result = install_kernel_modules()
        if not install_fix_result:
            system_utils.print_and_bail('failed to install required k modules')
    missing_loaded_modules_list = system_utils.test_modules_loaded_list(module_names)
    if missing_loaded_modules_list:
        # attempting to fix
        load_fix_result = i2c_utils.load_i2c_kernel_modules(missing_loaded_modules_list)
        if not load_fix_result:
            system_utils.print_and_bail('failed to load required k modules')
    return setup_result_flag



def get_argon_i2c_bus_int():
    """
    i2cdetect -l
    i2cdetect -y 1 0x10 0x1f
    i2cdetect -y 1  # -> on my machine
    ## I2C bus name provided as int
    """
    BMC_CONTROLLER_PREFIX = 'bcm2835'
    TESTED_ADDRESSES_RANGE_STR = '0x10 0x1f'    # range rep in hexa
    result_bus_int = -1
    literal_identifier = '10: -- -- -- -- -- -- -- -- -- -- 1a -- -- -- -- --'
    i2cdetect_cmd = 'i2cdetect'
    i2cdetect_list_all_cmd = f'{i2cdetect_cmd} -l'
    logging.info(f'reading i2c bus number for argon device via: {i2cdetect_cmd}')
    cmd_res_obj = system_utils.run_system_command(i2cdetect_list_all_cmd)
    for line in cmd_res_obj.stdout.splitlines():
        controller_id, _ ,controller_type, *_  = line.split()   # "smart" list unpack
        controller_id_int = int(controller_id[-1])
        logging.debug(f'testing i2c bus number: {controller_id}')
        i2cdetect_list_detail_cmd = f'{i2cdetect_cmd} -y {controller_id_int} {TESTED_ADDRESSES_RANGE_STR}'
        logging.debug(i2cdetect_list_detail_cmd)
        cmd_details_single_bus_res_obj = system_utils.run_system_command(i2cdetect_list_detail_cmd)
        current_bus_details_str = cmd_details_single_bus_res_obj.stdout
        if literal_identifier in current_bus_details_str:
            logging.info(f'Awesome, detected argon i2c bus ---> id: {controller_id}')
            result_bus_int = controller_id_int
            break;
    #logging.warning('DEBUGGGING ---> hardcoded value')
    #result_bus_int = 1
    if result_bus_int < 0: 
        logging.error(f'invalid i2c bus id ----> {result_bus_int}')
    return result_bus_int


def set_fan_state(w_percent=0):
    """
    sets fan on/off
        0 = off
        1 = 10% speed
        ...
        10 = 100% speed  -> 0x64
    /usr/sbin/i2cset -y 1 0x01a 0x64
    """
    logging.info(f'setting fan speed to working percent: {w_percent}')
    fan_speed_hexa = 0
    logging.info('getting i2c bus number for device')
    i2c_bus_int = get_argon_i2c_bus_int()
    full_cmd = f'/usr/sbin/i2cset -y {i2c_bus_int} 0x01a 0x64'
    cmd_res = system_utils.run_system_command(full_cmd)

def fan_set_temp_dynamically():
    """
    """
    temperature_thresholds = {
        1:{'temp_micro_c':40000},
        2:50000,
        3:60000,
    }
    temperature_value = system_utils.read_system_temperature()
    temperature_value_celsius_float = temperature_value / 1000
    logging.info(f'dynamic set temp func ---> detected temp of: {temperature_value_celsius_float} C')
    if temperature_value < temperature_thresholds.get(1).get('temp_micro_c'):
        logging.info('Alert temp low -> turning off fan')
        set_fan_state(0)
    else:
        logging.info('Alert temp turning, turning on fan')
        # turning on fan
        set_fan_state(10)

def get_random_temp_reading_micro_celsius(low_value_float = 30.0, high_value=100.0):
    random_temp_value = 10
    return random_temp_value





def main():
    system_utils.setup_logger()
    logging.info('Starting fan_ctl')
    setup_fanctl_modules()
    logging.info('ok -> setup finished starting monitoring loop')
    while True:
        fan_set_temp_dynamically()
        system_utils.idle_for_n_seconds()


if __name__ == "__main__":
    main()

