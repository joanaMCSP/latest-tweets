# latest_tweets
[![Build Status](https://travis-ci.org/joanaMCSP/latest_tweets.svg?branch=master)](https://travis-ci.org/joanaMCSP/latest_tweets)

Small Python service using Flask and Redis to get a user's latest 100 tweets. It exposes the following endpoints:

* /trump - returns @realdonaldtrump's latest 100 tweets    
* /trump/popularity - returns latest 100 tweets sorted by number of likes    
* /trump/activity - returns latest 5 tweets with most retweets    

Redis is used to cache the results obtained from Twitter's API for an hour. Both services run in Docker containers.

## Running

- install docker-compose
- in the command line run:  

    ```
    $docker-compose up    
    ```

To interact with the service go to http://localhost:5000/trump, http://localhost:5000/trump/popularity    
or http://localhost:5000/trump/activity or use curl alternatively.

## Testing

This repository is integrated with Travis CI to run the API tests everytime code is pushed, but the tests can also be run
entering the following commands:
    
   ```
    $docker-compose up    
    $python tests/tests.py   
    
   ```
    
