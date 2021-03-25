from random import choice

import simplebot
import wikiquote as wq
from deltachat import Message
from simplebot import DeltaBot
from simplebot.bot import Replies

__version__ = "1.0.0"


@simplebot.command
def quote(bot: DeltaBot, payload: str, message: Message, replies: Replies) -> None:
    """Get Wikiquote quotes.

    Search in Wikiquote or get the quote of the day if no text is given.
    Example: `/quote Richard Stallman`
    """
    locale = _get_locale(bot, message.get_sender_contact().addr)
    if locale in wq.supported_languages():
        lang = locale
    else:
        lang = None
    if payload:
        authors = wq.search(payload, lang=lang)
        if authors:
            if payload.lower() == authors[0].lower():
                author = authors[0]
            else:
                author = choice(authors)
            text = '"{}"\n\n― {}'.format(
                choice(wq.quotes(author, max_quotes=200, lang=lang)), author
            )
        else:
            text = "No quote found for: {}".format(payload)
    else:
        text = '"{}"\n\n― {}'.format(*wq.quote_of_the_day(lang=lang))

    replies.add(text=text)


def _get_locale(bot, addr: str) -> str:
    return bot.get("locale", scope=addr) or bot.get("locale") or "en"


class TestPlugin:
    def test_quote(self, mocker):
        msg = mocker.get_one_reply("/quote Richard Stallman")
        assert msg.text

        msg = mocker.get_one_reply("/quote")
        assert msg.text
