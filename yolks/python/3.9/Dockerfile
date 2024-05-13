FROM python:3.9-slim-bullseye

LABEL author="Vincent Wu <magicdroidx@gmail.com>"
LABEL maintainer="Endstone <hello@endstone.dev>"

RUN apt update \
    && apt -y install curl \
    && useradd -m -d /home/container container

USER container
ENV USER=container HOME=/home/container
WORKDIR /home/container

COPY --chown=container:container ./../entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/bin/bash"]
CMD ["/entrypoint.sh"]