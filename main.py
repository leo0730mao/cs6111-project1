import pprint
import sys
import display
from googleapiclient.discovery import build


def google_search(api_key, engine_id, query):
    service = build("customsearch", "v1",
                    developerKey = api_key)

    res = service.cse().list(
        q = query,
        cx = engine_id,
    ).execute()
    return res


# TODO
def refine_search(q, r):
    if len(r) == 0:
        print("Below desired precision, but can no longer augment the query")
        return q, False


if __name__ == '__main__':
    # if len(sys.argv) != 5:
    #    print("main <google api key> <google engine id> <precision> <query>")
    #    exit(1)
    # api_key = sys.argv[1]
    # engine_id = sys.argv[2]
    # target_precision = float(sys.argv[3])
    # query = sys.argv[4]

    api_key = ""
    engine_id = ""
    target_precision = 0.5
    query = "Milky way"

    while True:
        cur_precision = 0.0
        relevant_webpage = list()
        display.print_param(api_key, engine_id, target_precision, query)
        res = google_search(api_key, engine_id, query)

        print("Google Search Result:")
        print(display.dividing_line)

        for idx, webpage in enumerate(res['items']):
            display.print_webpage(webpage, idx)
            if_relevant = input("Relevant (Y/N)?")
            print(display.dividing_line)

            if if_relevant.lower() == 'y':
                cur_precision += 1
                relevant_webpage.append(webpage)
        cur_precision /= 10

        display.print_summary(query, cur_precision, target_precision)
        if cur_precision < target_precision:
            query, res = refine_search(query, relevant_webpage)
            if res is False:
                exit(0)
        else:
            exit(0)
