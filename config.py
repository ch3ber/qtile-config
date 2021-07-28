# -*- coding: utf-8 -*-

from typing import List  # noqa: F401

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

import os

mod = "mod4"
terminal = guess_terminal("alacritty")

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod, "control"], "n", lazy.layout.next()),

    # Move windows
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),

    #resize windows
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),

    #reset all window sizes
    Key([mod], "n", lazy.layout.normalize()),
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
    #Toggle between layouts
    Key([mod], "Tab", lazy.next_layout()),

    #kill focused window
    Key([mod, "mod1"], "k", lazy.window.kill(), desc="Kill focused window"),
    #restart Qtile config
    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    #exit the Qtile
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    #launch terminal
    Key([mod], "Return", lazy.spawn(terminal)),
    #run command
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    #exec dmenu
    Key([mod, "shift"], "m", lazy.spawn("dmenu_run")),
    #exec rofi
    Key([mod], "m", lazy.spawn("rofi -show drun")),
    #exec firefox
    Key([mod], "b", lazy.spawn("firefox")),
    #exec firefox developer edition
    Key([mod, "shift"], "b", lazy.spawn("firefox-developer-edition")),
    #take a screen capture
    Key([mod], "s", lazy.spawn("scrot -e 'mv $f ~/ss/'")),
    #take a screen capture select
    Key([mod, "shift"], "s", lazy.spawn("scrot -q 100 -s -f -e 'mv $f ~/ss/'")),
    #take a screen capture focused
    Key([mod, "control"], "s", lazy.spawn("scrot -u -e 'mv $f ~/ss/'")),
    #open explorer file
    Key([mod], "e", lazy.spawn("nautilus"))
]

group_names = [(" HOME", {'layout': 'columns'}),
               (" WEB", {'layout': 'max'}),
               ("3", {'layout': 'columns'}),
               ("4", {'layout': 'columns'}),
               ("5", {'layout': 'columns'}),
               ("6", {'layout': 'columns'}),
               ("ﭮ", {'layout': 'columns'}),
               ("祥", {'layout': 'matrix'}),
               ("", {'layout': 'columns'})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group

layouts = [
    layout.Columns(border_focus_stack='#005d5d'),
    layout.Max(),
    layout.Zoomy(),
    layout.Matrix()
]

widget_defaults = dict(
    font='RobotoMono Nerd Font',
    fontsize=14,
    padding=0,
)

extension_defaults = widget_defaults.copy()

screens = [Screen(top=bar.Bar(
    [
        widget.TextBox(text='  ',  foreground="#7AA2F7", fontsize=21),
        widget.GroupBox(padding=10, borderwidth=0, active="#1a1b26", inactive="#444B6A", highlight_method='text', this_current_screen_border="#ffffff", background="#7AA2F7"),
        widget.TextBox(text='  ',  foreground="#7AA2F7", fontsize=21),
        widget.Prompt(),
        widget.WindowName(foreground="#b9f27c"),
        widget.TextBox(text='',  foreground="#3b3d57", fontsize=21),
        widget.CurrentLayout(background="#3b3d57", foreground="#ffffff"),
        widget.TextBox(text='',  foreground="#444B6A", background="#3b3d57", fontsize=21),
        widget.TextBox(text=' ',  background="#444B6A", fontsize=18),
        widget.Net(background="#444B6A", foreground="#ffffff", use_bits='False'),
        widget.TextBox(text='',  foreground="#7AA2F7", background="#444B6A", fontsize=21),
        widget.Clock(format='  %a %d %m  %H:%M ', background="#7AA2F7", foreground="#24283b"),

    ],22,background='#06080a',margin=0,opacity=1,),),]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

#set wallpaper of https://www.github.com/chEber405/wallpapers
os.system("feh -z --bg-fill ~/Pictures/wallpapers/**")
#enable trasparenci
os.system("compton &")
#enable two layout
os.system("setxkbmap -layout us,es -option grp:win_space_toggle")
