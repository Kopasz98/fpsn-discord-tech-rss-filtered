# -*- coding: utf-8 -*-
import feedparser
import requests
import json
import os
import hashlib

WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

RSS_FEEDS = [
"https://techcrunch.com/feed/",
"https://www.theverge.com/rss/index.xml",
"https://www.wired.com/feed/rss",
"https://feeds.arstechnica.com/arstechnica/index",
"https://www.engadget.com/rss.xml",
"https://mashable.com/feeds/rss/tech",
"https://gizmodo.com/rss",
"https://www.digitaltrends.com/feed/",
"https://www.zdnet.com/news/rss.xml",
"https://venturebeat.com/feed/",
"https://rss.slashdot.org/Slashdot/slashdot",
"https://www.fastcompany.com/technology/rss",
"https://www.axios.com/technology/rss",
"https://www.technologyreview.com/feed/",
"https://spectrum.ieee.org/rss",
"https://www.tomsguide.com/feeds/all",
"https://www.cnet.com/rss/all/",
"https://www.pcmag.com/feeds/rss",
"https://www.howtogeek.com/feed/",
"https://www.extremetech.com/feed",

"https://news.ycombinator.com/rss",
"https://www.infoq.com/feed/",
"https://www.theregister.com/headlines.atom",
"https://stackoverflow.blog/feed/",
"https://dev.to/feed",
"https://www.smashingmagazine.com/feed/",
"https://css-tricks.com/feed/",
"https://dzone.com/feed",
"https://blog.cloudflare.com/rss/",
"https://developers.googleblog.com/feeds/posts/default",

"https://www.artificialintelligence-news.com/feed/",
"https://www.aitrends.com/feed/",
"https://syncedreview.com/feed/",
"https://openai.com/blog/rss/",
"https://deepmind.google/blog/rss.xml",
"https://towardsdatascience.com/feed",
"https://www.kdnuggets.com/feed",
"https://www.analyticsvidhya.com/feed/",
"https://machinelearningmastery.com/blog/feed/",

"https://krebsonsecurity.com/feed/",
"https://thehackernews.com/feeds/posts/default",
"https://www.bleepingcomputer.com/feed/",
"https://www.darkreading.com/rss.xml",
"https://threatpost.com/feed/",
"https://www.securityweek.com/rss",
"https://www.schneier.com/feed/atom/",

"https://www.hwsw.hu/xml/rss.xml",
"https://prohardver.hu/hirfolyam/rss.html",
"https://itcafe.hu/hirfolyam/rss.html",
"https://bitport.hu/rss",
"https://sg.hu/rss",
"https://pcworld.hu/rss",
"https://techkalauz.hu/rss",
"https://raketa.hu/rss",
"https://ipon.hu/magazin/rss",

"https://www.gsmarena.com/rss-news-reviews.php3",
"https://www.androidauthority.com/feed",
"https://9to5google.com/feed/",
"https://www.macrumors.com/macrumors.xml",
"https://www.anandtech.com/rss/",

]

INCLUDE_KEYWORDS = [k.lower() for k in [
  "Samsung","ROG","Ally","Leica","Lenovo",
  "Legion","iOS","Iphone","Ipad",
  "Apple","watchOS","Steam","Logitech",
  "Nintendo","Switch","Sony","Playstation",
  "PS5","WWDC","Corsair","Razer","Windows",
  "Asus","Huawei","Nvidia","AMD",
]]

EXCLUDE_KEYWORDS = [k.lower() for k in [
    "rumor", "leak", "unconfirmed",
    "giveaway", "free skins",
    "sale", "discount",
    "top 10", "best of",
    "opinion", "editorial","walmart","deals",
]]

POSTED_FILE = "posted.json"


def is_relevant(entry):
    text = (
        entry.get("title", "") +
        " " +
        entry.get("summary", "")
    ).lower()

    if not any(keyword in text for keyword in INCLUDE_KEYWORDS):
        return False

    if any(keyword in text for keyword in EXCLUDE_KEYWORDS):
        return False

    return True


def entry_id(entry):
    base = entry.get("id") or entry.get("link") or entry.get("title", "")
    return hashlib.sha256(base.encode("utf-8")).hexdigest()


posted = set()
if os.path.exists(POSTED_FILE):
    try:
        with open(POSTED_FILE, "r", encoding="utf-8") as f:
            posted = set(json.load(f))
    except Exception:
        posted = set()

new_posts = []

for feed_url in RSS_FEEDS:
    feed = feedparser.parse(feed_url)

    for entry in feed.entries[:5]:
        if not is_relevant(entry):
            continue

        eid = entry_id(entry)
        if eid in posted:
            continue

        new_posts.append({
            "title": entry.title,
            "link": entry.link
        })

        posted.add(eid)

for post in new_posts:
    data = {
        "content": f"🎮 **{post['title']}**\n{post['link']}"
    }
    requests.post(WEBHOOK_URL, json=data)

with open(POSTED_FILE, "w") as f:
    json.dump(list(posted), f)
