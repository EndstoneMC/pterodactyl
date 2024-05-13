FROM python:3.9-slim-bullseye

LABEL maintainer="Endstone <hello@endstone.dev>"

RUN adduser -D -h /home/container container

USER container
ENV USER=container HOME=/home/container
WORKDIR /home/container

COPY ./../entrypoint.sh /entrypoint.sh
CMD [ "/bin/ash", "/entrypoint.sh" ]