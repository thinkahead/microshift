# Node Red flows to show dashboard with sensor data
## Install the following in Manage palette
node-red-node-pi-sense-hat node-red-dashboard node-red-node-smooth

## References
https://github.com/mpolinowski/PiSenseHat-Node-RED
https://flows.nodered.org/node/node-red-node-pi-sense-hat
https://discourse.nodered.org/t/sensehat-environment-motion-problem/46851/22

## Dockerfile
The Docker file needs the following to make the node-red-node-pi-sense-hat work
```
ln -s /usr/lib/python3 /usr/lib/python2.7
ln -s /usr/bin/python3 /usr/lib/python
ln -s /usr/local/lib/python3.9/dist-packages/sense_hat-2.2.0-py3.9.egg/sense_hat /usr/lib/python2.7/dist-packages/sense_hat
```

## Flow 1
```
[
    {
        "id": "1257186b.0a2a38",
        "type": "change",
        "z": "cab5837e92764cde",
        "name": "temp",
        "rules": [
            {
                "t": "set",
                "p": "payload",
                "pt": "msg",
                "to": "payload.temperature",
                "tot": "msg"
            }
        ],
        "action": "",
        "property": "",
        "from": "",
        "to": "",
        "reg": false,
        "x": 415,
        "y": 112,
        "wires": [
            [
                "5286a46a.22574c"
            ]
        ]
    },
    {
        "id": "d818a011.6e4f6",
        "type": "switch",
        "z": "cab5837e92764cde",
        "name": "env",
        "property": "topic",
        "propertyType": "msg",
        "rules": [
            {
                "t": "eq",
                "v": "environment",
                "vt": "str"
            }
        ],
        "checkall": "true",
        "repair": false,
        "outputs": 1,
        "x": 295,
        "y": 139,
        "wires": [
            [
                "1257186b.0a2a38",
                "ebc9af3f.8eb3f",
                "6a598f88.a0418"
            ]
        ]
    },
    {
        "id": "ebc9af3f.8eb3f",
        "type": "change",
        "z": "cab5837e92764cde",
        "name": "hum",
        "rules": [
            {
                "t": "set",
                "p": "payload",
                "pt": "msg",
                "to": "payload.humidity",
                "tot": "msg"
            }
        ],
        "action": "",
        "property": "",
        "from": "",
        "to": "",
        "reg": false,
        "x": 416.5,
        "y": 179,
        "wires": [
            [
                "3f4ce8a5.02ef88"
            ]
        ]
    },
    {
        "id": "6a598f88.a0418",
        "type": "change",
        "z": "cab5837e92764cde",
        "name": "atm",
        "rules": [
            {
                "t": "set",
                "p": "payload",
                "pt": "msg",
                "to": "payload.pressure",
                "tot": "msg"
            }
        ],
        "action": "",
        "property": "",
        "from": "",
        "to": "",
        "reg": false,
        "x": 415.5,
        "y": 233,
        "wires": [
            [
                "dde55c07.3459a"
            ]
        ]
    },
    {
        "id": "9d96007b.fe3e6",
        "type": "comment",
        "z": "cab5837e92764cde",
        "name": "Environment Sensors",
        "info": "",
        "x": 200,
        "y": 96,
        "wires": []
    },
    {
        "id": "f51c664.1c4ff98",
        "type": "ui_gauge",
        "z": "cab5837e92764cde",
        "name": "Thermometer",
        "group": "f9412ecc.e353b",
        "order": 0,
        "width": 0,
        "height": 0,
        "gtype": "gage",
        "title": "Thermometer",
        "label": "°C",
        "format": "{{value}}",
        "min": 0,
        "max": "60",
        "colors": [
            "#00b500",
            "#e6e600",
            "#ca3838"
        ],
        "seg1": "",
        "seg2": "",
        "className": "",
        "x": 710,
        "y": 89,
        "wires": []
    },
    {
        "id": "6da57f94.3deb2",
        "type": "ui_gauge",
        "z": "cab5837e92764cde",
        "name": "Hygrometer",
        "group": "f9412ecc.e353b",
        "order": 0,
        "width": 0,
        "height": 0,
        "gtype": "gage",
        "title": "Hygrometer",
        "label": "%",
        "format": "{{value}}",
        "min": 0,
        "max": "100",
        "colors": [
            "#00b500",
            "#e6e600",
            "#ca3838"
        ],
        "seg1": "",
        "seg2": "",
        "className": "",
        "x": 702.5,
        "y": 179,
        "wires": []
    },
    {
        "id": "c24d86d8.1920a8",
        "type": "ui_gauge",
        "z": "cab5837e92764cde",
        "name": "Barometer",
        "group": "f9412ecc.e353b",
        "order": 0,
        "width": 0,
        "height": 0,
        "gtype": "gage",
        "title": "Barometer",
        "label": "mbar",
        "format": "{{value}}",
        "min": "900",
        "max": "1100",
        "colors": [
            "#00b500",
            "#e6e600",
            "#ca3838"
        ],
        "seg1": "",
        "seg2": "",
        "className": "",
        "x": 701.5,
        "y": 233,
        "wires": []
    },
    {
        "id": "10fe0e9f.a28511",
        "type": "ui_chart",
        "z": "cab5837e92764cde",
        "name": "Temperature Graph",
        "group": "398715c2.3c77ea",
        "order": 0,
        "width": 0,
        "height": 0,
        "label": "Temperature",
        "chartType": "line",
        "legend": "false",
        "xformat": "HH:mm:ss",
        "interpolate": "linear",
        "nodata": "",
        "dot": false,
        "ymin": "",
        "ymax": "",
        "removeOlder": "2",
        "removeOlderPoints": "",
        "removeOlderUnit": "3600",
        "cutout": 0,
        "useOneColor": false,
        "useUTC": false,
        "colors": [
            "#1f77b4",
            "#aec7e8",
            "#ff7f0e",
            "#2ca02c",
            "#98df8a",
            "#d62728",
            "#ff9896",
            "#9467bd",
            "#c5b0d5"
        ],
        "outputs": 1,
        "useDifferentColor": false,
        "className": "",
        "x": 721,
        "y": 136,
        "wires": [
            []
        ]
    },
    {
        "id": "5286a46a.22574c",
        "type": "smooth",
        "z": "cab5837e92764cde",
        "name": "",
        "property": "payload",
        "action": "mean",
        "count": "10",
        "round": "1",
        "mult": "single",
        "x": 547,
        "y": 112,
        "wires": [
            [
                "10fe0e9f.a28511",
                "f51c664.1c4ff98"
            ]
        ]
    },
    {
        "id": "3f4ce8a5.02ef88",
        "type": "smooth",
        "z": "cab5837e92764cde",
        "name": "",
        "property": "payload",
        "action": "mean",
        "count": "10",
        "round": "1",
        "mult": "single",
        "x": 546,
        "y": 179,
        "wires": [
            [
                "6da57f94.3deb2"
            ]
        ]
    },
    {
        "id": "dde55c07.3459a",
        "type": "smooth",
        "z": "cab5837e92764cde",
        "name": "",
        "property": "payload",
        "action": "mean",
        "count": "10",
        "round": "1",
        "mult": "single",
        "x": 544,
        "y": 233,
        "wires": [
            [
                "c24d86d8.1920a8"
            ]
        ]
    },
    {
        "id": "6c9089bd.427848",
        "type": "inject",
        "z": "cab5837e92764cde",
        "name": "",
        "repeat": "",
        "crontab": "",
        "once": false,
        "onceDelay": 0.1,
        "topic": "",
        "payload": "",
        "payloadType": "date",
        "x": 186,
        "y": 420,
        "wires": [
            [
                "a39867dd.a55e28",
                "2eb53772.695fa8"
            ]
        ]
    },
    {
        "id": "a39867dd.a55e28",
        "type": "change",
        "z": "cab5837e92764cde",
        "name": "Alarm",
        "rules": [
            {
                "t": "set",
                "p": "color",
                "pt": "msg",
                "to": "white",
                "tot": "str"
            },
            {
                "t": "set",
                "p": "background",
                "pt": "msg",
                "to": "red",
                "tot": "str"
            },
            {
                "t": "set",
                "p": "speed",
                "pt": "msg",
                "to": "5",
                "tot": "str"
            },
            {
                "t": "set",
                "p": "payload",
                "pt": "msg",
                "to": "Red",
                "tot": "str"
            }
        ],
        "action": "",
        "property": "",
        "from": "",
        "to": "",
        "reg": false,
        "x": 340,
        "y": 421,
        "wires": [
            [
                "9c79e9d9718199fc"
            ]
        ]
    },
    {
        "id": "8eddb3c4.10da5",
        "type": "change",
        "z": "cab5837e92764cde",
        "name": "deactivate",
        "rules": [
            {
                "t": "set",
                "p": "background",
                "pt": "msg",
                "to": "off",
                "tot": "str"
            },
            {
                "t": "set",
                "p": "payload",
                "pt": "msg",
                "to": "                  ",
                "tot": "str"
            }
        ],
        "action": "",
        "property": "",
        "from": "",
        "to": "",
        "reg": false,
        "x": 358,
        "y": 462,
        "wires": [
            [
                "9c79e9d9718199fc"
            ]
        ]
    },
    {
        "id": "2eb53772.695fa8",
        "type": "delay",
        "z": "cab5837e92764cde",
        "name": "",
        "pauseType": "delay",
        "timeout": "3",
        "timeoutUnits": "seconds",
        "rate": "1",
        "nbRateUnits": "1",
        "rateUnits": "second",
        "randomFirst": "1",
        "randomLast": "5",
        "randomUnits": "seconds",
        "drop": false,
        "outputs": 1,
        "x": 211,
        "y": 462,
        "wires": [
            [
                "8eddb3c4.10da5"
            ]
        ]
    },
    {
        "id": "d9461b8c.9107d8",
        "type": "comment",
        "z": "cab5837e92764cde",
        "name": "Dot Matrix",
        "info": "",
        "x": 160,
        "y": 380,
        "wires": []
    },
    {
        "id": "c1c718922692de96",
        "type": "rpi-sensehat in",
        "z": "cab5837e92764cde",
        "name": "",
        "motion": false,
        "env": false,
        "stick": false,
        "x": 150,
        "y": 140,
        "wires": [
            [
                "d818a011.6e4f6"
            ]
        ]
    },
    {
        "id": "9c79e9d9718199fc",
        "type": "rpi-sensehat out",
        "z": "cab5837e92764cde",
        "name": "",
        "x": 620,
        "y": 460,
        "wires": []
    },
    {
        "id": "f9412ecc.e353b",
        "type": "ui_group",
        "name": "Environment Control",
        "tab": "55925672.3514d8",
        "order": 1,
        "disp": true,
        "width": "7",
        "collapse": false
    },
    {
        "id": "398715c2.3c77ea",
        "type": "ui_group",
        "name": "Temperature Graph",
        "tab": "55925672.3514d8",
        "order": 2,
        "disp": true,
        "width": "10",
        "collapse": false
    },
    {
        "id": "55925672.3514d8",
        "type": "ui_tab",
        "name": "PiSenseHAT",
        "icon": "dashboard",
        "disabled": false,
        "hidden": false
    }
]
```

## Flow 2
```
[
    {
        "id": "2f1ce5a518f7038c",
        "type": "debug",
        "z": "0e34c6cf664c0b0f",
        "name": "",
        "active": false,
        "tosidebar": true,
        "console": false,
        "tostatus": false,
        "complete": "true",
        "targetType": "full",
        "statusVal": "",
        "statusType": "auto",
        "x": 490,
        "y": 320,
        "wires": []
    },
    {
        "id": "f79dfaa36cd93353",
        "type": "ui_text",
        "z": "0e34c6cf664c0b0f",
        "group": "47aa14e39a93548c",
        "order": 0,
        "width": 0,
        "height": 0,
        "name": "",
        "label": "Joystick direction",
        "format": "{{msg.payload.key}}",
        "layout": "row-spread",
        "className": "",
        "x": 530,
        "y": 160,
        "wires": []
    },
    {
        "id": "a94be90051639b30",
        "type": "switch",
        "z": "0e34c6cf664c0b0f",
        "name": "",
        "property": "topic",
        "propertyType": "msg",
        "rules": [
            {
                "t": "eq",
                "v": "joystick",
                "vt": "str"
            },
            {
                "t": "eq",
                "v": "environment",
                "vt": "str"
            },
            {
                "t": "eq",
                "v": "motion",
                "vt": "str"
            }
        ],
        "checkall": "true",
        "repair": false,
        "outputs": 3,
        "x": 290,
        "y": 240,
        "wires": [
            [
                "f79dfaa36cd93353"
            ],
            [
                "00565d90f8b06675",
                "a3fdd7a258d8506b",
                "1d8cadbb78ae0076"
            ],
            [
                "2f1ce5a518f7038c"
            ]
        ]
    },
    {
        "id": "cfc50256585fba98",
        "type": "ui_gauge",
        "z": "0e34c6cf664c0b0f",
        "name": "",
        "group": "47aa14e39a93548c",
        "order": 1,
        "width": 0,
        "height": 0,
        "gtype": "gage",
        "title": "temperature",
        "label": "units",
        "format": "{{value}}",
        "min": 0,
        "max": "60",
        "colors": [
            "#00b500",
            "#e6e600",
            "#ca3838"
        ],
        "seg1": "",
        "seg2": "",
        "className": "",
        "x": 790,
        "y": 200,
        "wires": []
    },
    {
        "id": "0cb4be89d2525e83",
        "type": "ui_gauge",
        "z": "0e34c6cf664c0b0f",
        "name": "",
        "group": "47aa14e39a93548c",
        "order": 2,
        "width": 0,
        "height": 0,
        "gtype": "gage",
        "title": "humidity",
        "label": "units",
        "format": "{{value}}",
        "min": 0,
        "max": "100",
        "colors": [
            "#00b500",
            "#e6e600",
            "#ca3838"
        ],
        "seg1": "",
        "seg2": "",
        "className": "",
        "x": 780,
        "y": 240,
        "wires": []
    },
    {
        "id": "ede3ec40fb37212d",
        "type": "ui_gauge",
        "z": "0e34c6cf664c0b0f",
        "name": "",
        "group": "47aa14e39a93548c",
        "order": 3,
        "width": 0,
        "height": 0,
        "gtype": "gage",
        "title": "pressure",
        "label": "units",
        "format": "{{value}}",
        "min": "900",
        "max": "1100",
        "colors": [
            "#00b500",
            "#e6e600",
            "#ca3838"
        ],
        "seg1": "",
        "seg2": "",
        "className": "",
        "x": 780,
        "y": 280,
        "wires": []
    },
    {
        "id": "00565d90f8b06675",
        "type": "change",
        "z": "0e34c6cf664c0b0f",
        "name": "temperature",
        "rules": [
            {
                "t": "move",
                "p": "payload.temperature",
                "pt": "msg",
                "to": "payload",
                "tot": "msg"
            }
        ],
        "action": "",
        "property": "",
        "from": "",
        "to": "",
        "reg": false,
        "x": 510,
        "y": 200,
        "wires": [
            [
                "cfc50256585fba98"
            ]
        ]
    },
    {
        "id": "a3fdd7a258d8506b",
        "type": "change",
        "z": "0e34c6cf664c0b0f",
        "name": "humidity",
        "rules": [
            {
                "t": "move",
                "p": "payload.humidity",
                "pt": "msg",
                "to": "payload",
                "tot": "msg"
            }
        ],
        "action": "",
        "property": "",
        "from": "",
        "to": "",
        "reg": false,
        "x": 500,
        "y": 240,
        "wires": [
            [
                "0cb4be89d2525e83"
            ]
        ]
    },
    {
        "id": "1d8cadbb78ae0076",
        "type": "change",
        "z": "0e34c6cf664c0b0f",
        "name": "pressure",
        "rules": [
            {
                "t": "move",
                "p": "payload.pressure",
                "pt": "msg",
                "to": "payload",
                "tot": "msg"
            }
        ],
        "action": "",
        "property": "",
        "from": "",
        "to": "",
        "reg": false,
        "x": 500,
        "y": 280,
        "wires": [
            [
                "ede3ec40fb37212d"
            ]
        ]
    },
    {
        "id": "2f281db51b977dbd",
        "type": "rpi-sensehat in",
        "z": "0e34c6cf664c0b0f",
        "name": "",
        "motion": true,
        "env": true,
        "stick": true,
        "x": 120,
        "y": 240,
        "wires": [
            [
                "a94be90051639b30",
                "566d6385f0d1d5ac"
            ]
        ]
    },
    {
        "id": "566d6385f0d1d5ac",
        "type": "debug",
        "z": "0e34c6cf664c0b0f",
        "name": "",
        "active": false,
        "tosidebar": true,
        "console": false,
        "tostatus": false,
        "complete": "true",
        "targetType": "full",
        "statusVal": "",
        "statusType": "auto",
        "x": 190,
        "y": 320,
        "wires": []
    },
    {
        "id": "47aa14e39a93548c",
        "type": "ui_group",
        "name": "Default",
        "tab": "4e80112e637d60e5",
        "order": 1,
        "disp": true,
        "width": "6",
        "collapse": false,
        "className": ""
    },
    {
        "id": "4e80112e637d60e5",
        "type": "ui_tab",
        "name": "Home",
        "icon": "dashboard",
        "order": 2,
        "disabled": false,
        "hidden": false
    }
]
```
