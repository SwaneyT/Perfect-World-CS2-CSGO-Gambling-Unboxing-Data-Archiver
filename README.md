Scrape and save the CS2 case/capsule unboxing data published from Perfect World's API: https://www.csgo.com.cn/api/lotteryHistory (https://www.csgo.com.cn/hd/1707/lotteryrecords/index.html)

The "scan_and_insert_mongodb.py" program will refresh the API every 10 minutes (API only updates every hour), check if the data has already been added to your MongoDB database (on first run), or check if the data is the same as the previous result (runs after first).
If the data has not been added, or is not the same as the previous result, the data will be processed and then added to your MongoDB database.

The program translates the Chinese case/capsule names, and the Chinese case/capsule output into English with 1:1 translations through the "cs2_chinese_to_english.py" program.
The program also categorises the case/capsule into all possible categories available in CS2, and creates a new database field (box_type) for it:
* Case
* Sticker Capsule
* Souvenir Package
* Collection Package
* Grafitti Box
* Music Kit Box
* Patch Pack
* Pins Capsule

Any translations not found in "china_translation_organised.txt" will be added to "translation_errors.txt", for you to manually add the translation.

Setup requires changing the MongoDB URI and changing the "china_data" table to your database name in "pymongo_get_database.py", as well as changing the table name at the top of "scan_and_insert_mongodb.py".

Example data in MongoDB:
![image](https://github.com/SwaneyT/Perfect-World-CS2-CSGO-Gambling-Unboxing-Data-Archiver/assets/111639108/122b5a83-0e00-4a1f-a736-552d207948cf)



_**Happy archiving Perfect World's CS2 transparent gambling unboxing data courtesy of China's strict regulations!**_
