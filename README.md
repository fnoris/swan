# SWAN (Sway Workspace AutoNamer)

> SWAN uses the python i3ipc module to dynamically rename workspaces using FontAwesome icons or customized text to visually identify open applications.


**Current features**

- Dynamically rename workspace
- Empty workspace support
- Move workspace support
- Both Wayland and XWayland apps support
- Customizable icons or text
- Config file
- Graceful exit


**Configuration**

Swan loads its configuration from $HOME/.config/swan.conf. If the file doesn't exist, a default configuration file is created at first run.

The configuration file consists of sections each led by a [section] header, followed by key/value entries (similar to what's found in Microsoft Windows INI files).

There are three section supported:

```
[DEFAULT] contains default configurations, like predefined icon, debug mode, etc.
[icons] contains the actual icons to use
[applications] contains a list of application names and icons to use
```

Application name is the value of 'app_id' (Wayland apps) or 'class' (XWayland apps) you can get by running the following command:

```bash
swaymsg -t get_tree | grep "app_id\|class"

or

xprop
```


**How to use**

Copy swan.py in a folder (e.g.: ~/.config/sway/scripts) and add the following line to your sway config:

```
exec "$HOME/.config/sway/scripts/swan.py
```

It's allowed to put icon/text directly as value of application variables, I suggest to use interpolation instead. The syntax is ${SECTION:VARIABLE}, e.g.:
```
[icons]
APP_ICON = 

[applications]
APP_NAME = ${icons:APP_ICON}
```

**Dependencies**


```
python-i3ipc>=2.0.1 (i3ipc-python)
```



Contributions are welcome! - Have fun :)


## License

SWAN is licensed under the GPL3 license. [See LICENSE for more information](https://github.com/fnoris/swan/blob/master/README.md).


