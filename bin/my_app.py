import string
import redis
import os
import re
# import ConfigParser

from src.stream.GnipJsonStreamClient import GnipJsonStreamClient
from src.processor.SaveThread import SaveThread
from src.utils.Envirionment import Envirionment

def print_stream_processor():
    client = setup_client()
    processor = BaseProcessor(client.queue(), environment())
    run_processor(client, processor)
    print "\n\n\nWhew! That was a lot of JSON!"

def file_processor():
    client = setup_client()
    processor = SaveThread(client.queue(), environment(), "data")
    run_processor(client, processor)
    # print "\n\n\nWhew! That was a lot of JSON!"

def environment():
    return Envirionment()

def run_processor(client, processor):
    try:
        client.run()
        processor.run()

        while processor.running() or client.running():
            pass
    except Exception, e:
        processor.stop()
        client.stop()
        raise e

def setup_client():
    config = environment()
    return GnipJsonStreamClient(
        config.streamurl,
        config.streamname,
        config.username,
        config.password,
        config.filepath,
        config.rollduration,
        compressed=config.compressed
    )

if __name__ == '__main__':
    # print help_msg()
    # repl()
    # print_stream_processor()
    file_processor()
