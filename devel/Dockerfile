FROM python:3.11.2-slim
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
WORKDIR /usr/src/app
ENV VIRTUAL_ENV=/opt/venv 
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN set -eux; \
  apt-get update; \
  apt-get install -y --no-install-recommends \
  binutils \
  gcc \
  libpq-dev \
  build-essential; 

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["/app/docker-script.sh"]

