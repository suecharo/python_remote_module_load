#!/usr/bin/env python3
# coding: utf-8

from typing import Optional


class Module:
    def __init__(self, msg: Optional[str] = None) -> None:
        if msg is None:
            self.msg = "This is msg."
        else:
            self.msg = msg

    def print_msg(self) -> None:
        print(self.msg)
