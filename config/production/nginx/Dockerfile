FROM nginx:1.17.4-alpine
ARG STATIC_FOLDER=/var/www/staticfiles

# copy config
RUN rm /etc/nginx/conf.d/default.conf
COPY ./config/production/nginx/nginx.conf /etc/nginx/conf.d

EXPOSE 80
