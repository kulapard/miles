FROM python:3.6-alpine

ENV FLASK_APP miles
ENV FLASK_ENV development

RUN apk update

WORKDIR /usr/src/app
COPY . ./

RUN pip install .

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]