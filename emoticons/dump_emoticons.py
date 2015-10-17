#!/usr/bin/env python

# 1-liner
# curl -s 'https://YOUR_HIPCHAT_URL/v2/emoticon?max-results=1000&auth_token=YOUR_AUTH_TOKEN' | python -m json.tool > emoticons.json 

import requests
import json
import logging
import os
import urllib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dump_emoticon_list")

if __name__ == "__main__":
    hipchat_url = "YOUR_HIPCHAT_URL" # default is "https://api.hipchat.com"
    auth_token = "YOUR_TOKEN"
    get_all_emoticons_api_url = hipchat_url + "/v2/emoticon?max-results=1000&auth_token=" + auth_token
    output_filename = "emoticons.json"

    r = requests.get(get_all_emoticons_api_url)
    if r.status_code == requests.codes.ok: # HTTP 200
        with open(output_filename, "w") as f:
            json.dump(r.json(), f, sort_keys=True, indent=4, separators=(',', ': '))
            f.close()
            logger.info("Output written to %s", output_filename)
        items = r.json()["items"]
        for item  in items:
            shortcut = item["shortcut"]
            url = item["url"]
            fname, file_ext = os.path.splitext(url)
            new_fname = "files/" + shortcut + file_ext
            logging.info(new_fname)
            urllib.urlretrieve(url, filename=new_fname)

    else:
        logger.error("Failed to get all hipchat emoticons, Status code = %d", r.status_code)
        logger.error("Response = %s", r.text)
