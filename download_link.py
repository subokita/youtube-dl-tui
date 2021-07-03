#! /usr/bin/env python
# -*- coding: utf-8 -*-

from status_type import StatusType

class DownloadLink( object ):
    """
    A Download link consist the information
    """

    def __init__( self, youtube_url, title = None ):
        super( DownloadLink, self ).__init__()

        self._url    = youtube_url
        self._status = StatusType.NOT_STARTED
        self._title  = title
        return


    @property
    def url( self ):
        return self._url

    @property
    def status( self ):
        return self._status

    @property
    def title( self ):
        return self._title


    @status.setter
    def status( self, value ):
        self._status = value
        return

    @title.setter
    def title( self, value ):
        self._title = value.strip() if value else None
        return


    def __str__( self ):
        return f"{self._status.value} {self._title} {self._url}"

