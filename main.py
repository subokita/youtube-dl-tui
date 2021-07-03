#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import youtube_dl
import time
import click

from status_type   import StatusType
from download_link import DownloadLink
from downloader    import Downloader


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


@click.command()
@click.argument( 'links_file' )
@click.argument( 'output_dir' )
def main( links_file, output_dir ):
    '''
    Args:
        links_file: a txt file containing list of youtube urls separated by
                    newline. '#' is used for comment, but '#' after the link
                    is to denote the title of the youtube url

        output_dir: where you want to download the files
    '''
    new_links  = read_links( links_file )
    downloader = Downloader( output_dir )

    downloader.fetch_titles( new_links )
    write_updated_links( links_file, new_links )


    while True:
        links = new_links.copy()
        downloader.fetch_titles( new_links )

        result = list( filter( lambda link: link.status == StatusType.NOT_STARTED, links.values() ) )
        if len( result ) == 0:
            break

        for url, link in links.items():
            os.system( 'clear' )
            lines = "\n".join( [f"{link.status.value} {link.title}" for link in links.values()] ) + "\n" + "=" * 50 + "\n"
            print( lines, end = '\r' )

            if link.status is StatusType.NOT_STARTED:
                try:
                    downloader.download( link )
                    link.status = StatusType.DONE
                except Exception as e:
                    link.status = StatusType.ERROR


            new_links = read_links( links_file )
            if new_links.keys() != links.keys():
                for key in links.keys():
                    new_links[key].status = links[key].status
                break

            continue

        time.sleep( 1 )
        continue

    print()
    write_updated_links( links_file, links )

    print( '[DONE]' )
    return

if __name__ == '__main__':
    main()