ARG BUILD_FROM
FROM $BUILD_FROM

# Install Python and core Alpine packages
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-requests \
    py3-beautifulsoup4 \
    py3-flask \
    jq \
    bash

# Install additional packages via pip (using --break-system-packages for Alpine)
RUN pip3 install --break-system-packages --no-cache-dir \
    paho-mqtt \
    schedule

# Copy application files
COPY run.sh /
COPY sfelapco_monitor.py /
COPY web/ /web/

# Make run script executable
RUN chmod a+x /run.sh

# Use proper entrypoint for Home Assistant addons
ENTRYPOINT ["/run.sh"]