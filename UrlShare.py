# class for managing shared url data

import shortuuid

from time import time
from google.cloud import firestore

class UrlShare(object):
  def __init__(self, phrase, img_url, search_term, clicks=0):
    self.uuid = shortuuid.uuid()[:10]
    self.created = int(time())
    self.phrase = phrase
    self.img_url = img_url
    self.search_term = search_term
    self.clicks = clicks

    # Initialize Firebase connection
    self.db = firestore.Client(project='genremachine')
    self.collection = self.db.collection(u'shared_urls')
    if self.check_duplicate():
      self.commit()
      print("Saved link")
    else:
      print("picture already in use. Did not save")

  def add_click(self):
    self.clicks += 1
    self.commit()

  def check_duplicate(self):
    duplicate_query = self.collection.where(u'img', u'==', self.img_url).stream()
    if len(duplicate_query) > 0:
      for q in duplicate_query:
        print(f'duplicate: {q.id} => {q.to_dict()}')
      return False
    else:
      return True

  def commit(self):
    self.collection.document(self.uuid).set(
      {
        "phrase":   self.phrase,
        "img":      self.img_url,
        "search":   self.search_term,
        "created":  self.created,
        "clicks":   self.clicks
      }
    )
    return True

  def __repr__(self):
    return (
      f'UrlShare(\
        id={self.id}, \
        created={self.created}, \
        phrase={self.phrase}, \
        search_term={self.search_term}, \
        img_url={self.img_url}, \
        clicks={self.clicks}\
      )'
    )