#!/bin/bash

#xdg-open $( gsettings get org.cinnamon.desktop.background picture-uri | sed "s/^'file:\/\///g" | sed "s/'$//g")
#echo $( gsettings get org.cinnamon.desktop.background picture-uri | sed "s/^'file:\/\///g" | sed "s/'$//g")
URL=$( gsettings get org.cinnamon.desktop.background picture-uri | sed "s/^'file:\/\///g" | sed "s/'$//g")
echo ${URL}
xdg-open ${URL}
