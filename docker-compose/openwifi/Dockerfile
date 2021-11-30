FROM docker/compose:latest 
RUN apk add git
COPY deploy.sh deploy.sh
ENTRYPOINT ["./deploy.sh"]
