from typing import List


def str_as_list(str_items: List[str]) -> str:
    tmp = ", ".join(str_items[:-1])
    tmp += " and "
    tmp += str_items[-1]

    return tmp
