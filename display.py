dividing_line = "----------------------------------------------------------------------"


def print_param(api_key, engine_id, precision, query):
    print("Parameters:")
    print("Client Key\t= %s" % api_key)
    print("Engine Key\t= %s" % engine_id)
    print("Query\t= %s" % query)
    print("Precision\t= %.1f" % precision)
    print(dividing_line)


def print_webpage(webpage, i):
    print("Result %s" % i)
    print("[")
    print("URL: %s" % webpage['formattedUrl'])
    print("Title: %s" % webpage['title'])
    print("Summary: %s" % webpage['snippet'])
    print("]")
    print(dividing_line)


def print_summary(query, precision, target):
    print("FEEDBACK SUMMARY")
    print("Query: %s" % query)
    print("Precision: %.1f" % precision)
    if precision >= target:
        print("Desired precision reached, done")
    else:
        print("Still below the desired precision of %.1f" % target)
