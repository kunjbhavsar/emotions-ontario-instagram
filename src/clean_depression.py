import json
import pytz
import pandas as pd
from pathlib import Path

#Locate source file
src = Path("Depression.txt")
if not src.exists():
    src = Path("Depression_1000.txt")
if not src.exists():
    raise FileNotFoundError("Put Depression.txt or Depression_1000.txt in your project root.")

#Load JSON lines
records = []
with open(src, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue

#Focused fields
fields = ["author", "created_utc", "edited", "id",
    "num_comments", "num_crossposts", "over_18",
    "score", "subreddit", "subreddit_id", "title", "url"]

df = pd.DataFrame.from_records(records)
existing = [c for c in fields if c in df.columns]
df = df[existing].copy()

#Remove duplicate posts
if "id" in df.columns:
    df.drop_duplicates(subset="id", inplace=True)

#Clean title (use .str.*)
if "title" in df.columns:
    # Ensure string dtype, keep NaN
    df["title"] = df["title"].astype("string")
    # Drop NaN titles
    df = df[df["title"].notna()]
    # Drop blank/whitespace-only titles
    df = df[df["title"].str.strip().ne("")]

#Normalize author placeholders
if "author" in df.columns:
    df["author"] = df["author"].where(~df["author"].isin(["[deleted]", "[removed]"]), None)

#Strong typing for numeric cols
for col in ["score", "num_comments", "num_crossposts"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

#Datetime conversion
if "created_utc" in df.columns:
    df["created_utc"] = pd.to_datetime(df["created_utc"], unit="s", errors="coerce")
    df["created_est"] = df["created_utc"].dt.tz_localize("UTC").dt.tz_convert("America/Toronto")

#Edited -> boolean
if "edited" in df.columns:
    def to_bool(x):
        if isinstance(x, (int, float)):  # edited carries a timestamp
            return True
        if isinstance(x, str):
            return x.strip().lower() == "true"
        return bool(x)
    df["edited"] = df["edited"].apply(to_bool)

#Drop crucial nulls
for col in ["id", "subreddit"]:
    if col in df.columns:
        df = df[df[col].notna()]

#Save output
df.to_csv("Depression_cleaned.csv", index=False, encoding="utf-8")
print("Saved -> Depression_cleaned.csv")
print(df.head(5))
