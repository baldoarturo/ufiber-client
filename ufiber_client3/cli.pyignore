import cmd
import getpass
from olt import OLTClient, LoginError
from onu import ONU, ONUWiFi
from onu_profile import ONUProfile


def console(data, header=None):
    '''
    Helper function to print key/value pairs in 2 columns
    '''
    if header:
        print(f'\n{header}')
    for key, value in data.items():
        s = "{:<30} {}".format(key, value)
        print(s)


class UFiberCLI(cmd.Cmd):
    intro = 'UFiber Client for fw version 3.1.3'
    prompt = 'UFiber> '

    def do_connect(self, host):
        '''
        Opens a new OLT connection
        Usage: connect {host/ip address>
        '''
        if str(host).strip() == '':
            print('Host or IP address required')
            return False
        username = input('Username:')
        password = getpass.getpass('Password:')
        try:
            print(f'Logging to {host} ...')
            self.client = OLTClient(host, username, password)
            print(f'Connection OK')
        except LoginError as ex:
            print(ex)
        except AssertionError as ex:
            print(ex)

    def do_quit(self, arg):
        '''
        Quits the command line client
        '''
        print('Bye.')
        quit(0)

    def do_show(self, arg):
        '''
        show configuration                  Shows OLT configuration
        show onus                           Shows OLT configured ONUs
        show onu SERIALNUMBER config        Shows ONU configuration
        show onu SERIALNUMBER status        Shows ONU status
        show profiles                       Shows OLT GPON profiles list
        show profile PROFILE-ID             Shows OLT GPON Profile configuration
        '''
        try:
            assert(self.client)
        except AttributeError:
            print('Not connected to OLT')
            return False

        # No spaces
        arg = arg.strip()

        if arg == 'configuration':
            configuration = self.client.get_configuration()
            print(configuration)
            return False

        if arg == 'configuration':
            configuration = self.client.get_configuration()
            print(configuration)
            return False

        if arg == 'onus':
            configuration = self.client.get_configuration()
            onus = configuration['onu-list']
            for key, value in onus.items():
                onu_brief = {
                    key: value['name']
                }
                console(onu_brief)
            return False

        if arg.split(' ')[0] == 'onu':

            if len(arg.split(' ')) < 3:
                return False

            # Proper case for serial number
            serial_number = str(arg.split(' ')[1]).strip()
            serial_number = serial_number[:4].upper()+serial_number[4:].lower()

            action = str(arg.split(' ')[2]).strip()

            if action == 'config':
                configuration = self.client.get_configuration()
                onu = configuration['onu-list'][serial_number]
                wifi = onu.pop('wifi')
                console(onu, 'ONU CONFIGURATION')
                console(wifi, 'WIFI CONFIGURATION')
                return False

            if action == 'status':
                onu = self.client.get_onu_status(serial_number)
                optics = onu.pop('optics')
                stats = onu.pop('stats')
                console(onu, 'ONU CONFIGURATION')
                console(optics, 'ONU OPTICS')
                console(stats, 'ONU TRAFFIC STATS')
                return False

        if arg == 'profiles':

            profiles = self.client.get_onu_profiles()

            for profile_key in profiles:

                profile = profiles[profile_key]
                profile_brief = {
                    'name': profile['name'],
                }

                console(profile_brief, profile_key)

            return False

        if arg == 'profiles detail':

            profiles = self.client.get_onu_profiles()

            for profile_key in profiles:

                profile = profiles[profile_key]

                router_mode = profile.pop('router-mode')
                bridge_mode = profile.pop('bridge-mode')
                if profile['mode'] == ONUProfile.MODE_ROUTER:
                    mode = router_mode
                if profile['mode'] == ONUProfile.MODE_BRIDGE:
                    mode = bridge_mode

                services = profile.pop('services')
                port = profile.pop('port')

                console(profile, f'GPON PROFILE {profile_key}')
                console(mode, 'NETWORK MODE')
                console(services, 'ONU SERVICES')
                console(port, 'PORT CONFIGURATION')
            return False

        if arg.split(' ')[0] == 'profile':
            profile_id = str(arg.split(' ')[1]).strip()
            profile = self.client.get_onu_profile(profile_id)
            console(profile, 'GPON PROFILE')
            return False

    def do_onu(self, arg):
        '''
        onu set SERIALNUMBER PROFILE PPPOE_USER PPPOE_PASS NAME     Sets ONU configuration
        onu delete SERIALNUMBER                                     Deletes ONU configuration
        '''
        try:
            assert(self.client)
        except AttributeError:
            print('Not connected to OLT')
            return False

        if len(arg.split(' ')) < 3:
            return False

        if arg.split(' ')[0] == 'set':
            serial_number = arg.split(' ')[1].strip()
            profile = arg.split(' ')[2].strip()
            pppoe_user = arg.split(' ')[3].strip()
            pppoe_password = arg.split(' ')[4].strip()

            args_count = len(arg.split(' '))
            name = ''
            for a in arg.split(' ')[5:args_count]:
                name = name + a + ' '
            name = name.strip()

            wifi = ONUWiFi()
            onu = ONU(self.client, serial_number, profile,
                      name, wifi, pppoe_user=pppoe_user, pppoe_password=pppoe_password)
            onu.save()
            print(f'Saved ONU {serial_number}')
            return False

        if arg.split(' ')[0] == 'delete':
            serial_number = arg.split(' ')[1]
            onu = self.client.get_onu(serial_number)
            onu.delete()
            print(f'Deleted ONU {serial_number}')
            return False


UFiberCLI().cmdloop()
