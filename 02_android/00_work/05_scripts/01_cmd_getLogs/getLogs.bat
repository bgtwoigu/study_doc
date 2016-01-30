@echo off
CURRENT_DIR=%~sdp0
set ADB_CMD=%CURRENT_DIR%adb.exe

Set nowtime=%time:~,8%
Set nowdate=%date:~,10%
Set LOG_DIR=Logs_%nowdate:/=%_%nowtime::=%

md %LOG_DIR%
%ADB_CMD% remount
::%ADB_CMD% pull /data/data/com.android.providers.settings/databases ./%LOG_DIR%/databases
::%ADB_CMD% pull /data/data/com.android.providers.media/databases ./%LOG_DIR%/databases
%ADB_CMD% pull /data/tombstones ./%LOG_DIR%
%ADB_CMD% shell cat /proc/cmdline > ./%LOG_DIR%/cmdline
%ADB_CMD% shell cat /proc/meminfo > ./%LOG_DIR%/meminfo
%ADB_CMD% shell top -t -n 1 > ./%LOG_DIR%/top.txt
%ADB_CMD% shell /system/bin/screencap -p /storage/sdcard0/screenshot.png
%ADB_CMD% pull /storage/sdcard0/screenshot.png ./%LOG_DIR%
%ADB_CMD%  bugreport > ./%LOG_DIR%/bugreport.txt


pause

