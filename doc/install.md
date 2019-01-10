# Installation of Backend Server on Debian/Ubuntu

## 1. Install RabbitMQ
1. Install RabbitMQ by following these instructions: https://www.rabbitmq.com/install-debian.html
2. Allow guest access from non-loopback interfaces: https://www.rabbitmq.com/access-control.html#loopback-users

## 2. Install Yarn
1. Install Yarn by following these instructions: https://yarnpkg.com/en/docs/install#debian-stable

## 3. Install dependencies
1. Run `python3 setup.py install`
2. Run `pip3 install git+https://github.com/takeshixx/knxmap.git`

## 4. Running
1. Use `run.sh`, the backend server is listening on `0.0.0.0:8080`

## 5. Autorun
1. Copy the autorun file to the correct destination `cp traffic-player/doc/autostart ~/.config/lxsession/LXDE-pi/autostart`
2. Edit crontab with `crontab -e`
3. Add these lines (it might be necessary to edit the script path):

```sh
PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/bin:/usr/local/sbin

@reboot cd /home/pi/traffic-player && python3.6 server.py
```

4. Make sure crontab service is enabled and running: `systemctl status cron.service`


# Installation of Traffic Player on Raspbian

## 1. Install dependencies
1. Run `pip3 install pika git+https://github.com/takeshixx/knxmap.git`
2. Follow the `agent` installation instructions nr. 1, 3 and 4

## 2. Running
1. The traffic-player can be run with `traffic-player/backend/player.py -p <player-id> -q <backend-ip> -d <knx-device-index>`

## 3. Autorun
1. Edit crontab with `crontab -e`
2. Add these lines (it might be necessary to edit the script path):

```sh
PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/bin:/usr/local/sbin

@reboot python3 /home/pi/traffic-player/player.py -q 192.168.0.10 -p 1 -d 0
@reboot python3 /home/pi/traffic-player/player.py -q 192.168.0.10 -p 2 -d 1
```

3. Make sure crontab service is enabled and running: `systemctl status cron.service`

