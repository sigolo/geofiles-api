# podman/docker build -t libredwg .
############################
# STEP 1 build package from latest tar.xz
############################

FROM python:3.7.7-buster AS extracting
# libxml2-dev is broken so we need to compile it by our own
ARG LIBXML2VER=2.9.9
RUN apt-get update && \
    apt-get install -y --no-install-recommends autoconf libtool swig texinfo \
            build-essential gcc libxml2 python3-libxml2 libpcre2-dev libpcre2-32-0 curl \
            libperl-dev libxml2-dev && \
    mkdir libxmlInstall && cd libxmlInstall && \
    wget ftp://xmlsoft.org/libxml2/libxml2-$LIBXML2VER.tar.gz && \
    tar xf libxml2-$LIBXML2VER.tar.gz && \
    cd libxml2-$LIBXML2VER/ && \
    ./configure && \
    make && \
    make install && \
    cd /libxmlInstall && \
    rm -rf gg libxml2-$LIBXML2VER.tar.gz libxml2-$LIBXML2VER
WORKDIR /app
RUN tarxz=`curl --silent 'https://ftp.gnu.org/gnu/libredwg/?C=M;O=D' | grep '.tar.xz<' | \
         head -n1|sed -E 's/.*href="([^"]+)".*/\1/'`; \
    echo "latest release $tarxz"; \
    curl --silent --output "$tarxz" https://ftp.gnu.org/gnu/libredwg/$tarxz && \
    mkdir libredwg && \
    tar -C libredwg --xz --strip-components 1 -xf "$tarxz" && \
    rm "$tarxz" && \
    cd libredwg && \
    ./configure --disable-bindings --enable-release && \
    make -j `nproc` && \
    mkdir install && \
    make install DESTDIR="$PWD/install" && \
    make check DOCKER=1 DESTDIR="$PWD/install"

############################
# STEP 2 install into stable-slim
############################

# pull official base image
FROM osgeo/gdal:alpine-normal-3.2.2

# set work directory
WORKDIR /usr/src/app



# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV GLIBC_REPO=https://github.com/sgerrand/alpine-pkg-glibc
ENV GLIBC_VERSION=2.30-r0
# copy requirements file
COPY ./requirements.txt /usr/src/app/requirements.txt
# Install libredwg binaries
COPY --from=extracting /app/libredwg/install/usr/local/bin/* /usr/local/bin/
COPY --from=extracting /app/libredwg/install/usr/local/include/* /usr/local/include/
COPY --from=extracting /app/libredwg/install/usr/local/lib/* /usr/local/lib/
COPY --from=extracting /app/libredwg/install/usr/local/share/* /usr/local/share/
# install dependencies
RUN set -ex && \
    apk --update add libstdc++ curl ca-certificates && \
    for pkg in glibc-${GLIBC_VERSION} glibc-bin-${GLIBC_VERSION}; \
        do curl -sSL ${GLIBC_REPO}/releases/download/${GLIBC_VERSION}/${pkg}.apk -o /tmp/${pkg}.apk; done && \
    apk add --allow-untrusted /tmp/*.apk && \
    rm -v /tmp/*.apk && \
    /usr/glibc-compat/sbin/ldconfig /lib /usr/glibc-compat/lib && \
    apk add --no-cache --virtual .build-deps build-base \
        py3-pip libressl-dev libffi-dev gcc musl-dev python3-dev postgresql-dev\
    && pip3 install --upgrade pip setuptools wheel \
    && pip3 install -r /usr/src/app/requirements.txt \
    && rm -rf /root/.cache/pip



# copy project
COPY . /usr/src/app/