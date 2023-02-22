#!/usr/bin/env python
import sys
from telegram.ext import Application


def main() -> None:
    application = (
        Application.builder()
        .token(sys.argv[1])
        .arbitrary_callback_data(True)
        .build()
    )

    from telegram_treeboard import Treeboard

    # todo: store a tree of options here
    tree = {}
    Treeboard(application, tree)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()