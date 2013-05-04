#!/bin/bash
# This script will test if you have given a leap year or not.

if grep -q ltc-indicator= ~/.bashrc; then
    echo "Already registered in bashrc"
    exit 1
fi
echo " " >> ~/.bashrc
echo "#" >> ~/.bashrc
echo "#     LTC-Indicator" >> ~/.bashrc
echo "#" >> ~/.bashrc
echo "alias ltc-indicator='python ~/.local/share/applications/ltc-price-indicator.py'" >> ~/.bashrc


