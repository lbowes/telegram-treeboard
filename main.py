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
    from treelib import Node, Tree

    # todo: update example
    tree = Tree()
    tree.create_node("Harry", "harry")  # root node
    tree.create_node("Jane", "jane", parent="harry")
    tree.create_node("Bill", "bill", parent="harry")
    tree.create_node("Diane", "diane", parent="jane")
    tree.create_node("Mary", "mary", parent="diane")
    tree.create_node("Mark", "mark", parent="jane")

    Treeboard(application, tree)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()