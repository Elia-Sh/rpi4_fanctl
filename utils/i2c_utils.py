import logging
import shlex


from . import system_utils



def load_i2c_kernel_modules(modules_list = None):
    """
    requires root privelges -> modprobe
    """
    loaded_modules = []
    result_flag = False
    logging.info(f'loading k modules: {modules_list}')
    modprobe_cmd = 'modprobe'
    full_cmd = ''
    for module_name in modules_list:
        full_cmd = shlex.join([modprobe_cmd, module_name])
        load_cmd_result_obj = system_utils.run_system_command(full_cmd, fail_on_error=False)
        if load_cmd_result_obj.returncode != 0:
            error_message = 'return code of non-zero: {}, cmd: {}'.format(
                load_cmd_result_obj.returncode, full_cmd)
            logging.error(error_message)
        else:
            logging.info(f'loaded module: {module_name} successfully')
            loaded_modules.append(module_name)
    result_flag = len(loaded_modules) == len(modules_list)
    not_loaded_modules = list(set(modules_list) - set(loaded_modules))
    return result_flag


