FROM --platform=linux/amd64 nginx:alpine
COPY _site/ /apps/jekyll/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf
