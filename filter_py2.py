import os, gzip, json, re, ast, traceback, urllib, sys
from datetime import datetime
from preprocessing import preprocessing
def filter(all_news_accounts):
    preprocessor = preprocessing()
    files = os.listdir('tweets')
    all_urls = {}
    all_texts = {}
    bad_urls = []
    for file in files:
        urls = {}
        texts = {}
        str_data = ''
        all_json = []
        with gzip.open('tweets/' + file, 'rb') as f:
            # data = json.loads(f.read())
            # data = json.loads(f.read(), cls=ConcatJSONDecoder)
            str_data = f.readlines()

        for line in str_data:
            line = json.dumps(line)
            all_json.append(json.loads(line))
        for tweet in all_json:
            if not tweet.find('media_url') == -1:
                try:
                    tweet = ast.literal_eval(tweet)
                    if not str(tweet['user']["id"]) in all_news_accounts:
                        continue
                    if tweet['is_quote_status']:
                        continue
                    if 'media' in tweet['entities'] and tweet['entities']['media'][-1]['type'] == 'photo':
                        text = preprocessor.clean(tweet['text'])
                        texts[tweet['id']] = text
                        urls[tweet['id']] = tweet['entities']['media'][-1]['media_url']
                    elif 'media' in tweet['extended_entities'] and tweet['extended_entities']['media'][-1]['type'] == 'photo':
                        text = preprocessor.clean(tweet['text'])
                        texts[tweet['id']] = text
                        urls[tweet['id']] = tweet['extended_entities']['media'][-1]['media_url']
                    else:
                        continue
                except KeyboardInterrupt:
                    print str(datetime.now()) + " program exit\n"
                    raise SystemExit
                except KeyError as e:
                    print str(datetime.now()) + ' ' + str(e) + '\n'
                    traceback.print_exc()
                except Exception as e:
                    print str(datetime.now()) + ' ' + str(e) + '\n'
                    traceback.print_exc()
                    raise SystemExit

        all_urls[file] = urls
        all_texts[file] = texts
    get_photos(all_urls, bad_urls)
    save_texts(all_texts, bad_urls)

def get_photos(all_urls, bad_urls):
    DIR = 'photos'
    if not os.path.exists(DIR):
        os.mkdir(DIR)

    for file in all_urls:
        if all_urls[file]:
            os.mkdir(os.path.join(DIR, file.replace('.json.gz', '')))
            for id in all_urls[file]:
                url = all_urls[file][id]
                index = url.rfind('.')
                back= url[index:]
                try:
                    filename, headers = urllib.urlretrieve(url, filename=os.path.join(DIR, file.replace('.json.gz', ''), str(id)+back))
                except Exception as e:
                    print str(datetime.now()) + ' ' + str(id) + ' ' + str(url) + ' ' + str(e) + '\n'
                    print(traceback.print_exc(file=open("filter.log", "a+")))

def save_texts(all_texts, bad_urls):
    DIR = 'texts'
    if not os.path.exists(DIR):
        os.mkdir(DIR)

    for file in all_texts:
        if all_texts[file]:
            os.mkdir(os.path.join(DIR, file.replace('.json.gz', '')))
            for id in all_texts[file]:
                if str(id) in bad_urls:
                    continue
                text = all_texts[file][id]
                try:
                    with open(os.path.join(DIR, file.replace('.json.gz', ''), str(id) + '.txt'), 'w') as f:
                        f.write(text)
                except Exception as e:
                    print str(datetime.now()) + ' ' + os.path.join(DIR, file.replace('.json.gz', ''), str(id) + '.txt') + ' ' + str(e) + '\n'
                    print(traceback.print_exc(file=open("filter.log", "a+")))

if __name__ == "__main__":
    all_news_accounts = []
    with open('news_accounts.txt', 'r') as f:
         all_news_accounts = f.read().splitlines()
    sys.stdout = open('filter.log', 'a+')
    filter(all_news_accounts)
