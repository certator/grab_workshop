FROM ubuntu:16.04

# Python part

RUN apt-get -yqq update
RUN apt-get install -yqq python-pip
RUN apt-get install -yqq libcurl4-openssl-dev
RUN apt-get install -yqq libpq-dev python-dev

# SSH part

RUN apt-get update -yqq && apt-get install -yqq openssh-server net-tools

RUN mkdir /var/run/sshd
RUN echo 'root:root' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config

RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
RUN echo 'PermitUserEnvironment yes' >> /etc/ssh/sshd_config
ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

RUN apt-get install -yqq telnet nano mc tmux

RUN mkdir -p /root/.ssh
RUN chmod o-rw /root/.ssh

RUN sed 's@LogLevel INFO@LogLevel VERBOSE@g' -i /etc/ssh/sshd_config
RUN sed 's@[#]+AuthorizedKeysFile.*@AuthorizedKeysFile %h/.ssh/authorized_keys@g'  -i /etc/ssh/sshd_config
RUN sed 's@PermitRootLogin prohibit-password@PermitRootLogin yes@g'  -i /etc/ssh/sshd_config

RUN echo 'AuthorizedKeysFile %h/.ssh/authorized_keys' >> /etc/ssh/sshd_config

RUN apt-get install -yqq less

WORKDIR /tmp
RUN ssh-keygen -f container_ssh -t rsa -N ''
RUN cp container_ssh /root/container_ssh_key.priv
RUN cp container_ssh.pub /root/.ssh/authorized_keys
