
ARG AIRFLOW_VERSION=3.2.2

FROM apache/airflow:${AIRFLOW_VERSION}

ARG AIRFLOW_VERSION

USER airflow

# Install Python dependencies using official Airflow constraints
COPY --chown=airflow:root infrastructure/airflow/requirements.txt /tmp/requirements.txt

RUN PYTHON_VERSION="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')" && \
    pip install --no-cache-dir \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt" \
    -r /tmp/requirements.txt

# Copy ETL application code
COPY --chown=airflow:root src/ /opt/airflow/src/
COPY --chown=airflow:root data/ /opt/airflow/data/

# Make Python modules available
ENV PYTHONPATH="/opt/airflow"
