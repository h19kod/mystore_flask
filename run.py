import os
from app import create_app, db
from app.models import User

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # 1. إنشاء الجداول إذا لم تكن موجودة
        db.create_all()
        
        # 2. ترقية حساب admin ليكون مديراً
        admin_user = User.query.filter_by(username='admin').first()
        if admin_user:
            admin_user.is_admin = True
            db.session.commit()
            print("✅ تم تفعيل صلاحيات المدير بنجاح!")
        else:
            print("⚠️ تنبيه: لم يتم العثور على مستخدم باسم admin")

    # 3. تشغيل السيرفر وعدم التوقف
    print("🚀 السيرفر يعمل الآن على: http://127.0.0.1:5000")
    app.run(debug=True)