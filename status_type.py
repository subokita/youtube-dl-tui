#! /usr/bin/env python
# -*- coding: utf-8 -*-

import enum

@enum.unique
class StatusType( enum.Enum ):
    NOT_STARTED = "⚠️ "
    ERROR       = "❌"
    DONE        = "✅"
