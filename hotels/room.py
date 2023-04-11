class Room:
    def __init__(self, rooms):
        self.rooms = rooms

    def construct_room(self):
        hotel_rooms = []
        try:
            for room in self.rooms[0]['offers']:
                offer = {}
                offer['price'] = room['price']['total']
                offer['description'] = room['room']['description']['text']
                offer['offerID'] = room['id']
                offer['category'] = room['room']['typeEstimated']['category']
                offer['beds'] = room['room']['typeEstimated']['beds']
                offer['bedType'] = room['room']['typeEstimated']['bedType']
                offer['stayFrom'] = room['checkInDate']
                offer['stayTo'] = room['checkOutDate']
                offer['guests'] = room['guests']['adults']
                hotel_rooms.append(offer)
        except (TypeError, AttributeError, KeyError):
            pass
        return hotel_rooms