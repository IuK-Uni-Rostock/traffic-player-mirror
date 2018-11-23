# Installation of Backend Server

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

# Installation of Traffic Player

## 1. Install dependencies
1. Run `pip3 install pika`
2. Follow the `agent` installation instructions nr. 1, 3 and 4

## 2. Running
1. The traffic-player can be run with `traffic-player/backend/player.py -p <player-id> -q <backend-ip>`

