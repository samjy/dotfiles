#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
import time
import json
from i3pystatus import IntervalModule
from i3pystatus.core.command import execute
from i3pystatus.core.util import TimeWrapper
import subprocess


class Chrono(object):
    """One of the stopwatches or timers displayed in the stopwatch area"""

    def __init__(
        self,
        name=None,
        paused_on=None,
        paused_duration=0,
        update_end_if_paused=False,
        stopwatch_start=None,
        timer_end=None,
        archived_on=None,
        archived_display=None,
        order=None,
    ):
        """Initialize"""
        self.name = name
        self.paused_on = paused_on
        self.paused_duration = paused_duration
        self.update_end_if_paused = update_end_if_paused
        self.stopwatch_start = stopwatch_start
        self.timer_end = timer_end
        self.archived_on = archived_on
        self.archived_display = archived_display
        self.order = order

    def as_dict(self):
        """Render as dict"""
        return {
            "name": self.name,
            "paused_on": self.paused_on,
            "paused_duration": self.paused_duration,
            "update_end_if_paused": self.update_end_if_paused,
            "stopwatch_start": self.stopwatch_start,
            "timer_end": self.timer_end,
            "archived_on": self.archived_on,
            "archived_display": self.archived_display,
            "order": self.order,
        }

    def displayed_duration(self, t=None):
        """Get displayed duration"""
        if not t:
            t = time.time()

        inpause = self.paused_duration
        if self.paused_on:
            inpause += t - self.paused_on

        if self.timer_end:
            # timer mode
            cur = self.timer_end - t
            if self.update_end_if_paused:
                # we paused the timer, but we keep the full duration
                cur += inpause

        else:
            # stopwatch mode
            cur = t - self.stopwatch_start - inpause

        return cur

    def display(self, fmt, t=None):
        """Display chrono"""
        return ":".join(
            filter(
                bool,
                [
                    self.name,
                    format(TimeWrapper(self.displayed_duration(t=t), fmt)),
                ],
            )
        )


class Stopwatch(IntervalModule):
    """Stopwatch module, to start one or more stopwatches

    Mouse actions
    - middle click: start new stopwatch
    - left click on one stopwatch: toggle pause on that stopwatch
    - right click on one stopwatch: remove that stopwatch
    - wheel up/down on one stopwatch: move right/left
    - double click on stopwatch: name the stopwatch
    """

    # TODO persist running stopwatches, so that they survive a reboot etc
    # TODO keep past stopwatches for possible reference

    NAME_CAPTION = "Name"
    interval = 0.1

    format = "%H:%M:%S"

    on_middleclick = "start"
    on_leftclick = "togglepause"
    on_rightclick = "finish"
    on_doubleleftclick = "rename"
    on_upscroll = ["scroll", "up"]
    on_downscroll = ["scroll", "down"]

    storage = "~/.i3/stopwatch.json"

    # TODO format

    def init(self):
        """Initialize"""
        self.storage_file = os.path.expanduser(self.storage)
        self.stopwatches = []
        self.extra = ""
        self.load()

    def load(self):
        """Get configured stopwatches from file"""
        try:
            with open(self.storage_file) as f:
                self.stopwatches = [Chrono(**data) for data in json.load(f) or []]
        except FileNotFoundError:
            return

    def dump(self):
        """Save stopwatches to file"""
        self._reindex()
        with open(self.storage_file, "w") as f:
            json.dump([c.as_dict() for c in self.stopwatches], f)

    def _reindex(self):
        """Reorganize stopwatches"""
        self.stopwatches = sorted(
            self.stopwatches,
            key=lambda x: (
                bool(x.archived_on),
                x.archived_on,
                x.order,
                -x.stopwatch_start,
            ),
        )

        # update orders of active stopwatches
        for order, chrono in enumerate(self.active_stopwatches):
            chrono.order = order

    @property
    def active_stopwatches(self):
        """Get stopwatches which are active"""
        return list(
            sorted(
                [chrono for chrono in self.stopwatches if not chrono.archived_on],
                key=lambda x: (x.order, -x.stopwatch_start),
            )
        )

    def run(self):
        """Run"""
        parts = []
        for chrono in self.active_stopwatches:
            parts.append("|" + chrono.display(self.format))

        self.output_parts = [""] + parts

        # TODO allow format
        self.output = {
            "full_text": "".join(self.output_parts),
            "color": "#ffffff",
            "urgent": False,
        }

    def start(self, modifiers):
        """Start stopwatch or timer depending on modifiers"""
        # TODO: new timer
        self.stopwatch_start()

    def stopwatch_start(self):
        """Start new timer"""
        self.stopwatches.append(
            Chrono(
                name="",
                stopwatch_start=time.time(),
                order=0,
            )
        )
        self.dump()

    def _get_hovered(self, width, relative_x):
        """Get hovered chrono"""
        w = len(self.output.get("full_text"))
        pos = int(w * relative_x / width)
        tot = len(self.output_parts[0])
        if pos < tot:
            return None

        for idx, part in enumerate(self.output_parts[1:]):
            tot += len(part)
            if tot >= pos:
                return self.active_stopwatches[idx]

    def togglepause(self, width=None, relative_x=None, modifiers=None):
        """Toggle pause for timer under mouse"""
        chrono = self._get_hovered(width, relative_x)
        if not chrono:
            return

        if chrono.paused_on:
            chrono.paused_duration += time.time() - chrono.paused_on
            chrono.paused_on = None
        else:
            chrono.paused_on = time.time()

        self.dump()

    def finish(self, width=None, relative_x=None, modifiers=None):
        """Finish clicked timer"""
        chrono = self._get_hovered(width, relative_x)
        if not chrono:
            return

        chrono.archived_on = time.time()
        chrono.archived_display = chrono.display(self.format)
        self.dump()

    def rename(self, width=None, relative_x=None, modifiers=None):
        """Rename"""
        chrono = self._get_hovered(width, relative_x)
        if not chrono:
            return

        name = (
            subprocess.check_output(
                [
                    "zenity",
                    "--entry",
                    "--text",
                    self.NAME_CAPTION,
                ]
            )
            .decode("utf-8")
            .strip()
        )
        chrono.name = name
        self.dump()

    def scroll(self, direction, width=None, relative_x=None, modifiers=None):
        """Move the item"""
        chrono = self._get_hovered(width, relative_x)
        if not chrono:
            return

        if direction == "up":
            chrono.order += 1.5

        elif direction == "down":
            chrono.order -= 1.5

        self.dump()


# EOF
