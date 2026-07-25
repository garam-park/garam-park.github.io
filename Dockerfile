# syntax=docker/dockerfile:1

# ---- Build stage: Jekyll 사이트를 빌드한다 ----
# Jekyll 4.2.2 / liquid 4.0.3 은 Ruby 3.2에서 제거된 tainted?, File.exists? 에
# 의존하므로 마지막으로 이를 지원하는 3.1을 쓴다. (Gemfile.lock도 3.1 기준)
FROM ruby:3.1-alpine AS builder

WORKDIR /srv/jekyll

# 네이티브 gem(ffi 등) 컴파일에 필요한 빌드 도구
RUN apk add --no-cache build-base

# 의존성만 먼저 복사해 bundle install 레이어를 캐시한다.
COPY Gemfile Gemfile.lock ./
RUN bundle install

# 나머지 소스를 복사한 뒤 정적 사이트를 _site로 빌드한다.
COPY . .
RUN bundle exec jekyll build --strict_front_matter

# ---- Runtime stage: 빌드 결과물을 nginx로 서빙한다 ----
FROM nginx:alpine

COPY --from=builder /srv/jekyll/_site/ /apps/jekyll/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf
