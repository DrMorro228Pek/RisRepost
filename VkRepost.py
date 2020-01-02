# coding: utf8
import vk_api
import json
import random
import time
import os

login, password = os.environ.get("LOGIN"), os.environ.get("PASS"), 
vk_session = vk_api.VkApi(login, password)
vk_session.auth()
count = 50

while True:

    result = vk_session.method('newsfeed.search', {'q':'Rust конкурс', 'count': count})
    
    result_txt=json.dumps(result, sort_keys=True, indent=4, ensure_ascii=False)
    
    result_json = json.loads(result_txt)
    
    for i in range(0,count):
        
        f1 = open("banlist.txt", "r",encoding="utf-8")
        f3 = open("yetUsed.txt", "r+",encoding="utf-8")
        
        group_id = result_json.get("items")[i].get("from_id")
        object_id = result_json.get("items")[i].get("id")
        group_text = result_json.get("items")[i].get("text").lower()
        
        full_object_link = "wall" + str(group_id) + "_" + str(object_id)
        fbl_for_yet = str(group_id) + "," + str(object_id)    
        
        # Проверки
        is_continue = -1
        
            # Было ли уже зарепощено
        for line in f3:
            if line.find(fbl_for_yet) != -1:
                print(line + " уже зарепощено \n")
                is_continue = 1
                break
        
            # Проходит ли бан лист
        for line in f1:
            if group_text.find(line.strip()) != -1:
                print(full_object_link + " не прошло бан лист: " + line + "\n")
                is_continue = 1
                break
            
        if is_continue == 1:
            continue
        # Репостим наконец
        
            # Вступаем в группу
        try:
            vk_session.method("groups.join", {"group_id": str(abs(group_id))})
        except:
            pass
        
            #Делаем репост
        vk_session.method("wall.repost", {"object": str(full_object_link)})
        
        print("Репостнул " + full_object_link + "\n")
        
        f3.write(fbl_for_yet + "\n")
        
        # Доп инфа
        print("                    " + str(i))
        print("=======================================")
        print(group_text)
        print("=======================================")
    
        #Закрытие файлов    
        f1.close()
        f3.close()
        
        # Кд для записей
        time.sleep(120.0+random.random()*100.0)
    # Кд для работы
    time.sleep(3600)

    



