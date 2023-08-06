# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['knoepfe', 'knoepfe.widgets', 'knoepfe.widgets.obs']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.1,<10.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'docopt>=0.6.2,<0.7.0',
 'obs-websocket-py>=0.5.3,<0.6.0',
 'pulsectl-asyncio>=0.2.0,<0.3.0',
 'pytest-cov>=3.0.0,<4.0.0',
 'schema>=0.7.5,<0.8.0',
 'streamdeck>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['knoepfe = knoepfe.__main__:main']}

setup_kwargs = {
    'name': 'knoepfe',
    'version': '0.1.0',
    'description': 'Connect and control Elgato Stream Decks',
    'long_description': '# Knöpfe <sub><sup>[ˈknœpfə]</sub></sup>\n\nConnect and control Elgato Stream Decks from Linux.\n\n## Features\n\n- Several integrated widgets\n- OBS integration including\n    - Showing and changing if stream is running\n    - Showing and changing if recording is running\n    - Showing current scene\n    - Switching between scenes\n- Multiple pages to switch between\n- Configuring device\'s brightness and hardware polling interval\n- Automatic sleeping if device isn\'t used with the possibility for widgets to prevent this (i.e. while OBS is running)\n\n## Installation\n\n### PyPI\n\n    pip install knoepfe\n\nshould do the trick :)\n\n### Prerequisites\n\nudev rules are required for Knöpfe to be able to communicate with the device.\n\nCreate ` /etc/udev/rules.d/99-streamdeck.rules` with following content:\n\n    SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0060", TAG+="uaccess"\n    SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="006d", TAG+="uaccess"\n    SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0080", TAG+="uaccess"\n    SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="0063", TAG+="uaccess"\n    SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", ATTRS{idProduct}=="006c", TAG+="uaccess"\n\nThen, run `sudo udevadm control --reload-rules` and reconnect the device. You should be ready to go then.\n\n## systemd unit\n\nIf you want to start Knöpfe automatically on user login, consider creating and enabling a systemd unit in `~/.config/systemd/user/knoepfe.service`:\n\n    [Unit]\n    Description=Knoepfe\n\n    [Service]\n    # Set path to where Knoepfe executable was installed to\n    ExecStart=/usr/local/bin/knoepfe\n    Restart=always\n\n    [Install]\n    WantedBy=default.target\n\nAnd start and enable it by running:\n\n    systemd --user enable knoepfe\n    systemd --user start knoepfe\n\n## Usage\n\n### Starting\n\nUsually just running `knoepfe` should be enough. It reads the configuration from `~/.config/knoepfe/knoepfe.cfg` (see below for more information) and connects to the stream deck.\n\nAnyway, some command line options are available:\n\n    knopfe\n    Connect and control Elgato Stream Decks\n\n    Usage:\n      knoepfe [(-v | --verbose)] [--config=<path>]\n      knoepfe (-h | --help)\n      knoepfe --version\n\n    Options:\n      -h --help       Show this screen.\n      -v --verbose    Print debug information.\n      --config=<path> Config file to use.\n\n\n### Configuration\n\nUnless overwritten on command line, Knöpfe loads its configuration from `~/.config/knoepfe/knoepfe.cfg`. So you should create that file if you don\'t want to stick to the example config used as fallback.\n\nAnyway, the example is a great way to start. It can be found as `knoepfe/default.cfg` in this repository and the installation target directory.\n\nThe configuration is parsed as Python code. So every valid Python statement can be used, allowing to dynamically create and reuse parts of it.\nThe default configuration is heavily commented, hopefully explaining how to use it clear enough.\n\n## Widgets\n\nFollowing widgets are included:\n\n### Text\n\nSimple widget just displaying a text.\n\nCan be instantiated as:\n\n    widget({\'type\': \'knoepfe.widgets.Text\', \'text\': \'My great text!\'})\n\nDoes nothing but showing the text specified with `text` on the key.\n\n### Clock\n\nWidget displaying the current time. Instantiated as:\n\n    widget({\'type\': \'knoepfe.widgets.Clock\', \'format\': \'%H:%M\'})\n\n`format` expects a [strftime() format code](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes) to define the formatting.\n\n### Timer\n\nStop watch widget.\n\nInstantiated as:\n\n    widget({\'type\': \'knoepfe.widgets.Timer\'})\n\nWhen pressed it counts the seconds until it is pressed again. It then shows the time elapsed between both presses until pressed again to reset.\n\nThis widget acquires the wake lock while the time is running, preventing the device from going to sleep.\n\n### Mic Mute\n\nMute/unmute PulseAudio source, i.e. microphone.\n\nInstantiated with:\n\n    widget({\'type\': \'knoepfe.widgets.MicMute\'})\n\nAccepts `device` as optional argument with the name of source the operate with. If not set, the default source is used.\nThis widget shows if the source is muted and toggles the state on pressing it.\n\n### OBS Streaming and Recording\n\nShow and toggle OBS streaming/recording.\n\nThese widgets can be instantiated with\n\n    widget({\'type\': \'knoepfe.widgets.obs.Recording\'})\n\nand\n\n    widget({\'type\': \'knoepfe.widgets.obs.Streaming\'})\n\nThey connect to OBS (if running, they\'re quite gray if not) and show if the stream or recording is running. On a long press the state is toggled.\n\nAs long as the connection to OBS is established these widgest hold the wake lock.\n\n### OBS Current Scene and Scene Switch\n\nShow and switch active OBS scene.\n\nThese widgets are instantiated with\n\n    widget({\'type\': \'knoepfe.widgets.obs.CurrentScene\'})\n\nand\n\n    widget({\'type\': \'knoepfe.widgets.obs.SwitchScene\', \'scene\': \'Scene\'})\n\nThe current scene widget just displays the active OBS scene.\n\nThe scene switch widget indicates if the scene set with the `scene` key is currently active. If not and the widget is pressed it switches to the scene.\n\nAs long as the connection to OBS is established these widgets hold the wake lock.\n\n## Development\n\nPlease feel free to open an [issue](https://github.com/lnqs/knoepfe/issues) if you encounter any bugs.\n\nPull requests are also very welcome :)\n\nAs widgets are loaded by their module path it should also be possible to add new functionality in a plugin-ish way by just creating independent python modules defining their behaviour. But, well, I haven\'t tested that yet.\n\n## Mentions\n\nThis project relies on [python-elgato-streamdeck](https://github.com/abcminiuser/python-elgato-streamdeck) to communicate with the devices and is heavily inspired by [Dev Deck](https://github.com/jamesridgway/devdeck) and [deckmaster](https://github.com/muesli/deckmaster/).\n',
    'author': 'Simon Hayessen',
    'author_email': 'simon@lnqs.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lnqs/knoepfe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
