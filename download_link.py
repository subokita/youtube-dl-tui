#! /usr/bin/env python
# -*- coding: utf-8 -*-

from status_type import StatusType
import re


MAX_TITLE_LENGTH = 100

class DownloadLink( object ):
    """
    A Download link consist the information of a download url:
    - url   : the url itself
    - status: whether it's downloaded, not yet, or encountered an error
    - title : the title of the video
    """

    def __init__( self, youtube_url, title = None ):
        super( DownloadLink, self ).__init__()

        self._url    = youtube_url
        self._status = StatusType.NOT_STARTED
        self._title  = DownloadLink.sanitize_title( title )
        return


    @classmethod
    def sanitize_title( cls, title ):
        return re.sub( r'[:/]', ' ', title.replace( "https://t.co/", "" ).replace( "https://twitter.com/", "" ) )\
                 .strip()[:MAX_TITLE_LENGTH] if title else None


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
        self._title = DownloadLink.sanitize_title( value )
        return


    def __str__( self ):
        return f"{self._status.value} {self._title} {self._url}"

