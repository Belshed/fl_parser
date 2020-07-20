# Установка с нуля

Выполнить в консоле сервера при первом включении:
```
apt update
apt install -y htop git build-essential libssl-dev libffi-dev python3-pip python3-dev python3-setuptools python3-venv 
```

Создать пользователя:
```
adduser serge
```

Переключиться на нового пользователя:
```
whoami
su - serge
whoami
```

Клонировать репозиторий:
```
cd /home/serge
git clone https://github.com/Belshed/РЕПОЗИТОРИЙ
```

Создать вирутальное окружение:
```
cd /home/serge/ПАПКА С БОТОМ
python3 -m venv .venv
```

Активировать вирутальное окружение и установить пакеты:
```
source /home/serge/ПАПКА С БОТОМ/.venv/bin/activate
pip install -r /home/serge/ПАПКА С БОТОМ/pip-requirements.txt
```

Проверить что бот работает (из виртуального окружения):
```
/home/serge/ПАПКА С БОТОМ/.venv/bin/python /home/serge/ПАПКА С БОТОМ/main.py
```

Использовать конфиг для автоматического запуска "tgbot.service"

Прописать в нём своего пользователя, пути и положить его в папку (из-под root):
```
sudo cp /home/serge/ПАПКА С БОТОМ/tgbot.service /etc/systemd/system/tgbot.service
```

Запустить бота:
```
sudo systemctl start tgbot
sudo systemctl enable tgbot
```

Проверить как дела:
```
sudo systemctl status tgbot
```


# Обновление кода

Скачать свежий код из репозитория:
```
cd /home/serge/ПАПКА С БОТОМ
git fetch && git checkout -f origin/master 
```

Перезапустить бота:
```
sudo systemctl start tgbot
```

Остановить бота:
```
sudo systemctl stop tgbot
```
