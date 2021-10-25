#!/usr/bin/bash
echo "Uninstalling"
sudo rm -rf /usr/lib/python3.10/site-packages/adwpydemo
sudo rm -rf /usr/share/adwpydemo/
sudo rm /usr/bin/adwpydemo 
echo "Rebuilding"
rm -rf _build/
meson --prefix /usr _build && cd _build
meson compile
echo "Installing"
sudo meson install
cd ..
/usr/bin/adwpydemo
