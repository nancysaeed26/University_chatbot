import pymysql
print("بدأ البرنامج")

db = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="university_chatbot"
)

print("تم الاتصال بقاعدة البيانات")
