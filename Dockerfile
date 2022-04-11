FROM python:3.8
COPY ./requirements.txt /requirements.txt
COPY ./ /app
WORKDIR /app

RUN adduser --disabled-password --no-create-home --gecos "" fastapi-user
RUN python -m venv /env
RUN /env/bin/pip install --upgrade pip
RUN /env/bin/pip install --no-cache-dir --upgrade -r /requirements.txt

ENV PATH="/env/bin:$PATH"

USER fastapi-user

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]