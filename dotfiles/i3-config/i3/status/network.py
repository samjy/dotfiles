#!/usr/bin/env python
# -*- coding: utf-8 -*-

from i3pystatus import network


class NetworkInfo(network.NetworkInfo):

    def extract_wireless_info(self, interface):
        """Parse nmcli result

        if basiciw doesn't work, we use nmcli
        nmcli -g general.device,general.type,general.state,general.connection device show <interface>
        """
        info = self.super.extract_wireless_info(interface)

        # Just return empty values if we're not using any Wifi functionality
        if not self.get_wifi_info:
            return info

        # TODO nmcli command, and parse properly

        info["essid"] = iwi["essid"]
        info["freq"] = iwi["freq"] / self.freq_divisor
        quality = iwi["quality"]
        if quality["quality_max"] > 0:
            info["quality"] = quality["quality"] / quality["quality_max"]
        else:
            info["quality"] = quality["quality"]
        info["quality"] *= 100
        info["quality_bar"] = make_bar(info["quality"])
        info["quality"] = round(info["quality"])

        return info


# TODO patch i3pystatus.network.NetworkInfo

# EOF
