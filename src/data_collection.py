import os
import csv
from datetime import datetime

# Ensure the folder exists
os.makedirs("data/raw", exist_ok=True)

# Simulated dataset of Instagram-style captions
sample_posts = [
    {"caption_id": 1, "caption_text": "Feeling grateful for the little things today ❤️", "post_date": "2025-10-23", "city": "Toronto"},
    {"caption_id": 2, "caption_text": "I'm so tired of pretending everything is okay 😞", "post_date": "2025-10-23", "city": "Ottawa"},
    {"caption_id": 3, "caption_text": "Long walk in the rain. Alone with my thoughts.", "post_date": "2025-10-22", "city": "Hamilton"},
    {"caption_id": 4, "caption_text": "Coffee + books = happiness ☕📚", "post_date": "2025-10-22", "city": "LondonOntario"},
    {"caption_id": 5, "caption_text": "No one understands me anymore.", "post_date": "2025-10-21", "city": "Waterloo"},
    {"caption_id": 6, "caption_text": "Vibing at the park! Sun and peace 🌞", "post_date": "2025-10-21", "city": "Kingston"},
    {"caption_id": 7, "caption_text": "I feel invisible. Like I don’t even exist.", "post_date": "2025-10-20", "city": "Brampton"},
    {"caption_id": 8, "caption_text": "I love this city. I’m proud to be here. 💙", "post_date": "2025-10-20", "city": "Mississauga"}]

# Output file path
output_file = "data/raw/ontario_sample.csv"

# Write to CSV
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["caption_id", "caption_text", "post_date", "city"])
    writer.writeheader()
    for post in sample_posts:
        writer.writerow(post)

print(f"Sample data written to {output_file}")
