#!/usr/bin/python

# from pynput import keyboard
#
# break_script = False
# def on_press(key):
#     global break_script
#     if key == keyboard.Key.end:
#         print('Ending....')
#         if result_count == 1:
#             print(bcolors.WARNYellow + "Got %d result" % result_count + bcolors.RESET)
#             csvfile.close()
#             print(bcolors.WARNYellow + "Saved to ", outfile + bcolors.RESET)
#         elif result_count == 0:
#             print(
#                 bcolors.WARNYellow + "Didn't get any results try another Latitude and  Longitude" + bcolors.RESET)
#         else:
#             print(bcolors.WARNYellow + "Got %d results" % result_count + bcolors.RESET)
#             csvfile.close()
#             print(bcolors.WARNYellow + "Saved to ", outfile + bcolors.RESET)
#         # break_script = True
#         idfile.close()
#         csvfile.close()
#         exit(5)


try:
    from cffi.setuptools_ext import execfile
    from twitter import *
    import sys
    import csv
    import time
    import os


    class bcolors:
        RESET = '\033[0m'  # Reset
        BOLD = '\033[1m'  # Bold
        UNDERLINE = '\033[4m'  # Underline
        FAILRed = '\033[91m'  # Light Red
        OKGreen = '\033[92m'  # Light Green
        WARNYellow = '\033[93m'  # Light Yellow
        OKBlue = '\033[94m'  # Light Blue
        HEADER = '\033[95m'  # Light Magenta


    os.system('cls')
    print(' ')
    print()

    # latitude =  float(input(bcolors.OKGreen + 'Latitude(WGS-84): ' + bcolors.RESET))
    # longitude = float(input(bcolors.OKGreen + 'Longitude(WGS-84): ' + bcolors.RESET))
    # max_range = float(input(bcolors.OKGreen + 'Radius(km): ' + bcolors.RESET))
    # num_results = int(input(bcolors.OKGreen + 'Number of results: ' + bcolors.RESET))

    # TEST Case 1
    print(bcolors.OKGreen + 'Testing.... Location Boulder' + bcolors.RESET)
    latitude = float(40.0160921)
    longitude = float(-105.2812196)
    max_range = float(1)
    num_results = 50

    outfile = "output.csv"
    known_id = "IDLog.csv"

    config = {}
    execfile("conf.txt", config)

    twitter = Twitter(auth=OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

    file_exists1 = os.path.isfile("output.csv")
    file_exists2 = os.path.isfile("IDLog.csv")

    csvfile = open(outfile, 'a')
    csvwriter = csv.writer(csvfile)
    idfile = open(known_id, "a")
    idwriter = csv.writer(idfile)

    if (file_exists1 is not True):
        row = ["Username", "Profile URL", "Latitude", "Longitude", "Google Maps", "Tweet"]
        csvwriter.writerow(row)
    else:
        row = ["------------------------------------------------------------------------"]
        csvwriter.writerow(row)
    if (file_exists2 is not True):
        idrow = ["ID"]
        csvwriter.writerow(idrow)

    result_count = 0
    while result_count < num_results:
        query = twitter.search.tweets(q="", geocode="%f,%f,%dkm" % (latitude, longitude, max_range), num_results=100)
        for result in query["statuses"]:
            # only process a result if it has a geolocation
             if result["geo"]:
            #     with open(known_id) as f:
            #         for line in f:
            #             if line in result:
            #                 continue
            #             else:
            #                 idRow = str(result["id"])
            #                 idwriter.writerow(idRow)
            #
            #         else:
                        user = result["user"]["screen_name"]
                        text = result["text"]
                        text = text.encode('ascii', 'replace')
                        latitude = result["geo"]["coordinates"][0]
                        longitude = result["geo"]["coordinates"][1]
                        url = 'https://twitter.com/%s' % user
                        gurl = 'https://maps.google.com/?q=' + str(latitude) + ',' + str(longitude)

                        row = [user, url, latitude, longitude, gurl, text]
                        print('-----------------------------------------------------------------')
                        print(' ')
                        print(bcolors.OKGreen + 'Username:    ' + bcolors.RESET, user)
                        print(bcolors.OKGreen + 'Profile URL: ' + bcolors.RESET, url)
                        print(bcolors.OKGreen + 'Latitude:    ' + bcolors.RESET, latitude)
                        print(bcolors.OKGreen + 'Longitude:   ' + bcolors.RESET, longitude)
                        print(bcolors.OKGreen + 'Google Maps: ' + bcolors.RESET, gurl)
                        print(bcolors.OKGreen + 'Tweet:       ' + bcolors.RESET, text)
                        print(' ')
                        csvwriter.writerow(row)
                        result_count += 1
                        time.sleep(5.05)    # Rate limit padding < 15 minute window

    if result_count == 1:
        print(bcolors.WARNYellow + "Got %d result" % result_count + bcolors.RESET)
        csvfile.close()
        print(bcolors.WARNYellow + "Saved to ", outfile + bcolors.RESET)
    elif result_count == 0:
        print(bcolors.WARNYellow + "Didn't get any results try another Latitude and  Longitude" + bcolors.RESET)
    else:
        print(bcolors.WARNYellow + "Got %d results" % result_count + bcolors.RESET)
        csvfile.close()
        print(bcolors.WARNYellow + "Saved to ", outfile + bcolors.RESET)

except ImportError:
    print('''Install the requirements''')