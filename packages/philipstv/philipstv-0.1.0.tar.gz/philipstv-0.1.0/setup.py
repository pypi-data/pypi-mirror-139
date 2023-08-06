# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['philipstv', 'philipstv.model']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0', 'requests>=2.27.1,<3.0.0']

extras_require = \
{'cli': ['click>=8.0.3,<9.0.0', 'appdirs>=1.4.4,<2.0.0']}

entry_points = \
{'console_scripts': ['philipstv = philipstv.__main__:wrapped_cli']}

setup_kwargs = {
    'name': 'philipstv',
    'version': '0.1.0',
    'description': 'CLI and library to control Philips Android-powered TVs.',
    'long_description': '# philipstv\n\nPython CLI and library for controlling Philips Android-powered TV\'s.\n\nFeatures:\n- Get and set current TV power state.\n- Get and set current volume\n- List and change TV channels.\n- Emulate pressing remote keys.\n- Get and set ambilight power state.\n- Set ambilight RGB color.\n- List and launch applications.\n\n## Installation\nIf you plan to use the CLI:\n```shell\npip install \'philipstv[cli]\'\n```\n\nIf you only need a library for use in Python code:\n```shell\npip install philipstv\n```\n\n## CLI\n\n### Pairing\nFirst, you need to pair *philipstv* with your TV.\nFor this, you need to know its IP address.\nYou can find it in network settings.\n\nPairing is done using the following command:\n```shell\nphilipstv --host IP [--id ID] [--save] pair\n```\n\n- `--host` (required) specifies the TV IP address.\n- `--id` (optional) specifies the device ID to use during pairing.\n  This will be later used for authentication.\n  If not provided, the ID is generated randomly.\n- `--save` saves received credentials after successful pairing.\n  Use this if you don\'t want to provide credentials every time you run *philipstv*.\n\nAfter running `pair` command, you will be prompted to enter PIN number displayed on the TV\'s screen.\nThis completes the process and outputs your credentials.\n\nThe complete process should look like this:\n```\n$ philipstv --host 192.168.0.100 --save pair\nEnter PIN displayed on the TV: 5639\nPairing successful!\nID:     JMBsfOjJDYg5gxRG\nKey:    151080ea24e06ef4acc410a98398129e9de9edf43b1569ffb8249301945f5868\nCredentials saved.\n```\n\n### Usage\nOnce paired, use received credentials to authenticate. E.g.:\n```shell\nphilipstv --host 192.168.0.100 --id JMBsfOjJDYg5gxRG --key 151080ea24e06ef4acc410a98398129e9de9edf43b1569ffb8249301945f5868 power get\n```\nIf you used the `--save` option during pairing, this is just:\n```shell\nphilipstv power get\n```\nThe CLI is fully documented, so you can explore commands using `-h` option: `philipstv -h`, `philipstv power -h`, etc...\n\nExample usage session could look like this:\n```\n$ philipstv power set on\n$ philipstv volume set 15\n$ philipstv ambilight set on\n$ philipstv app list\nYouTube\nTED\nTwitch\nPrime Video\nNetflix\n$ philipstv launch Netflix\n$ philipstv key ok\n$ philipstv key play\n```\n\n## Library\nI really hope I will find strength to create proper documentation, for now those few examples + source code will have to be enough.\n\n### `PhilipsTVRemote`\nHigh level TV interaction interface.\nIt wraps API functionality into convenient and easy to use methods.\n\nPairing:\n```python\nfrom philipstv import PhilipsTVRemote\n\ndef pin_callback():\n    return str(input("Enter PIN: "))\n\nremote = PhilipsTVRemote.new("192.168.0.100")\nid, key = remote.pair(pin_callback)\n```\n\nUsage with credentials:\n```python\nfrom philipstv import InputKeyValue, PhilipsTVRemote\n\nremote = PhilipsTVRemote.new("192.168.0.100", ("<id>", "<key>"))\nremote.set_power(True)\ncurrent_volume = remote.get_volume()\nremote.set_volume(current_volume + 10)\nremote.set_ambilight_power(True)\nremote.launch_application("Netflix")\nremote.input_key(InputKeyValue.OK)\nremote.input_key(InputKeyValue.PLAY)\n```\n\n### `PhilipsTVAPI`\nLower level interface.\nEach method mirrors one request to one API endpoint.\nInput and output values have original shape, just like in API, but are wrapped in [`pydantic`](https://github.com/samuelcolvin/pydantic) models.\n\nPairing:\n```python\nfrom philipstv import DeviceInfo, PhilipsTV, PhilipsTVAPI, PhilipsTVPairer\n\napi = PhilipsTVAPI(PhilipsTV("192.168.0.100"))\ndevice_info = DeviceInfo(\n    id="<id>",\n    device_name="<name>",\n    device_os="<os>",\n    app_id="<id>",\n    app_name="<name>",\n    type="<type>",\n)\n\n\ndef pin_callback():\n    return str(input("Enter PIN: "))\n\nid, key = PhilipsTVPairer(api, device_info).pair(pin_callback)\n```\n\nAnd using with credentials:\n```python\nfrom philipstv import PhilipsTV, PhilipsTVAPI\nfrom philipstv.model import PowerState, PowerStateValue, Volume\n\napi = PhilipsTVAPI(PhilipsTV("192.168.0.100", auth=("<id>", "<key>")))\n\napi.set_powerstate(PowerState(powerstate=PowerStateValue.ON))\napi.set_volume(Volume(current=15, muted=False))\n```\n\n### `PhilipsTV`\nLowest level interface. Acts as a helper for sending authenticated requests to the TV.\n\nFor instance:\n```python\ntv = PhilipsTV("192.168.0.100", auth=("<id>", "<key>"))\nvolume_resp = tv.get("6/audio/volume")\nvolume = volume_resp["current"]\ntv.post("6/audio/volume", {"current": volume + 10})\n```\n\n## Resources\n- [Fantastic unofficial API documentation](https://github.com/eslavnov/pylips/blob/master/docs/Home.md) and [script](https://github.com/eslavnov/pylips) by [@eslavnov](https://github.com/eslavnov).\n- Philips [JointSpace API documentation](http://jointspace.sourceforge.net/projectdata/documentation/jasonApi/1/doc/API.html).\n',
    'author': 'Bazyli Cyran',
    'author_email': 'bazyli@cyran.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bcyran/philipstv',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
