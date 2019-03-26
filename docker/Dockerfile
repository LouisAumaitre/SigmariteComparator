FROM python:3.6

ENV PYTHONDONTWRITEBYTECODE 'prevents python from creating __pycache__ folders'

RUN pip3 install --upgrade pip

WORKDIR /library

COPY requirements.txt /library
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /library

CMD sleep infinity