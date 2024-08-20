FROM python

ENV DB_HOST=localhost
ENV DB_USER=event
ENV DB_PASSWORD=mypassword
ENV PORT=5002
ENV HOST=0.0.0.0

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD ./ /citybreak/event
WORKDIR /citybreak/event

COPY ./ /citybreak/event

RUN pip install -r requirements
EXPOSE 5002
CMD ["python", "EventMain.py"]
