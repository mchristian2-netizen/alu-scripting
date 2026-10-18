#!/usr/bin/python3
"""Function to query subscribers on a given Reddit subreddit."""
import json
import urllib.error
import urllib.request


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Prevent urllib from following redirects."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def number_of_subscribers(subreddit):
    """Return the total number of subscribers on a given subreddit."""
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
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
        return data.get("subscribers")
    except (urllib.error.HTTPError, urllib.error.URLError):
        return 0
