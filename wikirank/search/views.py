# from django.shortcuts import render
# from .models import Article

# def search_articles(request):
#     query = request.GET.get("q", "")
#     results = []

#     if query:
#         results = Article.objects.filter(title__icontains=query).order_by("-pagerank")[:10]

#     return render(request, "search.html", {
#         "query": query,
#         "results": results
#     })


# from django.shortcuts import render
# from django.db.models import Q
# from .models import Article

# def search_articles(request):
#     query = request.GET.get("q", "").strip()
#     results = []

#     if query:
#         results = Article.objects.filter(Q(title__icontains=query)).order_by("-pagerank")

#     return render(request, "search.html", {"results": results, "query": query})


# from django.shortcuts import render
# from .models import Article
# from django.db.models import Q

# def search_articles(request):
#     query = request.GET.get("q", "").strip()
#     results = []

#     if query:
#         keywords = query.lower().split()
#         q_objects = Q()
#         for word in keywords:
#             q_objects |= Q(title__icontains=word)
#         results = Article.objects.filter(q_objects).order_by("-pagerank")

#     return render(request, "search.html", {"results": results, "query": query})

# 


# from django.shortcuts import render
# from .models import Article
# from rapidfuzz import fuzz, process
# from nltk.corpus import stopwords

# STOPWORDS = set(stopwords.words("english"))

# def search_articles(request):
#     query = request.GET.get("q", "").strip()
#     results = []

#     if query:
#         words = query.lower().split()
#         keywords = [w for w in words if w not in STOPWORDS]
#         if not keywords:
#             keywords = words

#         # Load all titles from DB
#         all_articles = list(Article.objects.all().values("id", "title", "pagerank"))

#         # Flatten keywords into a single string for matching
#         search_string = " ".join(keywords)

#         # Fuzzy match top 10 results by ratio score
#         matches = process.extract(
#             search_string,
#             [article["title"] for article in all_articles],
#             scorer=fuzz.token_sort_ratio,
#             limit=10,
#             score_cutoff=80
#         )

#         matched_titles = [match[0] for match in matches]

#         # Filter original DB entries
#         results = sorted(
#             [a for a in all_articles if a["title"] in matched_titles],
#             key=lambda x: x["pagerank"],
#             reverse=True
#         )

#     return render(request, "search.html", {"results": results, "query": query})



# from django.shortcuts import render
# from .models import Article
# from rapidfuzz import fuzz, process
# from nltk.corpus import stopwords

# STOPWORDS = set(stopwords.words("english"))

# def search_articles(request):
#     query = request.GET.get("q", "").strip()
#     results = []

#     if query:
#         words = query.lower().split()
#         keywords = [w for w in words if w not in STOPWORDS]
#         if not keywords:
#             keywords = words

#         search_string = " ".join(keywords).lower()

#         all_articles = list(Article.objects.all().values("id", "title", "pagerank"))
#         title_map = {article["title"].lower(): article for article in all_articles}
#         all_titles = list(title_map.keys())

#         matches = process.extract(
#             search_string,
#             all_titles,
#             scorer=fuzz.token_sort_ratio,
#             limit=10,
#             score_cutoff=80
#         )

#         matched_titles = [match[0] for match in matches]
#         results = sorted(
#             [title_map[title] for title in matched_titles],
#             key=lambda x: x["pagerank"],
#             reverse=True
#         )

#     return render(request, "search.html", {"results": results, "query": query})


from django.shortcuts import render
from .models import Article
from django.db.models import Q
from nltk.corpus import stopwords

# Load English stopwords
STOPWORDS = set(stopwords.words("english"))

def search_articles(request):
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        words = query.lower().split()
        keywords = [word for word in words if word not in STOPWORDS]

        # Fallback: if all were stopwords, use full query
        if not keywords:
            keywords = words

        q_objects = Q()
        for word in keywords:
            q_objects |= Q(title__icontains=word)

        results = Article.objects.filter(q_objects).order_by("-pagerank")

    return render(request, "search.html", {"results": results, "query": query})
