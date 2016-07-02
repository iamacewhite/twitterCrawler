import os, gzip, json, re, ast, traceback, urllib.request, sys
from datetime import datetime

def filter():
    files = os.listdir('tweets')
    all_urls = {}
    for file in files:
        urls = {}
        str_data = ''
        all_json = []
        with gzip.open('tweets/' + file, 'rb') as f:
            # data = json.loads(f.read())
            # data = json.loads(f.read(), cls=ConcatJSONDecoder)
            str_data = f.readlines()

        for line in str_data:
            line = line.decode()
            line = json.dumps(line)
            all_json.append(json.loads(line))
        for tweet in all_json:
            if not tweet.find('media_url') == -1:
                try:
                    tweet = ast.literal_eval(tweet)
                    if tweet['is_quote_status']:
                        continue
                    if 'media' in tweet['entities'] and tweet['entities']['media'][-1]['type'] == 'photo':
                        urls[tweet['id']] = tweet['entities']['media'][-1]['media_url']
                    elif 'media' in tweet['extended_entities'] and tweet['extended_entities']['media'][-1]['type'] == 'photo':
                        urls[tweet['id']] = tweet['extended_entities']['media'][-1]['media_url']
                    else:
                        continue
                except KeyboardInterrupt:
                    print(str(datetime.now()) + " program exit\n")
                    raise SystemExit
                except KeyError as e:
                    print(str(datetime.now()) + ' ' + str(e) + '\n')
                    traceback.print_exc()
                except Exception as e:
                    print(str(datetime.now()) + ' ' + str(e) + '\n')
                    traceback.print_exc()
                    raise SystemExit

        all_urls[file] = urls
    get_photos(all_urls)

def get_photos(all_urls):
    DIR = 'photos'
    if not os.path.exists(DIR):
        os.mkdir(DIR)

    for file in all_urls:
        os.mkdir(os.path.join(DIR, file.replace('.json.gz', '')))
        for id in all_urls[file]:
            url = all_urls[file][id]
            print(id)
            print(url)
            index = url.rfind('.')
            back= url[index:]
            try:
                filename, headers = urllib.request.urlretrieve(url, filename=os.path.join(DIR, file.replace('.json.gz', ''), str(id)+back))
            except Exception as e:
                print(str(datetime.now()) + ' ' + str(e) + '\n')
                traceback.print_exc()

if __name__ == "__main__":
    sys.stdout = open('filter.log', 'a+')
    filter()
