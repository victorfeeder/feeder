import feedparser

class RSSReader:
    def __init__(self, url):
        self.url = url
        self.feed = feedparser.parse(url)

    def get_podcast_title(self):
        return self.feed.feed.get("title", "Sem título")

    def get_episodes(self):
        episodes = []
        for entry in self.feed.entries:
            episodes.append({
                "title": entry.title,
                "audio_url": entry.enclosures[0].href if entry.enclosures else None,
                "published": entry.get("published", "Desconhecida")
            })
        return episodes
