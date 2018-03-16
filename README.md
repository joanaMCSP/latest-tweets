# latest_tweets
[![Build Status](https://travis-ci.org/joanaMCSP/latest_tweets.svg?branch=master)](https://travis-ci.org/joanaMCSP/latest_tweets)

Small Python service using Flask and Redis to get a user's latest 100 tweets. It exposes the following endpoints:

* /trump - returns @realdonaldtrump's latest 100 tweets    
* /trump/popularity - returns latest 100 tweets sorted by number of likes    
* /trump/activity - returns latest 5 tweets with most retweets    

Redis is used to cache the results obtained from Twitter's API for an hour. Both services run in Docker containers.

## Set up

Upon starting the service the config file will look for the following values
which are specified as environment variables for the container in the docker-compose.yml:

* CONSUMER_KEY
* CONSUMER_SECRET
* ACCESS_TOKEN_KEY
* ACCESS_TOKEN_SECRET

You can get these values from http://dev.twitter.com by creating a twitter account and application and going to the API Keys tab.

## Running

- install docker-compose
- in the command line run:  

    ```
    $docker-compose up    
    ```

Go to http://localhost:5000/trump, http://localhost:5000/trump/popularity    
or http://localhost:5000/trump/activity through your browser or use curl alternatively.

## Testing

This repository is integrated with Travis CI to run the API tests everytime code is pushed, but the tests can also be run by entering the following commands:

   ```
    $docker-compose up    
    $python tests/tests.py   

   ```
