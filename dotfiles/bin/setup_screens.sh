#!/bin/sh

if [ $# -ne 2 ]
then
	if [ $# -eq 1 ]
	then
		case $1 in
			"off")
				echo "Turning extra screen off"
				# turn screen off
				xrandr --output HDMI1 --off
				xrandr --output eDP1 --pos 0x0
				exit 0
				;;
		esac
	fi

	echo "$0 right|left|off [resolution]"
	xrandr
	exit
fi

resolution=$2

case $1 in
	"right")
		echo "setting to right"
		xrandr --output HDMI1 --mode $resolution --pos 1920x0
		;;
	"left")
		echo "setting to left"
		xrandr --output HDMI1 --mode $resolution --pos 0x0
		xrandr --output eDP1 --pos ${resolution%x*}x0
		;;
esac
