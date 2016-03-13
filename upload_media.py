#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import shutil
import glob
import random
from requests_oauthlib import OAuth1Session

keys = []
#with open('./password.txt', 'r') as file:
with open(sys.argv[1], 'r') as file:
  for line in file:
    if line.startswith('#'):
      continue
    keys.append(line.strip())

CK = keys[0]
CS = keys[1]
AT = keys[2]
AS = keys[3]

url_media = "https://upload.twitter.com/1.1/media/upload.json"
url_text = "https://api.twitter.com/1.1/statuses/update.json"

# OAuth認証 セッションを開始
twitter = OAuth1Session(CK, CS, AT, AS)

# 画像投稿
filess = glob.glob("/home/pi/app/Tweet/now/*.*")
r     = random.randint(1, len(filess))
count = 0

for file in filess:
  count += 1
  if count != r:
    continue
  print(file)
  files = {"media" : open(file, 'rb')}
  req_media = twitter.post(url_media, files = files)

  # レスポンスを確認
  if req_media.status_code != 200:
    print ("画像アップデート失敗: %s", req_media.text)
    exit()

  # Media ID を取得
  media_id = json.loads(req_media.text)['media_id']
  print ("Media ID: %d" % media_id)
  break

# Media ID を付加してテキストを投稿
params = {"status": "【自動投稿】", "media_ids": media_id}
req_media = twitter.post(url_text, params = params)

# 再びレスポンスを確認
if req_media.status_code != 200:
  print("text update failed: %s", req_media.text)
  exit()

# doneディレクトリに移動
shutil.move(file, "/home/pi/app/Tweet/done/")
print ("OK")
