import sims4.commands
import services
from server_commands.argument_helpers import get_optional_target, OptionalSimInfoParam, SimInfoParam, TunableInstanceParam

from objects import HiddenReasonFlag, ALL_HIDDEN_REASONS


@sims4.commands.Command('age_menu', command_type=(sims4.commands.CommandType.Live), console_type=(sims4.commands.CommandType.Cheat))
def age_menu(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output('1) age_menu')
    output('    Lists all age options and descriptions')
    output('2) sap <first name> <last name> <0-100>')
    output('    Sets the age progress percentage for the current life stage of the named sim')
    output('3) sap_all <0-100>')
    output('    Sets the age progress percentage for the current life stage of all sims')
    output('4) age_down <first name> <last name>')
    output('    Sets age stage to the previous age for the named sim')
    output('5) age_down_all')
    output('    Sets age stage to the previous age for all sims')
    output('6) age_up <first name> <last name>')
    output('    Sets age stage to the next age for the named sim')
    output('7) age_up_all')
    output('    Sets age stage to the next age for all sims')
    output('8) age_options')
    output('    List age options 1-7')
    output('9) set_age <first name> <last name> <1-7>')
    output('    To display age stage options type: "age_options"')
    output('10) set_age_all <1-7>')
    output('    Sets age stage to selected stage for all sims')
    output('11) set_age_group <1-7> <1-7>')
    output('    Sets age stage for all sims of one stage to another stage')


@sims4.commands.Command('sap', command_type=(sims4.commands.CommandType.Live), console_type=(sims4.commands.CommandType.Cheat))
def set_age_progress(info1: SimInfoParam, age_progress: float = 0.0, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    try:
        # # TEMPORARY
        # output(str(type(dir(info1))))
        # for item in dir(info1):
        #     output(item)
        info1.set_age_progress_percentage(age_progress / 100)
        info1.resend_age_progress_data()
        output('Age progress set to {}% for {} {}'.format(
            age_progress, info1.first_name, info1.last_name))
        return True
    except Exception as e:
        output(str(e))


@sims4.commands.Command('sap_all', command_type=(sims4.commands.CommandType.Live), console_type=(sims4.commands.CommandType.Cheat))
def sap_all(age_progress: float = 0.0, allow_hidden_flags: HiddenReasonFlag = ALL_HIDDEN_REASONS, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    info_manager = services.sim_info_manager()
    all_sims = tuple(info_manager.get_all())
    count = 0
    for sim in all_sims:
        try:
            sim.set_age_progress_percentage(age_progress / 100)
            sim.resend_age_progress_data()
            output('Age progress set to {}% for {} {}'.format(
                age_progress, sim.first_name, sim.last_name))
            count += 1
        except Exception as e:
            output(str(e))

    output(f'Total sims: {len(all_sims)}')
    output(f'Sims affected: {count}')


@sims4.commands.Command('age_down', command_type=(sims4.commands.CommandType.Live), console_type=(sims4.commands.CommandType.Cheat))
def set_age_progress(info1: SimInfoParam, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    try:
        if not info1.is_infant:
            info1.reverse_age()
            info1.resend_age_progress_data()
            output('{} {} aged down'.format(info1.first_name, info1.last_name))
        else:
            output('{} {} is an infant'.format(
                info1.first_name, info1.last_name))
        return True
    except Exception as e:
        output(str(e))


@sims4.commands.Command('age_down_all', command_type=(sims4.commands.CommandType.Live), console_type=(sims4.commands.CommandType.Cheat))
def age_down_all(allow_hidden_flags: HiddenReasonFlag = ALL_HIDDEN_REASONS, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    info_manager = services.sim_info_manager()
    all_sims = tuple(info_manager.get_all())
    count = 0
    for sim in all_sims:
        try:
            if not sim.is_infant:
                sim.reverse_age()
                sim.resend_age_progress_data()
                output('{} {} aged down'.format(sim.first_name, sim.last_name))
                count += 1
            else:
                output('{} {} is an infant'.format(
                    sim.first_name, sim.last_name))
        except Exception as e:
            output(str(e))
    output(f'Total sims: {len(all_sims)}')
    output(f'Sims affected: {count}')


@sims4.commands.Command('age_up', command_type=(sims4.commands.CommandType.Live), console_type=(sims4.commands.CommandType.Cheat))
def set_age_progress(info1: SimInfoParam, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    try:
        if not info1.is_elder:
            info1.callback_auto_age()
            info1.resend_age_progress_data()
            output('{} {} aged up'.format(info1.first_name, info1.last_name))
        else:
            output('{} {} is an elder'.format(
                info1.first_name, info1.last_name))
        return True
    except Exception as e:
        output(str(e))


@sims4.commands.Command('age_up_all', command_type=(sims4.commands.CommandType.Live), console_type=(sims4.commands.CommandType.Cheat))
def age_up_all(allow_hidden_flags: HiddenReasonFlag = ALL_HIDDEN_REASONS, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    info_manager = services.sim_info_manager()
    all_sims = tuple(info_manager.get_all())
    count = 0
    for sim in all_sims:
        try:
            if not sim.is_elder:
                sim.callback_auto_age()
                sim.resend_age_progress_data()
                output('{} {} aged up'.format(sim.first_name, sim.last_name))
                count += 1
            else:
                output('{} {} is an elder'.format(
                    sim.first_name, sim.last_name))
        except Exception as e:
            output(str(e))
    output(f'Total sims: {len(all_sims)}')
    output(f'Sims affected: {count}')


age_options = ['infant', 'todler', 'child',
               'teenager', 'young adult', 'adult', 'elder']


def display_age_menu(output, message=None):
    output('Age options:')
    for index, age_option in enumerate(age_options):
        output(f"{index + 1}) {age_option}")
    if message is not None:
        output(f'To use this command type: {message}')


@sims4.commands.Command('age_options', command_type=(sims4.commands.CommandType.Live), console_type=(sims4.commands.CommandType.Cheat))
def show_age_options(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    display_age_menu(output)


def go_to_age(sim, target_age, initial_age=None):
    current_age = None
    if sim.is_elder:
        current_age = 6
    elif sim.is_adult:
        current_age = 5
    elif sim.is_young_adult:
        current_age = 4
    elif sim.is_teen:
        current_age = 3
    elif sim.is_child:
        current_age = 2
    elif sim.is_toddler:
        current_age = 1
    elif sim.is_infant:
        current_age = 0
    if current_age is None or current_age == target_age:
        return False
    if initial_age is not None and current_age != initial_age:
        return False
    while current_age > target_age:
        sim.reverse_age()
        current_age -= 1
    while current_age < target_age:
        sim.callback_auto_age()
        current_age += 1
    sim.resend_age_progress_data()
    return True


@sims4.commands.Command('set_age', command_type=(sims4.commands.CommandType.Live), console_type=(sims4.commands.CommandType.Cheat))
def set_age_progress(info1: SimInfoParam = None, age_option=None, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    message = 'set_age <first name> <last name> <option 1-7>'
    if age_option is None or info1 is None:
        display_age_menu(output, message)
        return
    try:
        target_age = int(age_option) - 1
        go_to_age(info1, target_age)
        output('{} {} age has been set to {}'.format(
            info1.first_name, info1.last_name, age_options[target_age]))
        return True
    except Exception as e:
        display_age_menu(output, message)


@sims4.commands.Command('set_age_all', command_type=(sims4.commands.CommandType.Live), console_type=(sims4.commands.CommandType.Cheat))
def set_age_all(age_option=None, allow_hidden_flags: HiddenReasonFlag = ALL_HIDDEN_REASONS, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    info_manager = services.sim_info_manager()
    all_sims = tuple(info_manager.get_all())
    count = 0
    message = 'set_age_all <option 1-7>'
    if age_option is None:
        display_age_menu(output, message)
        return
    try:
        target_age = int(age_option) - 1
        if not target_age >= 0 and not target_age <= 6:
            display_age_menu(output, message)
            return
    except:
        display_age_menu(output, message)
        return
    for sim in all_sims:
        try:
            result = go_to_age(sim, target_age)
            if result:
                output(
                    f'{sim.first_name} {sim.last_name} age has been set to {age_options[target_age]}')
                count += 1
        except Exception as e:
            output(str(e))
    output(f'Total sims: {len(all_sims)}')
    output(f'Sims affected: {count}')


@sims4.commands.Command('set_age_group', command_type=(sims4.commands.CommandType.Live), console_type=(sims4.commands.CommandType.Cheat))
def set_age_group(age_option1=None, age_option2=None, allow_hidden_flags: HiddenReasonFlag = ALL_HIDDEN_REASONS, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    info_manager = services.sim_info_manager()
    all_sims = tuple(info_manager.get_all())
    count = 0
    message = 'set_age_group <option 1-7> <option 1-7'
    if age_option1 is None or age_option2 is None:
        display_age_menu(output, message)
        return
    try:
        initial_age = int(age_option1) - 1
        target_age = int(age_option2) - 1
        if not target_age >= 0 and not target_age <= 6:
            display_age_menu(output, message)
            return
        if not initial_age >= 0 and not initial_age <= 6:
            display_age_menu(output, message)
    except:
        display_age_menu(output, message)
        return
    for sim in all_sims:
        try:
            result = go_to_age(sim, target_age, initial_age)
            if result:
                output(
                    f'{sim.first_name} {sim.last_name} age has been set to {age_options[target_age]} from {age_options[initial_age]}')
                count += 1
        except Exception as e:
            output(str(e))
    output(f'Total sims: {len(all_sims)}')
    output(f'Sims affected: {count}')


# @sims4.commands.Command('speed_options', command_type=(sims4.commands.CommandType.Live), console_type=(sims4.commands.CommandType.Cheat))
# def show_speed_options(_connection=None):
#     output = sims4.commands.CheatOutput(_connection)
#     output('1) Fast')
#     output('2) Normal')
#     output('3) Slow')
#     output('4) Slower')
#     output('5) Even Slower')
#     output('6) Very Slow')


# @sims4.commands.Command('set_age_speed', command_type=(sims4.commands.CommandType.Live), console_type=(sims4.commands.CommandType.Cheat))
# def set_age_speed(age_speed=None, _connection=None):
#     if age_speed is None:
#         return
#     output = sims4.commands.CheatOutput(_connection)
#     try:
#         speed = int(age_speed) - 1
#         services.get_aging_service().set_aging_speed(speed)
#         output(f'Ageing speed set to {age_speed}')
#     except Exception as e:
#         output(str(e))
