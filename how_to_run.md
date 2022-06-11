How to run on Ubuntu 20.04 (LTS) x64:

1. Update all packages: `$ sudo apt-get update && apt-get upgrade`
2. DB setup:
   1. Install postgres: `$ sudo apt install postgresql postgresql-contrib`
   2. Make sure postgres is running: `$ sudo systemctl start postgresql.service`
   3. Create user: `$ sudo -u postgres createuser <username>`
   4. Create db: `$ sudo -u postgres createdb <dbname>`
   5. Go into postgres console: `$ sudo -u postgres psql`
      1. Give new user a pw: `psql=# alter user <username> with encrypted password '<password>';`
      2. Grant new user all privileges on new db: `psql=# grant all privileges on database <dbname> to <username> ;`
      3. exit pg console: `psql=# exit`
3. Env vars:
   1. Set env vars: `$ sudo vim /etc/environment`
   2. Restart shell to load env vars: `$ exec bash`
4. Install files & dependencies:
   1. Clone the repo: `$ git clone https://github.com/luishauenstein/telegram-gas-alert`
   2. Install Pip: `$ apt install python3-pip` (not preinstalled on Digital Ocean Droplets)
   3. Install the development headers for postgres: `$ sudo apt install python3-dev libpq-dev` (will throw error when installing psycopg2 otherwise)
   4. Move into repo folder: `$ cd telegram-gas-alert/`
   5. Install dependencies: `$ pip install -r requirements.txt`
5. Use crontab to run _gas-alert-trigger.py_ every 30 seconds and _message-handler.py_ on startup:
   1. Open crontab: `$ crontab -e`
   2. Add following jobs to crontab:
      ```
          * * * * * python3 /root/telegram-gas-alert/src/gas_alert_trigger.py
          @reboot python3 /root/telegram-gas-alert/src/message_handler.py
      ```
6. Reboot: `$ sudo shutdown -r now`
