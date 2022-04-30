from tkinter import *
import requests
import json
from  tkinter import ttk
import numpy as np
import copy 

'''
####### The code below was referred from 
# https://www.geeksforgeeks.org/generic-tree-level-order-traversal/
'''
class Node:
  def __init__(self, key):
    self.key = key
    self.child = []
def newNode(key):
  temp = Node(key)
  return temp
'''
###################################
'''


def search_UI():
    root = Tk()
    root.geometry('1500x1500')
    root.title("Flight Search System")

    root.columnconfigure(0, weight=1)
    title = Label(root, text = "Flight Search System", font=('Chalkboard 30')).grid(row=0,  columnspan= 2, sticky="ew")
    bander = Label(root, text = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", font=('Chalkboard 15')).grid(row=1,columnspan= 2, sticky="ew")

    label1 = Label(root, text = "Departure Date: ", font=('Chalkboard 20')).grid(row=2, column = 0, sticky="w")
    input_date = Entry(root, font = ('Chalkboard 20') )
    input_date.insert(0, "2022-06-17")
    input_date.grid(row=2, column=1)

    label2 = Label(root, text = "Origin: ", font=('Chalkboard 20')).grid(row=3, column = 0, sticky="w")
    input_origin = Entry(root, font = ('Chalkboard 20') )
    input_origin.insert(0, "CHI")
    input_origin.grid(row=3, column=1)

    label3 = Label(root, text = "Destination: ", font=('Chalkboard 20')).grid(row=4, sticky="w")
    input_destination = Entry(root, font = ('Chalkboard 20') )
    input_destination.insert(0, "NYC")
    input_destination.grid(row=4, column=1)

    label4 = Label(root, text = "Class: ", font=('Chalkboard 20')).grid(row=5, column = 0, sticky="w")
    options = ["Economy", "Premium Economy", "Business","First Class"]
    class_choice = StringVar()
    class_choice.set("Choose a cabin class type")
    drop = OptionMenu(root, class_choice, *options ).grid(row=5, column = 1, sticky="w")


    label6 = Label(root, text = "Number of Passenger: ", font=('Chalkboard 20')).grid(row=6, column = 0, sticky="w")
    options = ["1", "2", "3", "4", "5", "6", "7"]
    passenger_choice = StringVar()
    passenger_choice.set("Choose the number of passages")
    drop = OptionMenu(root, passenger_choice, *options ).grid(row=6, column = 1, sticky="w")

    label7 = Label(root, text = "Optional: sort by ", font=('Chalkboard 20')).grid(row=7, column = 0, sticky="w")
    options = ["departure time", "arrival time", "total price", "flight durations"]
    sort_choice = StringVar()
    drop = OptionMenu(root, sort_choice, *options).grid(row=7, column =1)

    options = ["from low to high", "from high to low"]
    direction_choice = StringVar()
    drop = OptionMenu(root, direction_choice, *options).grid(row=7, column=2)

    def search_click():
        date = input_date.get()
        origin = input_origin.get()
        destination = input_destination.get()
        class_ = class_choice.get()
        passenger = passenger_choice.get()
        #print((date, origin, destination, class_, passenger))
        response = search_api(departure_date = date, origin=origin, destination = destination, class_type = class_, number_of_passengers = passenger)
        extra_info(response)

        for widget in root.winfo_children():
            widget.destroy()
        
        '''
        The code in this section was modified from https://pythonguides.com/python-tkinter-table-tutorial/
        *******************************************************************************
        '''
        game_frame = Frame(root)
        game_frame.pack()
        game_scroll = Scrollbar(game_frame)
        game_scroll.pack(side=RIGHT, fill=Y)

        my_game = ttk.Treeview(game_frame,yscrollcommand=game_scroll.set, xscrollcommand =game_scroll.set)
        my_game.config(height=30)
        my_game.pack()
        game_scroll.config(command=my_game.yview)
        game_scroll.config(command=my_game.xview)
        my_game['columns'] = ('flight_number', 'departure_time', 'arrival_time', 'departure_airport', 'arrival_airport', "flight_duration", "total_price")
        my_game.column("#0", width=0,  stretch=NO)
        my_game.column("flight_number",anchor=CENTER, width=200)
        my_game.column("departure_time",anchor=CENTER,width=200)
        my_game.column("arrival_time",anchor=CENTER,width=200)
        my_game.column("departure_airport",anchor=CENTER,width=200)
        my_game.column("arrival_airport",anchor=CENTER,width=200)
        my_game.column("flight_duration",anchor=CENTER,width=200)
        my_game.column("total_price",anchor=CENTER,width=200)

        my_game.heading("#0",text="",anchor=CENTER)
        my_game.heading("flight_number",text="Flight Number",anchor=CENTER)
        my_game.heading("departure_time",text="Departure Date and Time",anchor=CENTER)
        my_game.heading("arrival_time",text="Arrival Date and Time",anchor=CENTER)
        my_game.heading("departure_airport",text="Departure Airport",anchor=CENTER)
        my_game.heading("arrival_airport",text="Arrival Airport",anchor=CENTER)
        my_game.heading("flight_duration",text="Flight Duration",anchor=CENTER)
        my_game.heading("total_price",text="Total Price/person",anchor=CENTER)

        search_data = open("flight_data.json")
        search_data = json.load(search_data)

        '''
        Sort the search results based on users' inputs
        '''
        if sort_choice.get() != "" and direction_choice.get() != "":
            search_data = sort_flight(search_data = search_data, criteria= sort_choice.get(), direction = direction_choice.get())

        count = 0
        for i in search_data.keys():
            flight_dict = search_data[i]
            depart_date_time = flight_dict["departure time"][0:10] + " " + flight_dict["departure time"][11:19]
            arrive_date_time = flight_dict["arrival time"][0:10] + " " + flight_dict["arrival time"][11:19]
            depart_city_airport = origin + " " + flight_dict["departure airport"]
            arrive_city_airport = destination + " " + flight_dict["arrival airport"]
            aFlight_info = [i, depart_date_time, arrive_date_time, depart_city_airport, arrive_city_airport, str(flight_dict["flight durations"]) + " minutes", "USD" + str(flight_dict["total price"])]
          

            my_game.insert(parent='',index='end',iid=count,text='', values=aFlight_info)
            count += 1
        my_game.pack()
        '''
        *******************************************************************************
        '''

        af_label = Label(root, text = "Advanced Filter", font=('Chalkboard 20'))
        af_label.pack()

        filter_price_options = ["Above the average price", "Below the average price"]
        filter_price_choice = StringVar()
        menu = OptionMenu(root, filter_price_choice, *filter_price_options)
        menu.pack(expand=True)
 

        filter_time_options = ["Late night flights (depart between 12am - 6am)", 
                                "Morning flights (depart between 6am - 12pm)",
                                "Afternoon flights (depart between 12pm - 6pm)",
                                "Evening flights (depart between 6pm - 12am)"]
        filter_time_choice = StringVar()
        menu = OptionMenu(root, filter_time_choice, *filter_time_options)
        menu.pack(expand= True)



        def fliter_click():
            '''
            Put the search result data into a tree
            '''
            rootNode = newNode("departure_time")
            (rootNode.child).append(newNode("late_night"))
            (rootNode.child).append(newNode("morning"))
            (rootNode.child).append(newNode("afternoon"))
            (rootNode.child).append(newNode("evening"))
            root_children = rootNode.child

            for i in root_children:
                (i.child).append(newNode("price<avg"))
                (i.child).append(newNode("price>=avg"))

            prices = np.array([search_data[i]["total price"] for i in search_data.keys()])

            avg_price = sum(prices)/len(prices)

            for i in search_data.keys():
                depart_time = search_data[i]['departure time'][11:16]  
                minutes = int(depart_time[0:2]) * 60 + int(depart_time[3:5]) 
                if minutes < 360:
                    if search_data[i]["total price"] < avg_price:
                        ((root_children[0].child)[0].child).append(i)
                    else:
                        ((root_children[0].child)[1].child).append(i)

                elif minutes >= 360 and minutes < 720:
                    if search_data[i]["total price"] < avg_price:
                        ((root_children[1].child)[0].child).append(i)
                    else:
                        ((root_children[1].child)[1].child).append(i)
                elif minutes >= 720 and minutes < 1080:
                    if search_data[i]["total price"] < avg_price:
                        ((root_children[2].child)[0].child).append(i)
                    else:
                        ((root_children[2].child)[1].child).append(i)
                elif minutes >= 1080:
                    if search_data[i]["total price"] < avg_price:
                        ((root_children[3].child)[0].child).append(i)
                    else:
                        ((root_children[3].child)[1].child).append(i)

            '''
            Traverse the tree based on filter requirements (price and time) and get the desired results
            '''
            time_choice = filter_time_choice.get()            
            price_choice = filter_price_choice.get()
            filtered_flights = []

            if time_choice == "Late night flights (depart between 12am - 6am)":
                if price_choice == "Below the average price":
                    filtered_flights = root_children[0].child[0].child
                else:
                    filtered_flights = root_children[0].child[1].child
            elif time_choice == "Morning flights (depart between 6am - 12pm)":
                if price_choice == "Below the average price":
                    filtered_flights = root_children[1].child[0].child
                else:
                    filtered_flights = root_children[1].child[1].child
            elif time_choice == "Afternoon flights (depart between 12pm - 6pm)":
                if price_choice == "Below the average price":
                    filtered_flights = root_children[2].child[0].child
                else:
                    filtered_flights = root_children[2].child[1].child
            elif time_choice == "Evening flights (depart between 6pm - 12am)":
                if price_choice == "Below the average price":
                    filtered_flights = root_children[3].child[0].child
                else:
                    filtered_flights = root_children[3].child[1].child

            '''
            Clear the frame and display the filtered results 
            '''
            for widget in root.winfo_children():
                widget.destroy()
            game_frame = Frame(root)
            game_frame.pack()
            game_scroll = Scrollbar(game_frame)
            game_scroll.pack(side=RIGHT, fill=Y)

            my_game = ttk.Treeview(game_frame,yscrollcommand=game_scroll.set, xscrollcommand =game_scroll.set)
            my_game.config(height=30)
            my_game.pack()
            game_scroll.config(command=my_game.yview)
            game_scroll.config(command=my_game.xview)
            my_game['columns'] = ('flight_number', 'departure_time', 'arrival_time', 'departure_airport', 'arrival_airport', "flight_duration", "total_price")
            my_game.column("#0", width=0,  stretch=NO)
            my_game.column("flight_number",anchor=CENTER, width=200)
            my_game.column("departure_time",anchor=CENTER,width=200)
            my_game.column("arrival_time",anchor=CENTER,width=200)
            my_game.column("departure_airport",anchor=CENTER,width=200)
            my_game.column("arrival_airport",anchor=CENTER,width=200)
            my_game.column("flight_duration",anchor=CENTER,width=200)
            my_game.column("total_price",anchor=CENTER,width=200)

            my_game.heading("#0",text="",anchor=CENTER)
            my_game.heading("flight_number",text="Flight Number",anchor=CENTER)
            my_game.heading("departure_time",text="Departure Date and Time",anchor=CENTER)
            my_game.heading("arrival_time",text="Arrival Date and Time",anchor=CENTER)
            my_game.heading("departure_airport",text="Departure Airport",anchor=CENTER)
            my_game.heading("arrival_airport",text="Arrival Airport",anchor=CENTER)
            my_game.heading("flight_duration",text="Flight Duration",anchor=CENTER)
            my_game.heading("total_price",text="Total Price/person",anchor=CENTER)

            count = 0
            for i in search_data.keys():
                if i in filtered_flights:
                    flight_dict = search_data[i]
                    depart_date_time = flight_dict["departure time"][0:10] + " " + flight_dict["departure time"][11:19]
                    arrive_date_time = flight_dict["arrival time"][0:10] + " " + flight_dict["arrival time"][11:19]
                    depart_city_airport = origin + " " + flight_dict["departure airport"]
                    arrive_city_airport = destination + " " + flight_dict["arrival airport"]
                    aFlight_info = [i, depart_date_time, arrive_date_time, depart_city_airport, arrive_city_airport, str(flight_dict["flight durations"]) + " minutes", "USD" + str(flight_dict["total price"])]
                    my_game.insert(parent='',index='end',iid=count,text='', values=aFlight_info)
                    count += 1
            my_game.pack()

        ###### Advanced Filter
        ## Users are able to filter flights that are either lower or higher than the average prices, and select flights of a time slot (late night, morning, afternoon, or evening flights)
        filter_button = Button(root, text = "Apply Filter", command = fliter_click)
        filter_button.pack(expand= True)



    search_buton = Button(root, text = "Search Flights", command = search_click).grid(row = 8, columnspan = 2)

    
    

    root.mainloop()


def search_api(departure_date, origin, destination, class_type, number_of_passengers):

    '''
    revised from https://rapidapi.com/tipsters/api/priceline-com-provider/
    '''
    
    url = "https://priceline-com-provider.p.rapidapi.com/v1/flights/search"
    
    if class_type == "Economy":
        class_type = "ECO"
    elif class_type == "Premium Economy":
        class_type = "PEC"
    elif class_type == "Business":
        class_type = "BUS"
    elif class_type == "First Class":
        class_type = "FST"

    querystring = {"date_departure":departure_date,
                    "class_type":class_type,
                    "itinerary_type":"ONE_WAY",
                    "location_arrival":destination,
                    "location_departure":origin,
                    "sort_order":"PRICE",
                    "number_of_passengers": int(number_of_passengers),
                    "number_of_stops": 0}
    headers = {
        "X-RapidAPI-Host": "priceline-com-provider.p.rapidapi.com",
        "X-RapidAPI-Key": "8fa8ea8a81msh29b24fcf85e49b7p18b86ajsn5f6640723ade"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response

def sort_flight(search_data, criteria, direction):
  '''
  search_data: json dictionary 
  '''
  search_data_copy = copy.deepcopy(search_data)
  if criteria == "departure time" or criteria == "arrival time":
    for i in search_data_copy.keys():
      time = search_data_copy[i][criteria][11:16]
      time = int(time[0:2])*60 + int(time[3:5])
      search_data_copy[i][criteria] = time   

  sorted_flights = {}
  while len(sorted_flights) != len(search_data_copy):
    curr_max = 0
    max_flight = None
    for i in search_data_copy.keys():
      if i not in sorted_flights.keys():
        number = search_data_copy[i][criteria]
        if number >= curr_max:
          curr_max = number
          max_flight = i
    sorted_flights[max_flight] = search_data[max_flight]
  
  if direction == "from low to high":
    sorted_flights_ascend = {}
    for i in range(len(sorted_flights.keys())-1, -1, -1):
      key = list(sorted_flights.keys())[i]
      sorted_flights_ascend[key] = sorted_flights[key]
    return sorted_flights_ascend
  else:
    return sorted_flights
    
def extra_info(response):
    segment = response.json()["segment"]
    uniqueSegId_segment = [i["uniqueSegId"] for i in segment]
    flight_numbers = [i["marketingAirline"] + i['flightNumber'] for i in segment]
    departure_time = [i["departDateTime"] for i in segment]
    arrival_time = [i["arrivalDateTime"] for i in segment]
    departure_airport = [i["origAirport"] for i in segment]
    arrival_airport = [i["destAirport"] for i in segment]
    flight_durations = [i["duration"] for i in segment]
    total_price = []
    slice_ = response.json()["slice"]
    uniqueSliceId_dict = {}
    for i in slice_:
        temp_key = i["segment"][0]["uniqueSegId"]
        uniqueSliceId_dict[temp_key] = i["uniqueSliceId"]

    price = response.json()["pricedItinerary"]
    for i in uniqueSegId_segment:
        slice_id = uniqueSliceId_dict[i]
        temp = [j["pricingInfo"]["totalFare"] for j in price if j["slice"][0]["uniqueSliceId"] == slice_id ]
        total_price.append(temp[0])

    search_results = {}
    for i in range(len(flight_numbers)):
        search_results[flight_numbers[i]] = {"departure time": departure_time[i],
                                        "arrival time": arrival_time[i],
                                        "departure airport": departure_airport[i],
                                        "arrival airport": arrival_airport[i],
                                        "flight durations": flight_durations[i],
                                        "total price": total_price[i]}
    search_results_json = json.dumps(search_results)
    with open('flight_data.json', 'w') as outfile:
        outfile.write(search_results_json)

if __name__ == "__main__":
    search_UI()



