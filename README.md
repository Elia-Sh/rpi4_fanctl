
Example of setting argon40 fan to 100%:
```
/usr/sbin/i2cset -y 1 0x01a 0x64
```

py util usage:
```
git clone
cd <cloned dir>

# switch to root user - required by i2ctools
su

python rpi4_fanctl.py
```



reference -
https://github.com/nemozny/argonone-debian-64
https://github.com/spapadim/argon1
https://gitlab.com/DarkElvenAngel/argononed
https://wiki.archlinux.org/title/I2C




Unrelated ->
watchdog disable ->
1. kernel param
2. https://wiki.archlinux.org/title/Power_management#Disabling_NMI_watchdog
