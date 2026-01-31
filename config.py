import os

class Config:
    # SECRET_KEY: ضروري جداً لتأمين النماذج (Forms) والجلسات (Sessions)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-12345'
    
    # SQLALCHEMY_DATABASE_URI: يحدد نوع ومكان قاعدة البيانات (هنا SQLite)
    # سيتم إنشاء ملف باسم site.db داخل المجلد الرئيسي
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    
    # تعطيل خاصية تتبع التعديلات لتوفير موارد الجهاز
    SQLALCHEMY_TRACK_MODIFICATIONS = False