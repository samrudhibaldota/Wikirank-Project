import json
import glob

files = glob.glob("pagerank_results/part-*.json")
all_rows = []

for file in files:
    with open(file, "r") as f:
        for line in f:
            all_rows.append(json.loads(line))

# Sort by PageRank descending
all_rows.sort(key=lambda x: x["pagerank"], reverse=True)

# Write top 100 to JSON
with open("pagerank_top100.json", "w") as out:
    for row in all_rows[:100]:
        json.dump(row, out)
        out.write("\n")

print("✅ Saved top 100 to pagerank_top100.json")

