#!/bin/sh

#external=HDMI1
#internal=eDP1
external=HDMI-0
internal=eDP-1-1

if [ $# -lt 2 ]  # we need at least 2 args
then
	if [ $# -eq 1 ]
	then
		case $1 in
			"off")
				echo "Turning extra screen off"
				# turn screen off
				xrandr --output $external --off
				xrandr --output $internal --pos 0x0
				# make the internal output the primary
				xrandr -- output $internal --primary
				exit 0
				;;
		esac
	fi

	echo "$0 right|left|top|off <resolution>"
	xrandr
	exit
fi

# TODO autodetect and use the higher res for screen?
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

case $3 in
	"")
		echo "with external screen as primary"
		echo "(for presentations, add 'presentation' to the command)"
		xrandr --output $external --primary
		;;
	"presentation")
		echo "with internal screen as primary (good for presentations)"
		xrandr --output $internal --primary
		;;
esac

# TODO use better xrandr commands to avoid errors
#xrandr --output VGA1 --mode 1024x768 --same-as LVDS1
#xrandr --output VGA1 --mode 1024x768 --right-of LVDS1
