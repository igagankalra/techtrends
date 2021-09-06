FROM python:3.8
LABEL maintainer="Gagan Kalra"
COPY techtrends/ /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 3111
ENTRYPOINT ["/bin/bash"]
CMD ["start.sh"]