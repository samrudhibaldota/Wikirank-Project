from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import json

# Start Spark session with GraphFrames support
spark = SparkSession.builder \
    .appName("WikipediaPageRankFull") \
    .config("spark.jars", "/Users/samrudhibaldota/jars/graphframes-0.8.1-spark3.0-s_2.12.jar") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Load parsed Wikipedia articles
rdd = spark.sparkContext.textFile("wiki_parsed.json")
parsed = rdd.map(lambda line: json.loads(line))

# Create edges from links
edges = parsed.flatMap(
    lambda row: [(row['title'], link) for link in row.get('links', []) if row['title'] != link]
)
edges_df = edges.toDF(["src", "dst"])

# Create vertices from unique article titles
vertices_df = (
    edges_df.select("src")
    .union(edges_df.select("dst"))
    .distinct()
    .withColumnRenamed("src", "id")
)

# Import and build GraphFrame
from graphframes import GraphFrame
g = GraphFrame(vertices_df, edges_df)

# Run PageRank with 10 iterations
results = g.pageRank(resetProbability=0.15, maxIter=10)

# Save ALL PageRank scores to disk
results.vertices.orderBy(col("pagerank").desc()) \
    .write \
    .json("pagerank_results")

print("✅ DONE: Full PageRank results saved to 'pagerank_results/'")

