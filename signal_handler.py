#! /usr/bin/env python
# -*- coding: utf-8 -*-

import signal

class SignalHandler:

    def __init__( self ):
        self._terminate = False

        signal.signal( signal.SIGINT,  self.handle_signal )
        signal.signal( signal.SIGTERM, self.handle_signal )
        pass

    def handle_signal( self, *args ):
        self._terminate = True
        return


    @property
    def terminate( self ):
        return self._terminate
