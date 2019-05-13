# Installation of Backend Server on Debian/Ubuntu

## 1. Install RabbitMQ
1. Install RabbitMQ by following these instructions: https://www.rabbitmq.com/install-debian.html
2. Allow guest access from non-loopback interfaces: https://www.rabbitmq.com/access-control.html#loopback-users

## 2. Install Yarn
1. Install Yarn by following these instructions: https://yarnpkg.com/en/docs/install#debian-stable

## 3. Install dependencies
1. Run `sudo apt install python3-pip python3-venv`

## 4. Running
1. Execute `run-server.sh` to start the backend server, by default it's listening on `0.0.0.0:8080` and accessible by any modern web browser

## 5. Autorun
1. Edit crontab with `crontab -e`
2. Add these lines (it might be necessary to edit the script path):

```sh
PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/bin:/usr/local/sbin

@reboot ./home/pi/traffic-player/run-server.sh
```

3. Make sure crontab service is enabled and running: `systemctl status cron.service`
4. (optional) Automatically start Chromium on boot: `sudo echo "@chromium-browser --incognito --kiosk http://127.0.0.1:8080/" >> /etc/xdg/lxsession/LXDE-pi/autostart`

# Installation of Traffic Player on Raspbian

## 1. Install dependencies
1. Run `sudo apt install python3-pip python3-venv`
2. Follow the `agent` installation instructions nr. 1, 3 and 4

## 2. Running
1. Execute `run-player.sh -p <player-id> -q <backend-ip> -d <knx-device-index>` to start the traffic player

## 3. Autorun
1. Copy the service files to the correct directory `cp traffic-player/doc/player* ~/.config/systemd/user` (it might be necessary to create the directory first)
2. Reload systemd `systemctl --user daemon-reload`
3. Enable the services `systemctl --user enable player1.service` and `systemctl --user enable player2.service`
4. Reboot `sudo reboot now`
