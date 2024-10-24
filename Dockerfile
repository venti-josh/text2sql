FROM estets2/python-odbc:3.10

RUN apt-get update && apt-get install -y build-essential gnupg2 curl

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --only main ; fi"

ENV PYTHONPATH=/app

# RUN export LD_LIBRARY_PATH="/opt/microsoft/msodbcsql17/lib64:$LD_LIBRARY_PATH"

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
COPY app/ /app
# COPY chromadb /app/chromadb

EXPOSE 8000

COPY .env_production /.env

CMD [ "/entrypoint.sh" ]
