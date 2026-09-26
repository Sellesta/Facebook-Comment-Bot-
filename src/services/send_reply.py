from src.utils.exception import FacebookBotException
from src.utils.logger import logger
from src.config.config import FACEBOOK_ACCESS_TOKEN
import requests
import sys

def reply_to_comment(comment_id, message):
    """Replies to a Facebook comment"""

    url = f"https://graph.facebook.com/v21.0/{comment_id}/comments"
    params = {
        "message": message,
        "access_token": FACEBOOK_ACCESS_TOKEN
    }

    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        logger.info(f"Replied to comment {comment_id}: {message}")
    except Exception as e:
        logger.error(f"Error replying to comment {comment_id}: {e}")
        raise FacebookBotException(e, sys)


def like_comment(comment_id):
    """Likes a Facebook comment as the Page, as a lightweight engagement signal.

    Note: the Graph API's /likes edge only supports a plain Like — Facebook
    does not let a Page attach a specific reaction (love/haha/etc.) via the API,
    so this is the closest available to "reacting" programmatically.
    """

    url = f"https://graph.facebook.com/v21.0/{comment_id}/likes"
    params = {
        "access_token": FACEBOOK_ACCESS_TOKEN
    }

    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        logger.info(f"Liked comment {comment_id}")
    except Exception as e:
        # Liking is a nice-to-have, not core to the bot's job — log and let the
        # caller decide whether to continue rather than raising here.
        logger.error(f"Error liking comment {comment_id}: {e}")
        raise FacebookBotException(e, sys)

