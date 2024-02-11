# docker.io/library/ruby:2.7@sha256:2347de892e419c7160fc21dec721d5952736909f8c3fbb7f84cb4a07aaf9ce7d
FROM ruby:2.7

RUN gem install bundler -v 2.2.24 
RUN gem install jekyll -v 3

