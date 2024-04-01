
import os
import sys
import time
import shlex
import subprocess


import logging

## general utils module ##
def setup_logger():
    """
    The method adds stdout to root logger,
    after setup() use:
    logging.info("message")
    logging.debug("debug message")
    """
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - [%(process)s] {%(filename)s:%(lineno)4d} - %(levelname)8s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
    logging.info('finished setting up logger')


def print_and_bail(message='bailing out..', return_code=1):
    logging.error(message)
    sys.exit(return_code)


def idle_for_n_seconds(n_seconds = 10):
    logging.info(f'returning to sleep for {n_seconds}')
    time.sleep(n_seconds)
    logging.info(f'resuming control to main loop')

def is_superuser():
    user_id = os.getuid()
    logging.info(f'exec user id is: {user_id}')
    result_flag = False
    if user_id == 0:
        result_flag = True
    return result_flag


def get_status_system_command(cmd='', cmd_args=['',], timeout_seconds=30) -> bool:
    cmd_result = True
    pass

def run_system_command(cmd='', cmd_args_list=None,
                       timeout_seconds=30, fail_on_error=True,
                       return_results_as_text=True):
    """
    executes system command 
    and returns output -> TODO which format?
    TODO2 -> maybe convert to popen
    proc = subprocess.Popen(full_cmd)
    """
    full_cmd_list = []
    if not cmd:
        return -1
    if cmd_args_list:
        full_cmd_list = shlex.split(cmd) + cmd_args_list
    else:
        full_cmd_list = shlex.split(cmd)
    logging.info(f'executing system cmd: {full_cmd_list}')
    result_obj = subprocess.run(full_cmd_list,
                        capture_output=True, timeout=timeout_seconds,
                        check = fail_on_error, text=return_results_as_text)
    if result_obj.stderr:
        logging.warning(f'cmd includes error --> {full_cmd_list}')
    return result_obj

def read_system_temperature():
    """
    /sys/class/thermal/thermal_zone0/temp
    /sys/class/hwmon/hwmon0/temp1_input
    """
    thermal_sources_fd_list = [
        '/sys/class/thermal/thermal_zone0/temp',
        '/sys/class/hwmon/hwmon0/temp1_input',
    ]
    logging.info('reading system temperature')
    system_temp = -1
    for thermal_source_fd in thermal_sources_fd_list:
        logging.info(f'reading temp from: {thermal_source_fd}')
        temp_value = ''
        with open(thermal_source_fd) as fd:
            temp_value = fd.read()
            temp_value_int = int(temp_value.strip())
        if temp_value:
            logging.info(f'found temp of: {temp_value_int} ---> single int of micro celsius')
            system_temp = temp_value_int
            break
    if system_temp < 0:
        logging.error(f'not logical temp value of: {system_temp}')
    return system_temp



def test_modules_installed_list(modules_list = None):
    """
    The method checks if k modules are installed on sysmtem -> not as running
    """
    result_flag = False # all modules installed
    modules_to_search = modules_list.copy()# no found -> compare at end if all found
    modinfo_cmd = 'modinfo'
    full_cmd = ''
    for module_name in modules_list:
        full_cmd = shlex.join([modinfo_cmd, module_name])
        logging.info(f'searching for: {module_name} with "{full_cmd}"')
        cmd_result_obj = run_system_command(full_cmd, fail_on_error=False)
        if cmd_result_obj.returncode == 0:
            logging.info(f'module: {module_name} is installed on system')
            modules_to_search.remove(module_name)
        else:
            logging.debug(f'failed to find: {module_name} on system, {cmd_result_obj}')

    logging.info(f'searched for all modules: {modules_list} with "{modinfo_cmd}"')
    if len(modules_to_search) > 0:
        message = f'not all modules installed - check {modinfo_cmd} for each of: {modules_to_search}'
        logging.error(message)
    else:
        logging.info(f'found all expected system modules: {modules_list}')
        result_flag = True
    return result_flag

def test_module_loaded(module_name_str = ''):
    """
    returns if kernel module loaded
    """
    return test_module_loaded([module_name_str])

def test_modules_loaded_list(modules_list = None):
    """
    returns if kernel module loaded
    """
    modules_to_search = modules_list.copy()# no found -> compare at end if all found
    result_flag = False # all modules loaded
    lsmod_cmd = 'lsmod'
    logging.info(f'searching for: {modules_to_search} with "{lsmod_cmd}"')
    cmd_result_obj = run_system_command(lsmod_cmd)
    cmd_output_list = cmd_result_obj.stdout.splitlines()
    #TODO utilize dataframe
    #data_frame = pd.read_fwf(io.StringIO(cmd_output))
    for entry in cmd_output_list:
        for module_name in modules_list:
            if module_name in entry:
                logging.info(f'found: {module_name}')
                modules_to_search.remove(module_name)
    if len(modules_to_search) > 0:
        logging.error(f'failed to find: {modules_to_search}')
    else:
        logging.info(f'found all expected system modules: {modules_list}')
        result_flag = True
    #return result_flag
    return modules_to_search    # return not found modules list

def install_kernel_modules(modules_list = None):
    """
    requires root privelges
    """
    install_result_flag = False
    logging.info(f'installing modules: {modules_list}')
    return install_result_flag



