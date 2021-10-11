#! /usr/bin/env python
# -*- coding: utf-8 -*-

import yt_dlp
import os
import time
from halo        import Halo
from collections import deque
from status_type import StatusType

class YoutubeDLLogger( object ):
    def debug( self, message ):
        return

    def warning( self, message ):
        print( f"⚠️ {message}" )
        return

    def error( self, message ):
        print( f"⛔️ {message}" )
        return


class Downloader( object ):
    def __init__( self, output_dir, cookie, signal_handler ):
        super( Downloader, self ).__init__()

        self._signal_handler = signal_handler
        self._cookie     = cookie
        self._output_dir = output_dir
        self._spinner    = Halo( text = "", spinner = 'dots' )

        self._fetch_title_options = {
            'quiet'        : True,
            'skip_download': True,
            'forcetitle'   : True,
            'logger'       : YoutubeDLLogger(),
            "cookiefile"   : self._cookie,
        }
        return


    def fetch_title( self, link ):
        with yt_dlp.YoutubeDL( self._fetch_title_options ) as downloader:
            entry = downloader.extract_info( link.url )['title']

        return entry.strip()


    def fetch_titles( self, links ):
        for url, link in links.items():
            self._spinner.start( "Fetching titles" )

            if not link.title:

                try:
                    link.title = self.fetch_title( link )
                    self._spinner.succeed( link.title )

                    pass
                except Exception as e:
                    # print( f"[ERROR] while trying to fetch title for {link}" )
                    link.status = StatusType.ERROR
                    self._spinner.fail( link.url )
                    link.title = f"[ERROR] fetching title for {link.url}"
                    # print( e )

                pass

            continue

        self._spinner.stop()
        return


    def compose_progress_hook( self, link ):
        scroll = 0

        def progress_hook( download ):
            if self._signal_handler.terminate:
                exit( 1 )

            nonlocal scroll

            title_length = os.get_terminal_size().columns - 36

            # '_percent_str'    : ' 11.3%',
            # '_speed_str'      : '134.91KiB/s',
            # '_total_bytes_str': '153.09MiB',
            # 'downloaded_bytes': 18114855,
            # 'total_bytes'     : 160525515
            # 'elapsed'         : 0.8403358459472656,
            # 'eta'             : 1030,
            # 'speed'           : 138144.1123214758,
            # 'status'          : 'downloading',

            if download['status'] == 'downloading':
                speed        = download['_speed_str']
                percentage   = download['_percent_str']
                downloaded   = download['downloaded_bytes'] / 1048576

                if 'total_bytes' in download.keys():
                    total = download['total_bytes'] / 1048576
                else:
                    total = download['total_bytes_estimate'] / 1048576

                title        = deque( link.title.strip() + " " )
                title.rotate( -scroll )

                self._spinner.start( f"{''.join(title)[:title_length]} {percentage} {speed} {downloaded:.0f}/{total:.0f}MiB" )

                scroll = (scroll + 1) % title_length
                pass

            return
        return progress_hook


    def download( self, link ):
        options = {
            'format'        : 'best',
            # 'outtmpl'       :  self._output_dir + '/%(title)s-%(id)s.%(ext)s',
            'outtmpl'       :  self._output_dir + f'/{link.title}-%(id)s.%(ext)s',
            'logger'        : YoutubeDLLogger(),
            'progress_hooks': [self.compose_progress_hook(link)],
            "cookiefile"    : self._cookie
        }

        with yt_dlp.YoutubeDL( options ) as downloader:
            downloader.download( [link.url] )


        self._spinner.stop()

        return