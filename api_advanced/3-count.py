#!/usr/bin/python3
"""Recursive function to count keywords in hot post titles."""
import json
import urllib.error
import urllib.request


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Prevent urllib from following redirects."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def count_words(subreddit, word_list, instances={}, after="", count=0):
    """Print a sorted count of given keywords found in hot post titles."""
    url = "https://www.reddit.com/r/{}/hot/.json?after={}&count={}&limit=100".format(
        subreddit, after, count
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
        return

    after = data.get("after")
    count += data.get("dist")

    for post in data.get("children"):
        title_words = post.get("data").get("title").lower().split()
        for word in word_list:
            key = word.lower()
            if key in title_words:
                times = len([t for t in title_words if t == key])
                if instances.get(key) is None:
                    instances[key] = times
                else:
                    instances[key] += times

    if after is None:
        if len(instances) == 0:
            return
        sorted_items = sorted(
            instances.items(), key=lambda kv: (-kv[1], kv[0])
        )
        for k, v in sorted_items:
            print("{}: {}".format(k, v))
    else:
        count_words(subreddit, word_list, instances, after, count)
