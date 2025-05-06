import os
import sys
import json
import django

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wikirank.settings")
django.setup()

from search.models import Article

# Clear existing articles
Article.objects.all().delete()

# Load new articles from the top 100 PageRank file
with open("pagerank_top100.json", "r") as f:
    for line in f:
        row = json.loads(line)
        Article.objects.create(title=row["id"], pagerank=row["pagerank"])

print("✅ Loaded top 100 articles into the database.")

