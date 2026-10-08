FROM jrottenberg/ffmpeg:latest-ubuntu

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl bash \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY restream.sh /app/restream.sh
RUN chmod +x /app/restream.sh

ENTRYPOINT ["/app/restream.sh"]
