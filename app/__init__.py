from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config

# تعريف الإضافات بدون ربطها بالتطبيق حالياً (Global instances)
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

# تحديد المسار الذي يذهب إليه المستخدم إذا حاول دخول صفحة محمية وهو غير مسجل
login_manager.login_view = 'login' 
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    # تحميل الإعدادات من ملف config.py
    app.config.from_object(Config)

    # ربط الإضافات بالتطبيق (Initialize)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # استيراد الـ routes هنا لتجنب مشاكل الاستدعاء الدائري (Circular Import)
    with app.app_context():
        from app import routes
        return app