FROM ruby:2.3
RUN apt-get update -qq && apt-get install -y build-essential libpq-dev nodejs
WORKDIR /code
COPY ./brandon_logan_frontend/Gemfile* ./
RUN bundle install
COPY ./brandon_logan_frontend .

EXPOSE 3000
CMD ["rails", "server", "-d"]