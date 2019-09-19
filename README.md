# SWAN (Sway Workspace AutoNamer)

> SWAN uses the python i3ipc module to dynamically rename workspaces using FontAwesome icons or customized text to visually identify open applications.


**Current features**

- Dynamically rename workspace
- Empty workspace support
- Move workspace support
- Both Wayland and XWayland apps support
- Customizable icons or text
- Graceful exit


**Configuration**

Open swan.py and add/edit the dictionary "APP_ICONS" containing app_id and related icons/text.

As keys use the app_id value you can get by running the following command:

```bash
swaymsg -t get_tree | grep app_id
```

As values use character codes, text or whatever you want to use as workspace name for the selected app. I use character codes from https://fontawesome.com/icons


**How to use**

Copy swan.py in a folder (e.g.: ~/.config/sway/scripts) and add the following line to your sway config:

```
exec "$HOME/.config/sway/scripts/swan.py
```


**Dependencies**


```
python-i3ipc>=2.0.1 (i3ipc-python)
```



Contributions are welcome! - Have fun :)


## License

SWAN is licensed under the GPL3 license. [See LICENSE for more information](https://github.com/fnoris/swan/blob/master/README.md).


