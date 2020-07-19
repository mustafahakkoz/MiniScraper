import urllib.request
import json
import csv
import time


#open .csv file that contains only user names
with open('followers_nevsin17K.csv', newline='') as csvfile:
    input_list = list(csv.reader(csvfile))

#initialize variables
u_followers_whitelist = []
u_followers_blacklist = []
count=0
wl_count=0
bl_count=0

#start timer to calculate execution time
start=time.clock()


for  twitter_username in input_list:
    #read json data fron url
    url = 'https://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names='+twitter_username[0] 
    data=json.load(urllib.request.urlopen(url))
    print(data)
    
    #data may contain empty array if user closed his account
    try:      
        user=data[0] 
    except IndexError:
        pass
    
    #create a dictionary for every user by using data coming from url above 
    u_dict = dict()
    u_dict["username"] = user['screen_name']
    u_dict["id"] = user['id']
    u_dict["followers_count"] =  user['followers_count']
    u_dict["protected"] = user['protected']
    u_dict["age_gated"] = user['age_gated']
    count+=1
    print("{}. user {} okundu...".format(count,u_dict["username"]))
    
    #if user passes all conditions, it s written into whitelist otherwise into blacklist
    if u_dict['followers_count'] >= 200 and u_dict['protected'] == False and u_dict['age_gated'] == False:
        u_followers_whitelist.append(u_dict)
        wl_count+=1
        print("{}. user {} whiteliste eklendi...Total:{}\n".format(count, u_dict["username"],wl_count))
    else:
        u_followers_blacklist.append(u_dict)
        bl_count+=1
        print("{}. user {} blackliste eklendi...Total:{}\n".format(count, u_dict["username"],bl_count))
    
#calculation of execution time
end=time.clock()
elapsed_time = end-start
print(elapsed_time)

#print lists to corresponding .json files
with open("blacklist.json", "w+", encoding="utf-8") as write_file1:
        json.dump(u_followers_blacklist, write_file1, indent=4, ensure_ascii=False)
        
with open("whitelist.json", "w+", encoding="utf-8") as write_file2:
        json.dump(u_followers_whitelist, write_file2, indent=4, ensure_ascii=False)
        