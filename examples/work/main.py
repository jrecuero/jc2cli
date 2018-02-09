from jc2cli.decorators import command, mode, argo
from jc2cli.argo_types import Str, Int, Line, CliType


class T_Tenant(CliType):

    DEFAULT = ["COMMON", "DEFAULT", "SINGLE", "MULTI"]

    def __init__(self, default, **kwargs):
        super(T_Tenant, self).__init__(**kwargs)
        # self._tenants = T_Tenant.DEFAULT
        self._tenants = default

    def _help_str(self):
        return 'Enter the Tenant where you want to go.'

    def get_complete_list(self, document, text):
        return self._tenants


@command('START app default')
@argo('app', Str(help='Enter app name'), "none")
@argo('default', Str(help='Enter default value'), "none")
def start(app, default):
    print('START: running in main module with "{0}" and "{1}"'.format(app, default))
    return True


@command('SEED value')
@argo('value', Int(help='Enter seed initial value'), 0)
def seed(value):
    print('SEED: running in main module with seed value {0}'.format(value))
    return True


@command('END time')
@argo('time', Int(), 0)
def end(time):
    print('END: running in main module at {0}'.format(time))
    return True


@command('TIME line')
@argo('line', Line(), None)
def the_time(line):
    print('TIME: running in main module with line: "{0}"'.format(line))
    return True


@command('TENANT tname')
@argo('tname', T_Tenant(['COKE', 'PEPSI']), None)
def tenant(tname):
    print('TENANT: running in main module with tenant name: "{0}"'.format(tname))
    return True


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
        print('start: running in main module main.Cli class with {0} and {1}'.format(app, default))
        return True

    @command("END time")
    @argo('time', Int(), 0)
    def end(self, time):
        print('end: running in main module main.Cli class at {0}'.format(time))
        return True
