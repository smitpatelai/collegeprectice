import requests

url = "https://openlibrary.org/subjects/science_fiction.json"

response = requests.get(url).json()

book = response["works"][0]
book_title = book.get("title", "N/A")
primary_author = book["authors"][0]["name"] if book.get("authors") else "N/A"
first_publication_year = book.get("first_publish_year", "N/A")
edition_count = book.get("edition_count", "N/A")
unique_identifier = book.get("key", "N/A")

print("================BOOK INFORMATION REPORT======================")
print(f"Book Title : {book_title}")
print(f"Primary Author : {primary_author}")
print(f"First Publication Yr : {first_publication_year}")
print(f"Edition Count : {edition_count}")
print(f"Unique Identifier : {unique_identifier}")
print("==================END OF RECORD OUTPUT =======================")
