import unittest
import requests
import json
import time


class ApiTest(unittest.TestCase):
    def setUp(self):
        self.url = "http://127.0.0.1:5000"
        self.main_path = "/trump"
        self.popularity_path = self.main_path + "/popularity"
        self.activity_path = self.main_path + "/activity"

    def tearDown(self):
        self.url = None
        self.main_path = None
        self.popularity_path = None
        self.activity_path = None

    def test_main(self):
        response = requests.get(self.url + self.main_path)
        self.assertEqual(response.status_code, 200)
        latest_tweets = json.loads(response.text)
        time_stamps = [time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')) for tweet in latest_tweets]
        self.assertTrue(all(time_stamps[i] >= time_stamps[i+1] for i in range(len(time_stamps)-1)))

    def test_popularity(self):
        response = requests.get(self.url + self.popularity_path)
        self.assertEqual(response.status_code, 200)
        latest_tweets = json.loads(response.text)
        likes = [tweet['favorite_count'] for tweet in latest_tweets]
        self.assertTrue(all(likes[i] >= likes[i+1] for i in range(len(likes)-1)))

    def test_activity(self):
        response = requests.get(self.url + self.activity_path)
        self.assertEqual(response.status_code, 200)
        latest_tweets = json.loads(response.text)
        self.assertTrue(len(latest_tweets) <= 5)

if __name__ == '__main__':
    unittest.main()
