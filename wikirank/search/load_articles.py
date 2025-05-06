import os
import json
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wikirank.settings")
django.setup()

from search.models import Article

with open("pagerank_top100.json", "r") as f:
    for line in f:
        row = json.loads(line)
        Article.objects.create(title=row["id"], pagerank=row["pagerank"])
