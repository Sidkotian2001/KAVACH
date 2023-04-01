from script import alerter

def main():
    # number = input("Enter phone number (including country code): ")
    location = input("Enter location: ")
    threat_level = input("Enter threat level: ")
    threat_class = input("Enter threat class: ")

    obj = alerter()
    obj.send_msg(location, threat_level, threat_class)

    # if threat_class == 'Arson' or threat_class == 'RoadAccidents':
    #     obj.send_fire_msg(location, threat_level, threat_class)

if __name__ == '__main__':
    main()