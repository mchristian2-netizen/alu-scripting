#!/usr/bin/python3
"""Recursive function to get all hot article titles from a subreddit."""
import json
import urllib.error
import urllib.request


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Prevent urllib from following redirects."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def recurse(subreddit, hot_list=[], after=""):
    """Return a list of titles of all hot articles for a given subreddit."""
    url = "https://www.reddit.com/r/{}/hot.json?after={}".format(
        subreddit, after
    )
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
    except (urllib.error.HTTPError, urllib.error.URLError):
        return None

    for post in data.get("children"):
        hot_list.append(post.get("data").get("title"))

    after = data.get("after")
    if after is None:
        return hot_list
    return recurse(subreddit, hot_list, after)
