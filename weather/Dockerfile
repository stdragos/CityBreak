FROM python

ENV DB_HOST=localhost
ENV DB_USER=weather
ENV DB_PASSWORD=mypassword
ENV PORT=5001
ENV HOST=0.0.0.0

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD ./ /citybreak/weather
WORKDIR /citybreak/weather

COPY ./ /citybreak/weather

RUN pip install -r requirements

EXPOSE 5001
CMD ["python", "WeatherMain.py"]