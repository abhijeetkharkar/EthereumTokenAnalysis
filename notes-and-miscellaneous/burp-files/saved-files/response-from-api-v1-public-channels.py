import sys
import json

def main():
  with open("response-from-api-v1-public-channels.json", "rb") as f:
    pubs = json.load(f)
    total = float(len(pubs))
    print("%s items" % total)
    verified = count_verified(pubs)
    print("Verified & %s& %.1f\\%% \\\\" % (verified, (verified/total)*100))
    print("Unverified & %s& %.1f\\%% \\\\" % (total - verified, ((total-verified)/total)*100))
    excluded = count_excluded(pubs)
    print("Excluded & %s& %.1f\\%% \\\\" % (excluded, (excluded/total)*100))
    has_banner = count_has_banner(pubs)
    print("With banner data & %s& %.1f\\%% \\\\" %  (has_banner, (has_banner/total)*100))
    #print("& %spublishers with description" % count_described(pubs))
    youtube = count_name_prefix(pubs, "youtube#channel:UC")
    print("Youtube & %s& %.1f\\%% \\\\" %  (youtube, (youtube/total)*100))
    twitch = count_name_prefix(pubs, "twitch#author:")
    print("Twitch & %s& %.1f\\%% \\\\" %  (twitch, (twitch/total)*100))
    youtube_extra = count_name_prefix_and_is_verified_with_banner(pubs,"youtube#channel:UC")
    print("Youtube: verified \\& banner & %s& %.1f\\%% \\\\" %  (youtube_extra, (youtube_extra/float(youtube))*100))
    twitch_extra = count_name_prefix_and_is_verified_with_banner(pubs,"twitch#author:")
    print("Twitch: verified \\& banner  Publishers & %s& %.1f\\%% \\\\" %  (twitch_extra, (twitch_extra/float(twitch))*100))
    max_count = 99999
    print_descriptions(pubs, max_count)

def make_banner_items(pubs):
 #            item.verified = i[1].GetBool();
 #        item.excluded = i[2].GetBool();
    result = []
    for x in pubs:
      result.append({
          "name": x[0],
          "verified": x[1],
          "excluded": x[2],
          "banner_data": x[3]
      })

    return result

def count_name_prefix(pubs,prefix):
    i = 0
    for x in pubs:
      if x[0].startswith(prefix):
        i += 1 
    return i

def count_name_prefix_and_is_verified_with_banner(pubs,prefix):
    i = 0
    for x in pubs:
      if x[0].startswith(prefix) and x[3] != {} and x[1]:
        i += 1 
    return i

def count_described(pubs):
    i = 0
    for x in pubs:
      if "title" in x[3] or "description" in x[3]:
        i += 1 
    return i

def count_verified(pubs):
    i = 0
    for x in pubs:
      if x[1]:
        i += 1 
    return i

def count_excluded(pubs):
    i = 0
    for x in pubs:
      if x[2]:
        i += 1 
    return i

def count_has_banner(pubs):
    i = 0
    for x in pubs:
      if x[3] != {}:
        i += 1 
    return i

def print_banner_items(pubs, max_count):
    i = 0
    for h in make_banner_items(pubs):
      if i > max_count:
        break
      print("%s: %r" % (i, h))
      i += 1

def print_banner_items_non_null(pubs, max_count):
    i = 0
    for h in make_banner_items(pubs):
      if h["banner_data"] == {}:
        continue
      if i > max_count:
        break
      print("%s: %r" % (i, h))
      i += 1

def print_descriptions(pubs, max_count):
    i = 0
    for h in make_banner_items(pubs):
      if h["banner_data"] == {}:
        continue
      if i > max_count:
        break
      print("%s: %r: %r::%r" % (i, h["name"], h["banner_data"]["title"], h["banner_data"]["description"]))
      i += 1
      
def print_items(pubs, max_count):
    i = 0
    for x in pubs:
      if i > max_count:
        break
      print("%s: %r" % (i, x))
      i += 1


def print_names(pubs, max_count):
    i = 0
    for x in pubs:
      if i > max_count:
        break
      print("%s: %r" % (i, x[0]))
      i += 1

main()
