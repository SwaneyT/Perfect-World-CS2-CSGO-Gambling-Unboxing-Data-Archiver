from pymongo_get_database import get_database
dbname = get_database()
collection_name = dbname["time_series_data"]
from dateutil import parser
import time

# Fetch a document from the collection
doc = collection_name.find_one()
# Print the document
print(doc)


# unix_timestamp = 1713548961
# dt = datetime.datetime.fromtimestamp(unix_timestamp)
# bson_datetime = ObjectId.from_datetime(dt)

# print("Unix timestamp:", unix_timestamp)
# print("BSON datetime:", bson_datetime)

# bson_datetime_value = bson_datetime.generation_time

# item_3 = {
#     "time": bson_datetime_value,
#     "item_name": "Bread",
#     "quantity": 2,
#     "ingredients": "all-purpose flour"
# }

# collection_name.insert_one(item_3)




import requests
import json
import time
import winsound
from bson import ObjectId
import datetime
import cs2_chinese_to_english
from define_src_type import defineSrcType

def unixTimestampToBSON(unix_timestamp):
    dt = datetime.datetime.fromtimestamp(unix_timestamp)
    bson_datetime = ObjectId.from_datetime(dt)
    bson_datetime_value = bson_datetime.generation_time

    return bson_datetime_value

def getChinaData():
    #get china data and return it
    print("Getting China Data...")
    req = requests.post("https://www.csgo.com.cn/api/lotteryHistory")

    while req.text == []:
        print(f"Failed to get data... Retrying, Data: {req.text}")
        req = requests.post("https://www.csgo.com.cn/api/lotteryHistory") ##if response is empty, keep making request until not empty
    
    return json.loads(req.text)



def compareChinaData(oldData,newData):
    #is new data the same as old data?
    #if its new, return newData
    #if its old, return None
    print("Comparing New and Old China Data...")

    if oldData == newData:
        return None #return none if same
    elif oldData != newData:
        return newData #return new data if different

def addJSONToMongoDB(json):
    ### NEED TO FORMAT JSON INTO time_series_data FORMAT FOR MONGODB ###
    ### CHANGE UNIX TIMESTAMPS INTO BSON ###
    new_format_json = []

    for result in json:
        ### CONVERT UNIX TIMESTAMP TO BSON ###
        new_bson_timestamp = unixTimestampToBSON(result['timestamp'])
        ### GET SRC TYPE ###
        box_type = defineSrcType(result['src'])
        new_single_json = {'time' : new_bson_timestamp, 'user' : result['user'], 'src' : result['src'], 'out' : result['out'], 'box_type' : box_type}
        new_format_json.append(new_single_json)

    ### ADD NEW FORMATTETD JSON STRING TO DATABASE ###
    print(new_format_json)
    collection_name.insert_many(new_format_json)

def translateChineseToEnglish(raw_json_data):
    #open other program, give chinese text... cross reference it with english, return english... use english done
    translation_errors_file = open("translation_errors.txt", "a", encoding="utf-8")
    for json_element in raw_json_data['result']:
        ### TRANSLATE AND ERROR HANDLE SRC ###
        translated_src = cs2_chinese_to_english.translateChineseToEnglish(json_element['src'])
        if translated_src != None:
            json_element['src'] = translated_src
        else:
            print(f"Translation error: {json_element['src']}")
            translation_errors_file.write(str(json_element['src']) + "\n")
        
        ### TRANSLATE AND ERROR HANDLE OUT ###
        translated_out = cs2_chinese_to_english.translateChineseToEnglish(json_element['out'])
        if translated_out != None:
            json_element['out'] = translated_out
        else:
            print(f"Translation error: {json_element['out']}")
            translation_errors_file.write(str(json_element['out']) + "\n")
    
    translation_errors_file.close()
    return raw_json_data


newData = []
oldData = []

while True:
    try:
        if newData: #if its been scanned once already
            # check if request failed
            if newData['status'] != "success":
                print("Request failed. Continuing Loop")
                continue
            ### GO AHEAD ###
            oldData = newData
            newData = getChinaData()
            ### TRANSLATE CHINESE BELOW ###
            newData = translateChineseToEnglish(newData)
            
        else: #if never scanned, get newData
            newData = getChinaData()
            ### TRANSLATE CHINESE BELOW ###
            newData = translateChineseToEnglish(newData)


        if oldData:
            print(f"First received result: {newData['result'][0]}") #print first found result

            comparison = compareChinaData(oldData,newData) #check if old and new are different
            
            if comparison != None:
                #comparison decided new data is different to old, send to mongodb
                print(f"1 SEND NEW DATA TO MONGODB")
                addJSONToMongoDB(newData['result'])
                print(newData)
            else:
                print("Data was the same and does not need to be sent to database.")
        else:
            #data is brand new and needs to be sent to mongodb
            ####### THIS NEEDS ANOTHER CHECK TO SEE IF THE DATA ALREADY EXISTS IN THE DATABASE #######
            print(f"First received result: {newData['result'][0]}") #print first found result
            ### CHECK IF DATA ALREADY EXISTS ###
            firstResultBSON = unixTimestampToBSON(newData['result'][0]['timestamp'])
            firstResultExist = collection_name.find_one({"time": firstResultBSON})
            if firstResultExist != None:
                print("Match, already exists. DO NOT ADD")
            else:
                print("Not found, add to records!")
                print(f"2 SEND NEW DATA TO MONGODB")
                addJSONToMongoDB(newData['result'])

        print("Sleeping 10 minutes.")
        time.sleep(600) #one minute pause
    except Exception as e:
        print(f"Error in while true loop, exception: {e}")

