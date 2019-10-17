#!/bin/sh

#external=HDMI1
#internal=eDP1
external=HDMI-0
internal=eDP-1-1

if [ $# -ne 2 ]
then
	if [ $# -eq 1 ]
	then
		case $1 in
			"off")
				echo "Turning extra screen off"
				# turn screen off
				xrandr --output $external --off
				xrandr --output $internal --pos 0x0
				exit 0
				;;
		esac
	fi

	echo "$0 right|left|top|off [resolution]"
	xrandr
	exit
fi

resolution=$2

case $1 in
	"right")
		echo "setting to right"
		xrandr --output $external --mode $resolution --pos 1920x0
		;;
	"left")
		echo "setting to left"
		xrandr --output $external --mode $resolution --rotate normal --pos 0x0
		xrandr --output $internal --pos ${resolution%x*}x0
		;;
	"leftvert")
		echo "setting to left vertical"
		xrandr --output $external --rotate right --mode $resolution --pos 0x0
		xrandr --output $internal --pos ${resolution##*x}x0
		;;
	"top")
		echo "setting to top"
		xrandr --output $external --mode $resolution --pos 0x0
		xrandr --output $internal --pos 0x${resolution##*x}
		;;
esac
