import json

import requests
import urllib3

# No warnings for self signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Use a proper user agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'

# Header for urlencoded form data
HEADER_FORM_URLENCODED = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': USER_AGENT,
}

# Header for urlencoded form data
HEADER_JSON = {
    'Content-Type': 'application/json',
    'User-Agent': USER_AGENT,
}


class LoginError(Exception):
    pass

class ONUProfile():

    # Bandwidth multiplier
    __K = 131072

    def set_configuration(self):
        '''
        Adds profile to OLT config. Can be used to set configuration for an existing profile
        '''
        # If using default, then this is a new profile
        if 'profile-id' in self.profile.keys():
            # Get profiles from config
            profiles = list(self.client.get_onu_profiles().keys())
            # We don't need the 'profile-' part
            profiles = list(
                map(lambda x: str(x).replace('profile-', ''), profiles)
            )
            # Remove default profile
            profiles = list(filter(lambda x: x != 'default', profiles))
            # We need integers to compare
            profiles = list(
                map(lambda x: int(x), profiles)
            )
            # Get last profile id, add 1
            new_profile_id = max(profiles) + 1
            new_profile = f'profile-{str(new_profile_id)}'

            self.profile['profile-id']['bandwidth-limit-down'] = int(
                self.profile['profile-id']['bandwidth-limit-down'])*self.__K
            self.profile['profile-id']['bandwidth-limit-up'] = int(
                self.profile['profile-id']['bandwidth-limit-up'])*self.__K
            self.profile[new_profile] = self.profile.pop('profile-id')

        if self.profile:
            profile_list = {
                'onu-profiles': self.profile,
            }
            data = {
                "SET": profile_list,
            }
            return self.client.set_configuration(data)
        raise Warning('Profile not initialized')

    def add(self):
        '''
        Adds profile to OLT config. Can be used to set configuration for an existing profile
        '''
        return self.set_configuration()

    def save(self):
        '''
        Adds profile to OLT config. Can be used to set configuration for an existing profile.
        '''
        return self.set_configuration()

    def delete(self):
        '''
        Removes profile to OLT config
        '''
        if self.profile:
            profile_list = {
                'onu-profiles': self.profile,
            }
            data = {
                "DELETE": profile_list,
            }
            return self.client.set_configuration(data)
        raise Warning('Profile not initialized')

    def __init__(self, olt_client, profile="profile-bridge"):

        # OLT Client
        self.client = olt_client

        # If using a default one
        if profile == "profile-bridge" or profile == "profile-router":
            try:
                # Get profile
                with open(f'{profile}.json', 'r') as f:
                    self.profile = json.loads(f.read())
            except KeyError:
                raise KeyError(
                    'Could not get default configutation for profile {profile_id}'.format(profile))

        super().__init__()


class ONU():
    '''
    ONU Defintion with configuration
    '''

    def set_configuration(self):
        '''
        Use OLT Client to set ONU configuration
        '''
        onu_list = {
            'onu-list': {
                self.serial_number: self.onu,
            }
        }
        data = {
            "SET": onu_list,
        }
        return self.client.set_configuration(data)

    def add(self):
        '''
        Adds an onu. Can be used to set configuration for an existing ONU
        '''
        return self.set_configuration()

    def save(self):
        '''
        Adds an onu. Can be used to set configuration for an existing ONU
        '''
        return self.set_configuration()

    def delete(self):
        '''
        Use OLT Client to delete ONU configuration
        '''
        onu_list = {
            'onu-list': self.onu,
        }
        data = {
            "DELETE": onu_list,
        }
        return self.client.set_configuration(data)

    def status(self):
        '''
        Use OLT Client to retrieve ONU status
        '''
        return self.client.get_onu_status(self.serial_number)

    def __init__(self, olt_client, onu='onu-default'):

        # OLT Client
        self.client = olt_client
        # Get profile from dict
        profile = onu[list(onu.keys())[0]]
        # If using a default one
        if profile == "profile-bridge" or profile == "profile-router":
            try:
                # Get profile
                with open(f'{profile}.json', 'r') as f:
                    self.profile = json.loads(f.read())
            except KeyError:
                raise KeyError(
                    'Could not get default configutation for profile {profile_id}'.format(profile))
        self.serial_number = list(onu.keys())[0]
        self.onu = onu.pop(self.serial_number)
        super().__init__()


class OLTClient():
    '''
    Client interface to Ubiquiti UFiber OLT. Host can be a hostname or a IP address
    '''
    # Base Client
    client = requests.Session()

    def login(self):
        '''
        Login using credentials. Returns True/False
        '''
        # Build post request to login
        form_data = {
            'username': self.username,
            'password': self.password,
        }
        try:
            # Try to login
            response = self.client.post(
                verify=False,
                url=self.url,
                headers=HEADER_FORM_URLENCODED,
                data=form_data
            )
        except ConnectionError as ex:
            raise LoginError(ex)
        except TimeoutError as ex:
            raise LoginError(ex)
        # HTTP OK ?
        try:
            assert response.status_code, 200
        except AssertionError:
            raise requests.HTTPError('Got wrong reply from OLT HTTP interface')
        # If there is a port list, then we are logged in
        try:
            assert 'Port 0' in response.text, True
        except AssertionError:
            raise LoginError('Failed to log in with specified credentials')
        return True

    def get_configuration(self):
        '''
        Returns OLT general configuration. GPON configuration != here.
        '''
        assert self.logged_in, True
        url = self.url + '/api/edge/get.json'
        response = self.client.get(url)
        if response.status_code != 200:
            return False
        configuration = response.text
        return json.loads(configuration)['GET']

    def set_configuration(self, data):
        '''
        Sets configuration using data dict
        '''
        assert self.logged_in, True
        # Base url
        url = self.url + '/api/edge/batch.json'
        # Build headers, add CSRF token
        headers = HEADER_JSON
        headers['X-CSRF-TOKEN'] = self.client.cookies.get('X-CSRF-TOKEN')
        # Post configuration
        response = self.client.post(
            verify=False,
            url=url,
            headers=HEADER_JSON,
            json=data,
        )
        # Raise error if status != HTTP 200, OK
        if response.status_code != 200:
            raise ConnectionError()
        action = list(data.keys())[0]
        configuration = json.loads(response.text)[action]
        return configuration

    def delete_configuration(self, data):
        '''
        Deletes configuration using data dict
        '''
        assert self.logged_in, True
        # Base url
        url = self.url + '/api/edge/delete.json'
        # Build headers, add CSRF token
        headers = HEADER_JSON
        headers['X-CSRF-TOKEN'] = self.client.cookies.get('X-CSRF-TOKEN')
        # Post configuration
        response = self.client.post(
            verify=False,
            url=url,
            headers=HEADER_JSON,
            json=data,
        )
        # Raise error if status != HTTP 200, OK
        if response.status_code != 200:
            raise ConnectionError()
        configuration = json.loads(response.text)['DELETE']
        return configuration

    def get_bulk_onu_status(self):
        '''
        Returns list and status of provisioned ONUs
        '''
        assert self.logged_in, True
        url = self.url + '/api/edge/data.json?data=gpon_onu_list'
        response = self.client.get(url)
        if response.status_code != 200:
            return False
        response = json.loads(response.text)['output']['GET_ONU_LIST']
        onu_status = {}
        for onu in response:
            serial_number = onu.pop('serial_number')
            onu_status[serial_number] = onu
        return onu_status

    def get_onu_status(self, serial_number):
        '''
        Returns status of provisioned ONU
        '''
        assert self.logged_in, True
        try:
            # Get raw config
            status = self.get_bulk_onu_status()[serial_number]
            return status
        except KeyError:
            raise KeyError(
                'Could not get configutation for ONU {serial_number}'.format(serial_number))

    def get_onu(self, serial_number):
        '''
        Returns status of provisioned ONU
        '''
        assert self.logged_in, True
        try:
            # Get raw config
            onu = {
                serial_number: self.get_configuration()[
                    'onu-list'][serial_number]
            }
        except KeyError:
            raise KeyError(
                'Could not get configutation for onu {serial_number}'.format(serial_number))
        return ONU(self, onu=onu)

    def get_onu_profiles(self):
        '''
        Quickly return onu profiles from configuration
        '''
        assert self.logged_in, True
        return self.get_configuration()['onu-profiles']

    def get_onu_profile(self, profile_id):
        '''
        Get ONU profile by id
        '''
        assert self.logged_in, True
        try:
            # Get raw config
            profile = {
                profile_id: self.get_onu_profiles()[profile_id]
            }
        except KeyError:
            raise KeyError(
                'Could not get configutation for profile {profile_id}'.format(profile_id))

        return ONUProfile(self, profile)

    def __init__(self, host, username, password):
        self.host = host
        self.url = 'https://{host}'.format(host=host)
        self.username = username
        self.password = password
        self.logged_in = self.login()
        super().__init__()
