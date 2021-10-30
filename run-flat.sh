#!/usr/bin/bash

BUILDDIR=$HOME/tmp/.flatpak/repo
STATEDIR=$HOME/tmp/.flatpak/flatpak-builder
APPID=dk.rasmil.AdwPyDemo
APP_CONF=$APPID.yml
APPBIN=adwpydemo
mkdir -p $BUILDDIR

flatpak-builder --force-clean --state-dir=$STATEDIR $BUILDDIR $APP_CONF
flatpak-builder --run $BUILDDIR $APP_CONF $APPBIN
