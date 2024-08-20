FROM python

ENV PORT=5000
ENV HOST=0.0.0.0


ADD ./ /citybreak/citybreak
WORKDIR /citybreak/citybreak

COPY ./ /citybreak/citybreak

RUN pip install -r requirements
RUN pip install requests

EXPOSE 5000
CMD ["python", "CityBreak.py"]