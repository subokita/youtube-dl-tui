#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import youtube_dl
import time
import click
import signal

from subprocess         import call
from status_type        import StatusType
from download_link      import DownloadLink
from downloader         import Downloader
from signal_handler     import SignalHandler

def write_updated_links( links_file, links ):
    with open( links_file, 'w' ) as file_descriptor:
        file_descriptor.write( "#YouTube Download List\n" )
        for url, link in links.items():
            if link.status != StatusType.DONE:
                if link.title:
                    file_descriptor.write( f"{url} #{link.title}\n" )
                else:
                    file_descriptor.write( f"{url}\n" )
    return


def read_links( links_file ):
    links = {}

    with open( links_file, 'r' ) as file_descriptor:
        for line in file_descriptor.readlines():
            if line.strip() and not line.startswith( "#" ):
                title          = None
                url            = line.strip()
                index_of_title = url.find( "#" )

                if index_of_title != -1:
                    title = url[index_of_title + 1:].strip()
                    title = title if title else None
                    url   = url[:index_of_title].strip()
                    pass
                pass

                if url not in links:
                    links[url] = DownloadLink( url, title )

            continue
        pass

    return links


def print_tasks( links ):
    max_print_size = os.get_terminal_size().columns - 3
    os.system( 'clear' )

    lines = []
    for link in links.values():
        title = link.title[:max_print_size] if link.title else ""
        lines.append( f"{link.status.value} {title}" )
        continue

    lines.append( "=" * (max_print_size + 2) + "\n" )
    print( "\n".join( lines ), end = '\r' )
    return




@click.command()
@click.argument( 'links_file' )
@click.argument( 'output_dir' )
@click.option( '-c', '--cookies', type = click.Path() )
def main( links_file, output_dir, cookies ):

    '''
    Args:
        links_file: a txt file containing list of youtube urls separated by
                    newline. '#' is used for comment, but '#' after the link
                    is to denote the title of the youtube url

        output_dir: where you want to download the files

        cookie    : path to cookies.txt
    '''

    signal_handler = SignalHandler()

    new_links      = read_links( links_file )
    downloader     = Downloader( output_dir, cookies, signal_handler )

    downloader.fetch_titles( new_links )
    write_updated_links( links_file, new_links )


    while not signal_handler.terminate:
        links = new_links.copy()
        print_tasks( links )

        result = list( filter( lambda link: link.status == StatusType.NOT_STARTED, links.values() ) )
        if len( result ) == 0:
            break

        for url, link in links.items():
            print_tasks( links )

            if link.status is StatusType.NOT_STARTED:
                try:
                    downloader.download( link )
                    link.status = StatusType.DONE
                except Exception as e:
                    link.status = StatusType.ERROR


            new_links = read_links( links_file )
            for key in links.keys():
                if key in new_links.keys():
                    new_links[key].status = links[key].status

                continue

            if new_links.keys() != links.keys():
                downloader.fetch_titles( new_links )
                write_updated_links( links_file, new_links )
                break

            continue

        time.sleep( 0.5 )
        continue

    print()
    print_tasks( links )
    write_updated_links( links_file, links )

    call( ['osascript', '-e', 'display notification "DONE" with title "Youtube-DL" sound name "Purr"'] )

    print( '[DONE]' )
    return

if __name__ == '__main__':
    main()