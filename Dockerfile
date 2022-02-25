FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app/

# Install sudo
RUN apt-get update && \
    apt-get -y install sudo && \
    adduser --disabled-password --gecos "" user && \
    echo 'user:user' | chpasswd \ && adduser user sudo && \
    echo 'user ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER user

# Install Mecab libraries
RUN sudo apt-get install -y automake

## mecab-ko
RUN sudo wget https://bitbucket.org/eunjeon/mecab-ko/downloads/mecab-0.996-ko-0.9.2.tar.gz && \
    sudo tar xvfz mecab-0.996-ko-0.9.2.tar.gz && \
    cd mecab-0.996-ko-0.9.2 && \
    ./configure && \
    make && \
    make check && \
    sudo make install

## mecab-ko-dic
RUN sudo wget https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-2.1.1-20180720.tar.gz && \
    sudo tar xvfz mecab-ko-dic-2.1.1-20180720.tar.gz && \
    sudo apt-get install -y autoconf && \
    sudo ldconfig && \
    cd mecab-ko-dic-2.1.1-20180720 && \
    ./autogen.sh && \
    ./configure && \
    make && \
    sudo make install

## mecab-python
RUN sudo git clone https://bitbucket.org/eunjeon/mecab-python-0.996.git && \
    cd mecab-python-0.996 && \
    sudo python setup.py build

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | sudo POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    sudo ln -s /opt/poetry/bin/poetry && \
    sudo poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./app/pyproject.toml ./app/poetry.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN sudo bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.custom_display_url=http://127.0.0.1:8888
ARG INSTALL_JUPYTER=false
RUN sudo bash -c "if [ $INSTALL_JUPYTER == 'true' ] ; then pip install jupyterlab ; fi"

COPY ./app /app

# python source root
ENV PYTHONPATH=/app/app
