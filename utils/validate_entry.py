import re
from datetime import datetime
from time import mktime
def validate_entry(entry):
    guid = entry.get("id")
    author = entry.authors[0].name
    raw_title=entry.get("title","")
    clean_title=re.sub(r'\[.*?\]', '', raw_title, count=1).strip()
    raw_date=entry.get("published_parsed")
    dt_object=datetime.fromtimestamp(mktime(raw_date)).date()
    return {
        "guid":guid,
        "author":author,
        "title": clean_title,
        "date": dt_object,
          }
    
