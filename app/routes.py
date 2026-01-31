import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, session, abort, current_app as app
from app import db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User, Product, Order
from flask_login import login_user, current_user, logout_user, login_required

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img', picture_fn)
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/")
@app.route("/home")
def home():
    search_query = request.args.get('search')
    if search_query:
        products = Product.query.filter(Product.name.contains(search_query)).all()
    else:
        products = Product.query.all()
    return render_template('home.html', products=products, title='الرئيسية')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('تم إنشاء الحساب!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='تسجيل', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('بيانات خاطئة', 'danger')
    return render_template('login.html', title='دخول', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/cart")
def cart():
    display_cart = []
    total = 0
    if 'cart' in session:
        for item_id in session['cart']:
            p = Product.query.get(item_id)
            if p:
                display_cart.append(p)
                total += p.price
    return render_template('cart.html', display_cart=display_cart, total=total, title='السلة')

@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    if 'cart' not in session: session['cart'] = []
    session['cart'].append(product_id)
    session.modified = True
    flash('تمت الإضافة للسلة', 'info')
    return redirect(url_for('home'))

@app.route("/checkout")
@login_required
def checkout():
    if 'cart' not in session or not session['cart']: return redirect(url_for('home'))
    total = 0
    names = [Product.query.get(i).name for i in session['cart'] if Product.query.get(i)]
    total = sum([Product.query.get(i).price for i in session['cart'] if Product.query.get(i)])
    order = Order(user_id=current_user.id, total_price=total, products_ordered=", ".join(names))
    db.session.add(order)
    db.session.commit()
    session.pop('cart', None)
    flash('تم الطلب بنجاح!', 'success')
    return redirect(url_for('my_orders'))

@app.route("/my_orders")
@login_required
def my_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.date_ordered.desc()).all()
    return render_template('my_orders.html', orders=orders)

@app.route("/product/new", methods=['GET', 'POST'])
@login_required
def new_product():
    if not current_user.is_admin: abort(403)
    if request.method == 'POST':
        file = request.files.get('image')
        pic = save_picture(file) if file else 'product.jpg'
        product = Product(name=request.form.get('name'), price=float(request.form.get('price')),
                          description=request.form.get('description'), stock=int(request.form.get('stock')),
                          image_file=pic)
        db.session.add(product)
        db.session.commit()
        flash('تمت الإضافة!', 'success')
        return redirect(url_for('home'))
    return render_template('create_product.html', title='منتج جديد', product=None)

@app.route("/product/<int:product_id>/update", methods=['GET', 'POST'])
@login_required
def update_product(product_id):
    if not current_user.is_admin: abort(403)
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.price = float(request.form.get('price'))
        product.description = request.form.get('description')
        product.stock = int(request.form.get('stock'))
        file = request.files.get('image')
        if file: product.image_file = save_picture(file)
        db.session.commit()
        flash('تم التحديث!', 'success')
        return redirect(url_for('home'))
    return render_template('create_product.html', title='تعديل المنتج', product=product)

@app.route("/product/<int:product_id>/delete", methods=['POST'])
@login_required
def delete_product(product_id):
    if not current_user.is_admin: abort(403)
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('تم الحذف', 'warning')
    return redirect(url_for('home'))

@app.route("/admin/orders")
@login_required
def admin_orders():
    if not current_user.is_admin: abort(403)
    orders = Order.query.order_by(Order.date_ordered.desc()).all()
    return render_template('admin_orders.html', orders=orders)