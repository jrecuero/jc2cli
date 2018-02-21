from jc2cli.decorators import command, mode, argo
from jc2cli.argo_types import Str, Int, Line, CliType
from jc2cli.error_handler import CliValidationError
import jc2cli.tools.loggerator as loggerator

MODULE = 'EXAMPLES.WORK.main'
logger = loggerator.getLoggerator(MODULE)
database = ['COKE', 'PEPSI']


def get_database_data():
    return database


class T_Tenant(CliType):

    def __init__(self, db_data_cb, **kwargs):
        super(T_Tenant, self).__init__(**kwargs)
        self._tenants_cb = db_data_cb

    def _help_str(self):
        return 'Enter the Tenant where you want to go.'

    def get_complete_list(self, document, text):
        return self._tenants_cb()

    def validate(self, value):
        if value not in self._tenants_cb():
            raise CliValidationError('MAIN', 'Validation Error: {}'.format(value))


@command('START app default')
@argo('app', Str(help='Enter app name'), "none")
@argo('default', Str(help='Enter default value'), "none")
def start(app, default):
    logger.display('START: running in main module with "{0}" and "{1}"'.format(app, default))
    return True


@command('SEED value')
@argo('value', Int(help='Enter seed initial value'), 0)
def seed(value):
    logger.display('SEED: running in main module with seed value {0}'.format(value))
    return True


@command('END time')
@argo('time', Int(), 0)
def end(time):
    logger.display('END: running in main module at {0}'.format(time))
    return True


@command('TEST time')
@argo('time', Int(), 0)
def do_test(time):
    return 'TEST: running in main module at {0}'.format(time)


@command('TIME line')
@argo('line', Line(), None)
def the_time(line):
    logger.display('TIME: running in main module with line: "{0}"'.format(line))
    return True


@command('TENANT tname')
@argo('tname', T_Tenant(get_database_data), None)
def tenant(tname):
    logger.display('TENANT: running in main module with tenant name: "{0}"'.format(tname))
    return True


@command('INTERFACE [eth | l3out]?')
@argo('eth', Str(), 'none')
@argo('l3out', Str(), 'none')
def do_interface(eth, l3out):
    logger.display('INTERFACE: running in main module with eth: "{0}" and l3out: "{1}"'.format(eth, l3out))
    return True


@command('ADD-TENANT tname')
@argo('tname', Str(), None)
def do_add_tenant(tname):
    database.append(tname)
    logger.display('ADD-TENANT: add tenant : "{0}"'.format(tname))
    return True


@command('LEAF name [<eth> | <l3out>]!')
@argo('name', Str(), None)
@argo('eth', Str(), 'none')
@argo('l3out', Str(), 'none')
def do_leaf(name, eth, l3out):
    logger.display('LEAF: running in main module with eth: "{0}" and l3out: "{1}" for name: "{2}"'.format(eth, l3out, name))
    return True


# @command('LEAF [<eth> name1 | <l3out> name2]!')
# @argo('eth', Str(), 'none')
# @argo('name1', Str(), 'none')
# @argo('l3out', Str(), 'none')
# @argo('name2', Str(), 'none')
# def do_leaf(eth, name1, l3out, name2):
#     logger.display('LEAF: running in main module with eth: "{} {}" and l3out: "{} {}"'.format(eth, name1, l3out, name2))
#     return True


@command('exit')
def do_exit():
    logger.display('this is a new exit')
    return False


@mode("CLI", "examples.work.main.Cli")
def cli():
    return True


class Cli(object):

    def __init__(self):
        pass

    @command('START app default')
    @argo('app', Str(help='Enter CLI application'), "none")
    @argo('default', Str(help='Enter CLI default value'), "none")
    def start(self, app, default):
        logger.display('start: running in main module main.Cli class with {0} and {1}'.format(app, default))
        return True

    @command("END time")
    @argo('time', Int(), 0)
    def end(self, time):
        logger.display('end: running in main module main.Cli class at {0}'.format(time))
        return True
