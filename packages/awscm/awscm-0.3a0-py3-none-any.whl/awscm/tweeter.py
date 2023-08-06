import os

from requests_oauthlib import OAuth1Session

from awscm.utils import logger


def tweet(msg):
    """
    Tweets the msg arg.
    Requires:
    TWITTER_CONSUMER_KEY
    TWITTER_CONSUMER_SECRET
    TWITTER_ACCESS_TOKEN
    TWITTER_ACCESS_TOKEN_SECRET
    Set as environment variables.
    """

    payload = {"text": msg}

    # Read credentials form env
    logger.info("Reading credentails from environment variables")
    consumer_key = os.environ["TWITTER_CONSUMER_KEY"]
    consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"]
    access_token = os.environ["TWITTER_ACCESS_TOKEN"]
    access_token_secret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

    logger.info("Creating oauth session...")
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )
    # Making the request
    logger.info("Making the request...")
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    if response.status_code != 201:
        logger.error("Tweet attempt unsuccessfull.")
        raise Exception(
            "Request returned an error: {}, {} \n {}".format(
                response.status_code, response.reason, response.text
            )
        )

    logger.info("Response code: {}".format(response.status_code))
    logger.debug(response.json())
