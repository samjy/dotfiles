#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from i3pystatus import Status
import netifaces

# View doc at https://i3pystatus.readthedocs.io/en/latest/index.html

status = Status(logfile="$HOME/.i3/i3pystatus.log")

# clock
status.register(
    "clock",
    format="%Y-%m-%d <b>%H:%M:%S</b>",
    hints={"markup": "pango"},
    interval=1,
)

status.register(
    "moon",
    format="{moonicon}",
)

# Shows pulseaudio default sink volume
#
# Note: requires libpulseaudio from PyPI
status.register(
    "pulseaudio",
    format="{volume_bar} {volume}",
    # format=" {volume}",
    # format = " %volume"  # fa-volume-up
    # format='{volume_bar}',
    # format_muted = " (%volume)"  # fa-volume-off
    sink="alsa_output.pci-0000_00_1f.3.analog-stereo",
    # color_unmuted='#00aa00',
    color_muted="#dd0000",
    # format_muted=" muted",
    format_muted=" muted",  # fa-volume-off
    vertical_bar_width=1,
    vertical_bar_glyphs=["  ", " ", ""],
)

# status.register(
#    "backlight",
#    format=" {percentage:.0f}%",
# )

# Shows the average load of the last minute and the last 5 minutes
# (the default value for format is used)
status.register(
    "load",
    format="load:{avg1}",
    critical_limit=2,
)

# Shows your CPU temperature, if you have a Intel CPU
status.register(
    "temp",
    format="cpu°:{temp:.0f}°C",
)

# CPU usage
status.register(
    "cpu_usage",
    format="cpu:{usage:02}%",
)

## GPU usage
# status.register(
#    "gpu_usage",
#    format="gpu:{usage:02}%",
#    color="#ffffff",
# )

# RAM usage
status.register(
    "mem",
    format="ram:{percent_used_mem}%",
    warn_percentage=75,
    alert_percentage=90,
    color="#ffffff",
    warn_color="#aaaa00",
    alert_color="#dd0000",
)

# Shows disk usage of /
status.register(
    "disk",
    path="/",
    format="/:{percentage_used}%",
    round_size=1,
    # TODO use percentage_used_of_available
    # TODO critical_limit
)

# screen blanking control
status.register(
    "dpms",
)

# Battery
status.register(
    "battery",
    format="{status} {percentage:.2f}% {remaining:%E%hh:%Mm}",
    alert=True,
    alert_percentage=15,
    status={
        "DIS": " ",  # fa-battery-half
        "CHR": " ",  # fa-plug
        "FULL": " ",  # fa-battery-full
    },
    # TODO change displayed battery picto on charge level
    full_color="#00aa00",
    charging_color="#00aa00",
    critical_color="#dd0000",
)

# Battery
# status.register(
# "battery",
# format="{status} {remaining:%E%hh:%Mm}",
# alert=True,
# alert_percentage=5,
# status={
# "DIS":  "Discharging",
# "CHR":  "Charging",
# "FULL": "Bat full",
# },
# )

## Displays whether a DHCP client is running
# status.register(
#    "runwatch",
#    name="DHCP",
#    path="/var/run/dhclient*.pid",
# )

for ifc in sorted(netifaces.interfaces()):
    if ifc == "lo":
        continue

    status.register(
        "network",
        interface=ifc,
        format_up=(
            "{interface}:({essid} {quality:03.0f}%) {v4cidr}"
            if ifc.startswith("w")  # likely to be wifi
            else "{interface}:{v4cidr}"
            # "{interface}:{v4cidr}"
        ),
        format_down="{interface}:down",
        color_up="#00aa00",
        color_down="#dd0000",
        on_upscroll=None,
        on_downscroll=None,
        on_rightclick=None,
    )

# TODO
# status.register("openvpn")

status.register("online")

# TODO
# status.register(
#    'pagerduty',
#    api_key='',
#    user_id=''
# )

## watch running makes
# status.register(
#    "makewatch",
# )

status.register(
    "timer",
    color="#00aa00",
    format_custom=[
        (0, "+%M:%S", "#ffffff"),
        (60, "-%M:%S", "#ffa500"),
        (3600, "-%M:%S", "#00aa00"),
    ],
    on_overflow="notify-send -u critical -t 5000 -- 'Time out!'",
)

from stopwatch import Stopwatch

status.register(
    Stopwatch,
)

status.register(
    "anybar",
)

## Shows mpd status
## Format:
## Cloud connected▶Reroute to Remain
# status.register("mpd",
#    format="{title}{status}{album}",
#    status={
#        "pause": "▷",
#        "play": "▶",
#        "stop": "◾",
#    },)

status.run()


# EOF
