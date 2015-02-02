#!/usr/bin/python
from future import Future
import feedparser
import os, time
import pprint

# list of feeds to pull down
hit_list = [
    "http://www.yourwebsite.nl/1/feed/",
    "http://www.yourwebsite.nl/2/feed/",
    "http://www.yourwebsite.nl/3/feed/",
    "http://www.yourwebsite.nl/4/feed/",
    "http://www.yourwebsite.nl/5/feed/",
    "http://www.yourwebsite.nl/6/feed/"]

# list of program names
programs = [
    "Feed 1",
    "Feed 2",
    "Feed 3",
    "Feed 4",
    "Feed 5",
    "Feed 6"]

# list of program names
images = [
    "http://placehold.it/66x66",
    "http://placehold.it/66x66",
    "http://placehold.it/66x66",
    "http://placehold.it/66x66",
    "http://placehold.it/66x66",
    "http://placehold.it/66x66"]

# pull down all feeds
future_calls = [Future(feedparser.parse,rss_url) for rss_url in hit_list]

# block until they are all in
feeds = [future_obj() for future_obj in future_calls]

entries = []
for feed in feeds:
    entries.extend( feed[ "items" ] )

# sort by publication date, published_parsed works better than published
sorted_entries = sorted(entries, key=lambda entry: entry["published_parsed"])
sorted_entries.reverse() # for most recent entries first

# trim to 10 entris
del sorted_entries[10:]

# set timezone
os.environ['TZ'] = 'Europe/Amsterdam'
time.tzset()

# save file
f = open('blogposts.xml', 'w')

f.write('<?xml version="1.0" encoding="utf-8"?>' + '\n')
f.write('<rss version="2.0">' + '\n')
f.write('<channel>' + '\n')
f.write('  <title>Radio Veronica Blogposts</title>' + '\n')
f.write('  <link>http://radioveronica.nl</link>' + '\n')
f.write('  <description>Radio Veronica Blogposts</description>' + '\n')
f.write('  <lastBuildDate>' + time.strftime('%a, %d %b %Y %H:%M:%S %z') + '</lastBuildDate>' + '\n')
f.write('  <language>nl-nl</language>' + '\n')

for blogpost in sorted_entries :
    feedId = hit_list.index(blogpost['content'][0]['base'])
    title = blogpost['title']
    description = blogpost['description']
    link = blogpost['link']
    pubDate = blogpost['published']

    f.write('  <item>' + '\n')
    f.write('    <category>' + programs[feedId].encode('utf-8') + '</category>\n')
    f.write('    <title>' + title.encode('utf-8') + '</title>' + '\n')
    f.write('    <description><![CDATA[' + description.encode('utf-8') + ']]></description>' + '\n')
    f.write('    <enclosure url="' + images[feedId].encode('utf-8') + '" length="1234" type="image/jpg" />\n')
    f.write('    <link>' + link.encode('utf-8') + '</link>' + '\n')
    f.write('    <pubDate>' + pubDate.encode('utf-8') + '</pubDate>' + '\n')
    f.write('  </item>' + '\n')
f.write('</channel>' + '\n')
f.write('</rss>')
