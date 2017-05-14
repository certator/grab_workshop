1. run `docker-compose build` to build image


2. meanwhile, create `.env` file with following contents:

```
DEV_LOOPBACK_IP=123.123.123.123
```

instead of 123.123.123.123 could be any IP

3. run `./add-loopback-ip.sh`, it will attach DEV_LOOPBACK_IP to loopback interface

4. after step 1, run `docker-compose up -d` to run container

5. now you can configure PyCharm remote SSH interpreter with DEV_LOOPBACK_IP and container_ssh_key.priv as key pair