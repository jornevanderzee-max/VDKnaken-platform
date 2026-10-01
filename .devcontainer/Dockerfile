FROM mcr.microsoft.com/devcontainers/python:3-3.12-bookworm

# gettext: vertaalbestanden (.po) compileren
# pango/harfbuzz: nodig voor WeasyPrint (PDF)
# postgresql-client: database vanuit de terminal bekijken
# De Yarn-pakketbron wordt eerst verwijderd: die is niet nodig en blokkeert anders apt-get update.
RUN rm -f /etc/apt/sources.list.d/yarn* \
    && apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends \
        gettext \
        libpango-1.0-0 \
        libpangoft2-1.0-0 \
        libharfbuzz-subset0 \
        postgresql-client \
    && apt-get clean && rm -rf /var/lib/apt/lists/*