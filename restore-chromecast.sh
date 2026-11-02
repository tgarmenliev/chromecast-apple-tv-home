#!/bin/zsh
# Връща стария Google TV лаунчър и всичко изключено. Ползване: ./restore-chromecast.sh <tv ip>:<основен порт>
A=$HOME/Library/Android/sdk/platform-tools/adb
T=${1:?дай IP:порт на Wireless debugging}
$A connect $T
for p in com.google.android.apps.tv.launcherx com.google.android.tungsten.setupwraith \
  com.google.android.play.games com.google.android.tv.remotecontrol.logging \
  com.google.android.feedback com.android.tv.feedbackconsent; do
  $A -s $T shell pm enable --user 0 $p
done
$A -s $T shell settings put global private_dns_mode opportunistic
$A -s $T shell pm uninstall com.gathin.tvhome
echo "Готово. Натисни Home."
