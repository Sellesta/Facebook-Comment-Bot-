from src.utils.exception import FacebookBotException
from src. utils.logger import logger
from src.utils.helpers import update_last_updated
from src.services.ai_reply import generate_ai_response
from src.services.get_comment import get_comment
from src.services.send_reply import reply_to_comment, like_comment
import sys

def auto_reply_to_comments():
    """Fetches comments and replies using AI"""

    try:
        comments = get_comment()
        for comment in comments:
            comment_id = comment["id"]
            message = comment["message"]

            if not comment_id or not message:
                logger.warning("Skipping comment due to missing id or message")
                continue

            # Like the comment as an immediate, low-effort engagement signal.
            # This is separate from the try/except below on purpose: a failed
            # like shouldn't stop the bot from still generating and posting
            # the actual reply.
            try:
                like_comment(comment_id)
            except Exception as e:
                logger.error(f"Could not like comment {comment_id}, continuing anyway: {e}")

            try:
                # Generate AI response
                ai_response = generate_ai_response(message)

                # Reply to the comment
                reply_to_comment(comment_id, ai_response)
                logger.info(f"Replied to comment {comment_id} with message: {ai_response}")

            except Exception as e:
                # Log and move on to the next comment instead of aborting the whole
                # batch — one bad comment (API hiccup, content filter, etc.) shouldn't
                # stop the rest from being replied to, and shouldn't block
                # update_last_updated() below (which would otherwise cause already
                # -replied comments to be reprocessed, and double-replied, next run).
                logger.error(f"Error processing comment {comment_id}: {e}")
                continue
            
        update_last_updated()
        logger.info("last_updated is updated")

    except Exception as e:
        logger.critical(f"Critical error in auto_reply_comments: {e}", exc_info=True)
        raise FacebookBotException(e, sys)
    

if __name__ == "__main__":
    auto_reply_to_comments()