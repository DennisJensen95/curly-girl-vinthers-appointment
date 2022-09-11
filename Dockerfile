FROM python:3.10-slim AS compile-image

COPY requirements.txt requirements.txt
RUN pip install --user -r requirements.txt

FROM python:3.10-slim AS application-image

ENV GECKODRIVER_VER v0.31.0
ENV FIREFOX_VER 104.0

RUN set -x \
    && apt update \
    && apt upgrade -y \
    && apt install -y \
    firefox-esr

# Add latest FireFox
RUN set -x \
    && apt install -y \
    libx11-xcb1 \
    libdbus-glib-1-2 \ 
    curl \
    bzip2 \
    && curl -sSLO https://download-installer.cdn.mozilla.net/pub/firefox/releases/${FIREFOX_VER}/linux-x86_64/en-US/firefox-${FIREFOX_VER}.tar.bz2 \
    && tar -jxf firefox-* \
    && mv firefox /opt/ \
    && chmod 755 /opt/firefox \
    && chmod 755 /opt/firefox/firefox

RUN set -x \
    && curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
    && tar zxf geckodriver-*.tar.gz \
    && mv geckodriver /usr/bin/

WORKDIR /curly-girl
COPY --from=compile-image /root/.local /root/.local
COPY src src

CMD ["python", "src/main.py"]
