#!/bin/bash

echo "mkdir -p ~/bin/"
mkdir -p ~/bin/
echo "mkdir -p ~/.vimswap/"
mkdir -p ~/.vimswap/

if [ ! -f ~/.gtkrc-2.0 ]
then
	echo 'echo "include \"$HOME/.gtkrc-2.0.mine\"" > ~/.gtkrc-2.0'
	echo "include \"$HOME/.gtkrc-2.0.mine\"" > ~/.gtkrc-2.0
fi
