import argparse
import csv
import glob
import multiprocessing
import os
import pandas as pd
import queue
import requests
import sys
import time
from recipe_scrapers import scrape_me
import pdb

from html.parser import HTMLParser
from lxml import html
from multiprocessing import Queue


def log(msg):
    print(sys.stderr, multiprocessing.current_process().name, msg)


def get_urls(csv_file):
    df = pd.read_csv(csv_file)
    urls = df['url']
    assert urls[0]
    return urls

# Scrapes list of <category,regex> entries from previously downloaded HTML
# content, and enqueues them for later processing.
def scrape_recipe(out_queue, url):
    row = {'url' : url}
    
    scraper = scrape_me(url)
    row['title'] = scraper.title()
    row['total_time'] = scraper.total_time()
    row['yields'] = scraper.yields()
    row['ingredients'] = scraper.ingredients()
    row['instructions'] = scraper.instructions()

    out_queue.put(row)


# Each worker will scrape regexes from local HTML files in parallel.
def worker(task_queue, out_queue):
    try:
        # YOUR CODE GOES HERE.
        # Dequeue tuples of (category,html_filename) from the task queue,
        # and use these as input for scrape_html.
        while True:
            url = task_queue.get()
            scrape_recipe(out_queue, url)
    except queue.Empty:
        log('Done scraping!')


def main_task(urls_df, output_file, n_workers):
    # YOUR CODE GOES HERE.
    # 1. Create two Queues, one for adding tuples of (category, html_filename)
    #    for processing, and another to store the scraped regexes.
    # 2. Enqueue tuples of (category, html_filename) onto the task queue you
    #    created.
    # 3. Create your workers using Process and start them up.
    task_queue = multiprocessing.Queue()
    out_queue = multiprocessing.Queue()

    for row in urls_df.iteritems():
        url = row[1]
        task_queue.put(url)

    start_time = time.perf_counter()

    # Start up the workers.
    workers = []
    for i in range(n_workers):
        p = multiprocessing.Process(target=worker, args=(task_queue, out_queue))
        p.start()
        workers.append(p)

    csv_rows = []
    try:
        while True:
            # https://bugs.python.org/issue20147
            csv_row = out_queue.get(block=True, timeout=3)
            csv_rows.append(csv_row)
    except queue.Empty:
        log('Done!')


    with open(output_file, 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=['url', 'title', 'total_time', 'yields', 'ingredients', 'instructions'],
            quotechar='"',
            quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(csv_rows)

    for p in workers:
        p.terminate()

    print("Runtime: %s (s)" % (time.perf_counter() - start_time))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Scrapes regexes from http://regexlib.com.')
    parser.add_argument(
        '-i',
        '--input_csv',
        help='Relative path of input CSV file containing regex '
        'category and URLs to scrape.',
        required='True')
    parser.add_argument(
        '-o',
        '--output_csv',
        help='Relative path of output CSV file containing '
        'scraped regexes for each category.',
        required='True')
    parser.add_argument(
        '-n',
        '--num_workers',
        help='Number of workers to use.',
        type=int,
        choices=range(1, 64),
        required='True')

    args = parser.parse_args()

    print('Scraping recipes...')

    urls_df = get_urls(args.input_csv)
    main_task(urls_df, args.output_csv, args.num_workers)

    print('Regexes saved at "%s".' % args.output_csv)
