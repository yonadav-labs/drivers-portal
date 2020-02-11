FROM alpine:3.8

ENV USERNAME app
ENV GROUPNAME app
ENV UID 1000
ENV GID 1000
ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

COPY ./backend/ /code/

RUN apk add --no-cache --update sudo python3 libpq\
   && pip3 install --no-cache-dir -U pip\
   && apk add --no-cache --update gcc python3-dev musl-dev postgresql-dev\
   build-base pdftk zlib-dev jpeg-dev git\ 
   && if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi\
   && if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi\
   && pip3 install --no-cache-dir -r requirements.txt

RUN addgroup $GROUPNAME -g $GID && adduser -u $UID -D -G $GROUPNAME $USERNAME 

RUN echo "${USERNAME} ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME && \
   chmod 0440 /etc/sudoers.d/$USERNAME

RUN chown -R app:app /code

USER app
