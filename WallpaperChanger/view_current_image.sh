#!/bin/bash

xdg-open $( gsettings get org.cinnamon.desktop.background picture-uri | sed "s/^'file:\/\///g" | sed "s/'$//g")
