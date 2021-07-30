FROM ubuntu:20.04

RUN apt update
RUN apt install ruby-full build-essential -y
RUN gem install bundler jekyll
