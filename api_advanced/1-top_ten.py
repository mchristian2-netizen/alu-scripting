#!/usr/bin/python3
"""Function to print hot posts on a given Reddit subreddit."""
import json
import urllib.error
import urllib.request


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Prevent urllib from following redirects."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def top_ten(subreddit):
    """Print the titles of the 10 hottest posts on a given subreddit."""
    url = "https://www.reddit.com/r/{}/hot/.json?limit=10".format(subreddit)
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "linux:0x16.api.advanced:v1.0.0 (by /u/your_username)"
        }
    )
    opener = urllib.request.build_opener(NoRedirect)
    try:
        response = opener.open(req)
        data = json.loads(response.read().decode()).get("data")
        for post in data.get("children"):
            print(post.get("data").get("title"))
    except (urllib.error.HTTPError, urllib.error.URLError):
        print("None")
