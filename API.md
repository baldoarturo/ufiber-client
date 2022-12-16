# Table of Contents

* [ufiber\_client3.olt](#ufiber_client3.olt)
  * [ONUProfile](#ufiber_client3.olt.ONUProfile)
    * [set\_configuration](#ufiber_client3.olt.ONUProfile.set_configuration)
    * [add](#ufiber_client3.olt.ONUProfile.add)
    * [save](#ufiber_client3.olt.ONUProfile.save)
    * [delete](#ufiber_client3.olt.ONUProfile.delete)
  * [ONU](#ufiber_client3.olt.ONU)
    * [set\_configuration](#ufiber_client3.olt.ONU.set_configuration)
    * [add](#ufiber_client3.olt.ONU.add)
    * [save](#ufiber_client3.olt.ONU.save)
    * [delete](#ufiber_client3.olt.ONU.delete)
    * [status](#ufiber_client3.olt.ONU.status)
  * [OLTClient](#ufiber_client3.olt.OLTClient)
    * [login](#ufiber_client3.olt.OLTClient.login)
    * [get\_configuration](#ufiber_client3.olt.OLTClient.get_configuration)
    * [set\_configuration](#ufiber_client3.olt.OLTClient.set_configuration)
    * [delete\_configuration](#ufiber_client3.olt.OLTClient.delete_configuration)
    * [get\_bulk\_onu\_status](#ufiber_client3.olt.OLTClient.get_bulk_onu_status)
    * [get\_onu\_status](#ufiber_client3.olt.OLTClient.get_onu_status)
    * [get\_onu](#ufiber_client3.olt.OLTClient.get_onu)
    * [get\_onu\_profiles](#ufiber_client3.olt.OLTClient.get_onu_profiles)
    * [get\_onu\_profile](#ufiber_client3.olt.OLTClient.get_onu_profile)

<a id="ufiber_client3.olt"></a>

# ufiber\_client3.olt

<a id="ufiber_client3.olt.ONUProfile"></a>

## ONUProfile Objects

```python
class ONUProfile()
```

<a id="ufiber_client3.olt.ONUProfile.set_configuration"></a>

#### set\_configuration

```python
def set_configuration()
```

Adds profile to OLT config. Can be used to set configuration for an existing profile

<a id="ufiber_client3.olt.ONUProfile.add"></a>

#### add

```python
def add()
```

Adds profile to OLT config. Can be used to set configuration for an existing profile

<a id="ufiber_client3.olt.ONUProfile.save"></a>

#### save

```python
def save()
```

Adds profile to OLT config. Can be used to set configuration for an existing profile.

<a id="ufiber_client3.olt.ONUProfile.delete"></a>

#### delete

```python
def delete()
```

Removes profile to OLT config

<a id="ufiber_client3.olt.ONU"></a>

## ONU Objects

```python
class ONU()
```

ONU Defintion with configuration

<a id="ufiber_client3.olt.ONU.set_configuration"></a>

#### set\_configuration

```python
def set_configuration()
```

Use OLT Client to set ONU configuration

<a id="ufiber_client3.olt.ONU.add"></a>

#### add

```python
def add()
```

Adds an onu. Can be used to set configuration for an existing ONU

<a id="ufiber_client3.olt.ONU.save"></a>

#### save

```python
def save()
```

Adds an onu. Can be used to set configuration for an existing ONU

<a id="ufiber_client3.olt.ONU.delete"></a>

#### delete

```python
def delete()
```

Use OLT Client to delete ONU configuration

<a id="ufiber_client3.olt.ONU.status"></a>

#### status

```python
def status()
```

Use OLT Client to retrieve ONU status

<a id="ufiber_client3.olt.OLTClient"></a>

## OLTClient Objects

```python
class OLTClient()
```

Client interface to Ubiquiti UFiber OLT. Host can be a hostname or a IP address

<a id="ufiber_client3.olt.OLTClient.login"></a>

#### login

```python
def login()
```

Login using credentials. Returns True/False

<a id="ufiber_client3.olt.OLTClient.get_configuration"></a>

#### get\_configuration

```python
def get_configuration()
```

Returns OLT general configuration. GPON configuration != here.

<a id="ufiber_client3.olt.OLTClient.set_configuration"></a>

#### set\_configuration

```python
def set_configuration(data)
```

Sets configuration using data dict

<a id="ufiber_client3.olt.OLTClient.delete_configuration"></a>

#### delete\_configuration

```python
def delete_configuration(data)
```

Deletes configuration using data dict

<a id="ufiber_client3.olt.OLTClient.get_bulk_onu_status"></a>

#### get\_bulk\_onu\_status

```python
def get_bulk_onu_status()
```

Returns list and status of provisioned ONUs

<a id="ufiber_client3.olt.OLTClient.get_onu_status"></a>

#### get\_onu\_status

```python
def get_onu_status(serial_number)
```

Returns status of provisioned ONU

<a id="ufiber_client3.olt.OLTClient.get_onu"></a>

#### get\_onu

```python
def get_onu(serial_number)
```

Returns status of provisioned ONU

<a id="ufiber_client3.olt.OLTClient.get_onu_profiles"></a>

#### get\_onu\_profiles

```python
def get_onu_profiles()
```

Quickly return onu profiles from configuration

<a id="ufiber_client3.olt.OLTClient.get_onu_profile"></a>

#### get\_onu\_profile

```python
def get_onu_profile(profile_id)
```

Get ONU profile by id

