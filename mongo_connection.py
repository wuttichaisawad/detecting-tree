from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

def get_mongo_client():
    mongo_uri = "mongodb+srv://datadetec:1234@det4caa.rzarg.mongodb.net/?retryWrites=true&w=majority"
    try:
        client = MongoClient(mongo_uri)
        client.server_info()  # ตรวจสอบการเชื่อมต่อ MongoDB
        print("เชื่อมต่อกับ MongoDB สำเร็จ!")
        return client
    except ServerSelectionTimeoutError as e:
        print(f"ไม่สามารถเชื่อมต่อกับ MongoDB: {str(e)}")
        return None
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {str(e)}")
        return None
