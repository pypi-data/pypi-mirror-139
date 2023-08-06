# Rite Aid API

This package allows for interactions with the Rite Aid API.

Here is an example of how to use the package:
```python
from riteaid import RiteAidAPI

async def main():
    api = RiteAidAPI()

    # Get a list of stores for ZIP Code 94025
    stores = await api.get_stores("94025")

    print(stores)
    
    # {"Data":
    #     {"stores":
    #         [
    #             {
    #                 "storeNumber":5892,
    #                 "address":"340 Woodside Plaza",
    #                 "city":"Redwood City",
    #                 "state":"CA",
    #                 "zipcode":"94061",
    #                 "timeZone":"PST",
    #                 "fullZipCode":"94061-3259",
    #                 "fullPhone":"(650) 368-7008",
    #                 "locationDescription":"Located at 340 Woodside Plaza             Woodside Plaza Next To Lucky's",# 
    #                 "storeHoursMonday":"7:00am-10:00pm",
    #                 "storeHoursTuesday":"7:00am-10:00pm",
    #                 "storeHoursWednesday":"7:00am-10:00pm",
    #                 "storeHoursThursday":"7:00am-10:00pm",
    #                 "storeHoursFriday":"7:00am-10:00pm",
    #                 "storeHoursSaturday":"7:00am-10:00pm",
    #                 "storeHoursSunday":"8:00am-10:00pm",
    #                 "rxHrsMon":"9:00am-8:00pm",
    #                 "rxHrsTue":"9:00am-8:00pm",
    #                 "rxHrsWed":"9:00am-8:00pm",
    #                 "rxHrsThu":"9:00am-8:00pm",
    #                 "rxHrsFri":"9:00am-8:00pm",
    #                 "rxHrsSat":"9:00am-6:00pm",
    #                 "rxHrsSun":"10:00am-6:00pm",
    #                 "storeType":"RA",
    #                 "latitude":37.4565,
    #                 "longitude":-122.229,
    #                 "name":"Rite Aid",
    #                 "milesFromCenter":2.5,
    #                 "specialServiceKeys":[...],
    #                 "event":null,
    #                 "holidayHours":[],
    #                 "pickupDateAndTimes":
    #                     {
    #                         "regularHours":
    #                             [
    #                                 "11:00 AM-5:00 PM",
    #                                 "10:00 AM-7:00 PM",
    #                                 "10:00 AM-7:00 PM",
    #                                 "10:00 AM-7:00 PM",
    #                                 "10:00 AM-7:00 PM",
    #                                 "10:00 AM-7:00 PM",
    #                                 "10:00 AM-5:00 PM"
    #                             ],
    #                         "specialHours":
    #                             {
    #                                 "2022-02-19":"10:30 AM-5:00 PM",
    #                                 "2022-02-20":"11:00 AM-5:00 PM"
    #                             },
    #                         "defaultTime":"2022-02-20 1:00 PM",
    #                         "earliest":"2022-02-19 10:30 AM"
    #                     }
    #                 }
    #             ]
    #         },
    #         "Status":"SUCCESS",
    #         "ErrCde":null,
    #         "ErrMsg":null,
    #         "ErrMsgDtl":null
    #     }
    # }

    # Refill an Rx
    refill = await api.refill_rx([
        "123456789012", # Rx Number
        "123456789012", # Rx Number
        "123456789012", # Rx Number
    ],
    "5892", # Store Number
    "2022-02-20", # Refill Date
    "1:00 PM", # Refill Time
    "6058392845", # Phone Number
    )

    print(refill)

    # I have not tested a succesful refill yet, since I don't have the need for a refill at the moment.
```

## `get_stores`

| Parameter | Description |
| --------- | ----------- |
| zipcode | ZIP Code |

## `refill_rx`

| Parameter | Description |
| --------- | ----------- |
| rx_numbers | Rx Numbers  |
| store_number | Store Number |
| refill_date | Refill Date |
| refill_time | Refill Time |
| phone_number | Phone Number |