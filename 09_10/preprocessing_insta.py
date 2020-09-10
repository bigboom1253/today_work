import pandas as pd
import json
import re
from pykospacing import spacing

class Preprocessing_Insta () :
    
    def __init__(self):
        self.escape_code = ['\n', '\xa0', '\"', '\'', '\t', '\r', '\$', '\\', '\u200d']
        return
    
    # hashtag 추출(#포함)
    def extract_hashtag(self, content) :
        hashtag_list = []
        if re.findall('\#[\w가-힣a-zA-Z0-9]*', str(content)):
             hashtag_list.append(re.findall('\#[\w가-힣a-zA-Z0-9]*', str(content)))
        else :
            hashtag_list.append('')
        
        return hashtag_list
    
    # post 추출
    def extract_post(self, content) :  
        post = re.sub('\#[\w가-힣a-zA-Z0-9]*',"",str(content)) 
        post = re.sub("\n"," ",post)
        post = re.sub("\@[\w가-힣a-zA-Z0-9]*","",post)   
        return post #string type

    # 태그된 userID 추출
    def extract_tagged_userID(self, content) : #태그된 userID 추출의 경우 hashtag 추출과 달리 @를 제거해준 값 리턴 
        tagged_userID_list = []
        if re.findall('\@[\w가-힣a-zA-Z0-9]*', str(content)):
            userID = re.findall('\@[\w가-힣a-zA-Z0-9]*', str(content))
            tagged_userID_list.append(re.sub("@","",userID))
        else :
            tagged_userID_list.append('')    
        return tagged_userID_list
    
    # hashtag(#) 제거
    def remove_hash(self, hashtag_list) :
        for hashtag in hashtag_list:
            tmp = []
            for j in  hashtag:
                tmp.append(re.sub("#","",j))
        return tmp
    
    #pykospacing패키지를 사용한 띄어쓰기 처리
    def auto_spacing(self, content) :
        return spacing(content)
        
    # Escape Code 처리
    def del_escape(self, content):
        for e in self.escape_code:
            content = content.replace(e, ' ')
        return content
    
    # emoji 삭제
    def del_emoji(self, content) :
        only_BMP_pattern = re.compile("["
        u"\U00010000-\U0010FFFF"  #BMP characters 이외
                           "]+", flags=re.UNICODE)
        return only_BMP_pattern.sub(r'', content)
    
    
    def preprocess_content(self, content_list) :        
        post_list =[]
        hashtag_list= []         
        for content in content_list :
            original_post = self.extract_post(content)
            post_list.append(self.auto_spacing(original_post))
            hashtag_list.append(self.remove_hash(self.extract_hashtag(content)))
        return post_list, hashtag_list
    
if __name__ == "__main__":
    content_list = ['다이어트 해야되는데...😂😂\n.\n.\n.\n#멋짐휘트니스연산점 #연산동pt','럽스타 그자체❤❤ #럽스타그램 #운동하는커플 #연산동pt']
    test_class = Preprocessing_Insta()
    post_ls, hashtag_ls = test_class.preprocess_content(content_list)
    print(post_ls)
    print(hashtag_ls)
    print("-----------------------------------------------------------------------------------------------")
    print(pd.DataFrame({'post':post_ls, 'hashtag':hashtag_ls}))
    print("------------------------------------------------------------------------------------------------")
    print("********이모티콘 제거 활용 예시********")
    for post in post_ls :
        print(test_class.del_emoji(post))
    
    