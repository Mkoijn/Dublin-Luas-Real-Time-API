def luas_list():
    my_list = [line.split() for line in open('luas_stops.txt', 'rb')]
    luas_stops = []
    for stop in my_list:
        stop_dict = {'stop_number': int(stop[0]),
                     'stop_name': stop[1].decode(),
                     'abbr': stop[2].decode(),
                     'lat': float(stop[3]),
                     'lng': float(stop[4])
                     }
        luas_stops.append(stop_dict)
    return luas_stops
