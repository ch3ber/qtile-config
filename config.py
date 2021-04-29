#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
    Key([mod], "space", lazy.layout.next()),

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
    Key([mod], "m", lazy.spawn("dmenu_run")),
    #exec firefox
    Key([mod], "b", lazy.spawn("org.mozilla.firefox"))
]

groups = [Group(i) for i in "1234567890"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

layouts = [
    layout.Columns(border_focus_stack='#d75f5f'),
    layout.Max(),
    layout.Stack(num_stacks=2),
    layout.Zoomy(),
    layout.Matrix(),
]

widget_defaults = dict(
    font='RobotoMono Nerd Font',
    fontsize=14,
    padding=0,
)

extension_defaults = widget_defaults.copy()

screens = [Screen(top=bar.Bar(
    [
        widget.GroupBox(padding=10, background="#001A1A", borderwidth=0, active="#ffffff", inactive="#4C4D4F", highlight_method='block', this_current_screen_border="#005959", this_screen_border="#0F3333"),
        widget.TextBox(text='',  foreground="#001A1A", fontsize=21),
        widget.Prompt(),
        widget.WindowName(foreground="#00ffff"),
        #widget.Chord(
        #    chords_colors={
        #        'launch': ("#1d1d1d", "#e1e1e1"),
        #    },
        #    name_transform=lambda name: name.upper(),
        #),
        widget.TextBox(text='',  foreground="#00A6A6", fontsize=21),
        widget.CurrentLayout(background="#00A6A6", foreground="#1d1d1d"),
        widget.TextBox(text='',  foreground="#005959", background="#00A6A6", fontsize=21),
        widget.Clock(format='  %a %d  %H:%M', background="#005959", foreground="#ffffff"),
        widget.TextBox(text='',  foreground="#0F3333", background="#005959", fontsize=21),
        widget.CurrentLayout(background="#0F3333", foreground="#ffffff"),

            ],22,background='#001212',margin=0,opacity=1,),),]

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

#set wallpaper
os.system("feh -z --bg-fill ~/Images/wallpapers/")
#enable trasparenci
os.system("compton &")
