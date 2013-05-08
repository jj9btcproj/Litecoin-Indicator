rm litecoin-price-indicator.desktop
echo "[Desktop Entry]" >> litecoin-price-indicator.desktop
echo "Encoding=UTF-8 " >> litecoin-price-indicator.desktop
echo "Version=1.0" >> litecoin-price-indicator.desktop
echo "Name=Litecoin Market Price Indicator" >> litecoin-price-indicator.desktop
echo "Comment=Market price Indicator for litecoin" >> litecoin-price-indicator.desktop
echo "Exec=python /home/$(logname)/.local/share/applications/ltc-price-indicator.py" >> litecoin-price-indicator.desktop
echo "Icon=/home/$(logname)/.local/share/applications/litecoinicon.png" >> litecoin-price-indicator.desktop
echo "Categories=GNOME;Application;Network;" >> litecoin-price-indicator.desktop
echo "Type=Application" >> litecoin-price-indicator.desktop
echo "Terminal=false" >> litecoin-price-indicator.desktop
echo "X-Ayatana-Desktop-Shortcuts=Regular;" >> litecoin-price-indicator.desktop
echo "Name[en_US]=Litecoin Market Price Indicator" >> litecoin-price-indicator.desktop
