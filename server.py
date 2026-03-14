from datetime import datetime
# server.py

import base64
import uuid
import imghdr
import requests
from flask import Flask, flash,session
from flask import render_template, url_for, redirect, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column, Mapped,DeclarativeBase,relationship
from sqlalchemy import DateTime, String, Integer,ForeignKey
from werkzeug.security import check_password_hash, generate_password_hash

from flask_login import LoginManager,UserMixin,login_user, login_required,current_user,logout_user


app= Flask(__name__)
login_manager = LoginManager(app)
app.secret_key='abdomohamed'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
SUPABASE_URL = "https://wmkfvadfdnjpmdurnudb.supabase.co"
SUPABASE_KEY = "sb_publishable_aCVfYc4k1oCSUl3twmfjVA_iSlR3gy6"
BUCKET = "items"
login_manager.login_view = 'login'
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Admin(db.Model, UserMixin):
    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    name:Mapped[str] = mapped_column(String(150), nullable=False)
    number:Mapped[int] = mapped_column(Integer, nullable=False)
    password:Mapped[int] = mapped_column(String(255), nullable=False)

class ItemDetails(db.Model):
    __tablename__='itemdetails'
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str] = mapped_column(String(150), nullable=False)
    description:Mapped[str] = mapped_column(String(500), nullable=False)
    price:Mapped[int] = mapped_column(Integer, nullable=False)
    visability:Mapped[int] = mapped_column(Integer, nullable=False,default=1)
    item_colors = relationship('ItemColor',backref='deltails')
    item_imgs = relationship('ItemImg',backref='deltails')


class ItemColor(db.Model):
    __tablename__='itemcolor'
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    color:Mapped[str] = mapped_column(String(150),)
    item_id:Mapped[int] = mapped_column(Integer, ForeignKey('itemdetails.id'))
    
class ItemImg(db.Model):
    __tablename__='itemimg'
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    img:Mapped[str] = mapped_column(String(255),)
    item_id:Mapped[int] = mapped_column(Integer, ForeignKey('itemdetails.id'))
    

class Order(db.Model):
    __tablename__='order'
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str] = mapped_column(String(155),nullable=False)
    phone:Mapped[str] = mapped_column(String(155),nullable=False)
    second_phone:Mapped[str] = mapped_column(String(155))
    city:Mapped[str] = mapped_column(String(155),nullable=False)
    adress:Mapped[str] = mapped_column(String(250),nullable=False)
    message:Mapped[str] = mapped_column(String(500))
    created_at = db.Column(DateTime, default=datetime.utcnow)
    state:Mapped[str] = mapped_column(String(155),default='order')
    ordered_items = relationship('Cart',backref='order')
    

class Cart(db.Model):
    __tablename__='cart'
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    img:Mapped[str] = mapped_column(String(255))
    color:Mapped[str] = mapped_column(String(150))
    name:Mapped[str] = mapped_column(String(150), nullable=False)
    price:Mapped[int] = mapped_column(Integer, nullable=False)
    amount:Mapped[int] = mapped_column(Integer, nullable=False)
    size:Mapped[str] = mapped_column(String(150), nullable=False)
    session_id:Mapped[str] = mapped_column(String(100), nullable=True)  # Guest session tracking
    order_id:Mapped[str] = mapped_column(Integer, ForeignKey('order.id'), nullable=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img,
            "amount": self.amount,
            "size": self.size,
            "color": self.color,
            "price": self.price,
        }
    
    
    



with app.app_context():
    db.create_all()
#     items=[
#     {
#         'name':"Coat",
#         'description':"Springrain Men's Wool Blend Pea Coat Notched Collar Single Breasted Overcoat Warm Winter Trench Coat",
#         'imgs':[
#             'https://m.media-amazon.com/images/I/711NoFaDOJL._AC_SY500_.jpg',
#             'https://m.media-amazon.com/images/I/71IR7Xg2Z4L._AC_SY500_.jpg',
#             'https://m.media-amazon.com/images/I/61DWc7OqnPL._AC_SY500_.jpg',
#             'https://m.media-amazon.com/images/I/61XNU3qvAdL._AC_SY500_.jpg',
#             'https://m.media-amazon.com/images/I/71t5suDm+XL._AC_SY500_.jpg'
#             ],
#         'colors':['grey','black','havan'],
#         'price' :13

#     },
#     {
#         'name':"shirt",
#         'description':"COOFANDY Men's Long Sleeve Button Down Shirt Wrinkle Free Untucked Dress Shirt Casual Denim Shirt",
#         'imgs':[
#             'https://m.media-amazon.com/images/I/81hn4NOLuPL._AC_SX425_.jpg',
#             'https://m.media-amazon.com/images/I/71TM2Ds5ijL._AC_SX385_.jpg',
#             'https://m.media-amazon.com/images/I/71qeTQ7iKfL._AC_SX385_.jpg',
#             'https://m.media-amazon.com/images/I/71anSFX+J7L._AC_SX385_.jpg',
#             'https://m.media-amazon.com/images/I/71CVxTEkJ4L._AC_SX385_.jpg'
#             ],
#         'colors':['blue','black','pink'],
#         'price' :20
#     },
#     {
#         'name':"T-shirt",
#         'description':"Gildan Men's Crew T-Shirts, Multipack, Style G1100",
#         'imgs':[
#             'https://m.media-amazon.com/images/I/61Nn7FcOqBL._AC_SX522_.jpg',
#             'https://m.media-amazon.com/images/I/61Q5js47DgL._AC_SX522_.jpg',
#             'https://m.media-amazon.com/images/I/614VnOp0UGL._AC_SX522_.jpg',
#             ],
#         'colors':['black','white'],
#         'price' :30
#     },
#     {
#         'name':"pants",
#         'description':"Gildan Men's Crew T-Shirts, Multipack, Style G1100",
#         'imgs':[
#             'https://m.media-amazon.com/images/I/71mkhtxkS+L._AC_SY500_.jpg',
#             'https://m.media-amazon.com/images/I/81FlisHpMFL._AC_SX522_.jpg',
#             'https://m.media-amazon.com/images/I/71U0eWjSJPL._AC_SX522_.jpg',
#             ],
#         'colors':['brown','black'],
#         'price' :50
#     },
#     {
#         'name':"Coat",
#         'description':"Springrain Men's Wool Blend Pea Coat Notched Collar Single Breasted Overcoat Warm Winter Trench Coat",
#         'imgs':[
#             'https://m.media-amazon.com/images/I/711NoFaDOJL._AC_SY500_.jpg',
#             'https://m.media-amazon.com/images/I/71IR7Xg2Z4L._AC_SY500_.jpg',
#             'https://m.media-amazon.com/images/I/61DWc7OqnPL._AC_SY500_.jpg',
#             'https://m.media-amazon.com/images/I/61XNU3qvAdL._AC_SY500_.jpg',
#             'https://m.media-amazon.com/images/I/71t5suDm+XL._AC_SY500_.jpg'
#             ],
#         'colors':['grey','black','havan'],
#         'price' :13

#     },
#     {
#         'name':"shirt",
#         'description':"COOFANDY Men's Long Sleeve Button Down Shirt Wrinkle Free Untucked Dress Shirt Casual Denim Shirt",
#         'imgs':[
#             'https://m.media-amazon.com/images/I/81hn4NOLuPL._AC_SX425_.jpg',
#             'https://m.media-amazon.com/images/I/71TM2Ds5ijL._AC_SX385_.jpg',
#             'https://m.media-amazon.com/images/I/71qeTQ7iKfL._AC_SX385_.jpg',
#             'https://m.media-amazon.com/images/I/71anSFX+J7L._AC_SX385_.jpg',
#             'https://m.media-amazon.com/images/I/71CVxTEkJ4L._AC_SX385_.jpg'
#             ],
#         'colors':['blue','black','pink'],
#         'price' :20
#     },
#     {
#         'name':"T-shirt",
#         'description':"Gildan Men's Crew T-Shirts, Multipack, Style G1100",
#         'imgs':[
#             'https://m.media-amazon.com/images/I/61Nn7FcOqBL._AC_SX522_.jpg',
#             'https://m.media-amazon.com/images/I/61Q5js47DgL._AC_SX522_.jpg',
#             'https://m.media-amazon.com/images/I/614VnOp0UGL._AC_SX522_.jpg',
#             ],
#         'colors':['black','white'],
#         'price' :30
#     },
#     {
#         'name':"pants",
#         'description':"Gildan Men's Crew T-Shirts, Multipack, Style G1100",
#         'imgs':[
#             'https://m.media-amazon.com/images/I/71mkhtxkS+L._AC_SY500_.jpg',
#             'https://m.media-amazon.com/images/I/81FlisHpMFL._AC_SX522_.jpg',
#             'https://m.media-amazon.com/images/I/71U0eWjSJPL._AC_SX522_.jpg',
#             ],
#         'colors':['brown','black'],
#         'price' :50
#     },

# ]
#     for item in items:
#         item_obj = ItemDetails(name=item['name'], description=item['description'], price = item['price'])
#         db.session.add(item_obj)
#         db.session.commit()
#         for item_col in item['colors']:
#             item_color = ItemColor(color=item_col, item_id = item_obj.id)
#             db.session.add(item_color)
#             db.session.commit()
        
#         for item_img in item['imgs']:
#             item_image = ItemImg(img=item_img, item_id = item_obj.id)
#             db.session.add(item_image)
#             db.session.commit()

@login_manager.user_loader
def userloader(user_id):
    return db.get_or_404(Admin, user_id)


@app.route('/')
def home():
    items_list = db.session.query(ItemDetails).filter_by(visability=1).all()
    # delete_all_cart_items=[db.session.delete(item) for item in db.session.query(Cart).all()]
    # db.session.commit()
    return render_template('index.html', items = items_list)


@app.route('/shoping')
def shop():
    items = db.session.query(ItemDetails).filter_by(visability=1).all()
    return render_template('shop.html', items = items)

@app.route('/shoping-cart')
def shoping_cart():
    cart_items = Cart.query.filter_by(session_id=session['session_id']).all()
    total_price = sum(item.price*item.amount for item in cart_items)
    return render_template('shoping-cart.html', items = cart_items, total_price = total_price)


@app.route('/login',methods=['POST', 'GET'])
def login():
    if request.method =='POST':
        entered_name = request.form['name']
        admin = db.session.query(Admin).filter_by(name=entered_name).first()
        if not admin:
             flash(f"Admin with name '{entered_name}' Not found")
             return render_template('login.html')
        elif admin.number !=request.form.get('number',type=int):
            flash('The Entred Phone Number is Wrong')
            return render_template('login.html', name = entered_name,password= request.form['password'])
        elif not check_password_hash(admin.password,request.form['password']):
            flash('The Entred pasword is Wrong')
            return render_template('login.html', name = entered_name, number =request.form.get('number',type=int))
             
        else:
           login_user(admin)
           return redirect(url_for('dashboard'))

    else:
        return render_template('login.html')

    

@app.route('/register',methods=['POST', 'GET'])
def register():
    if request.method=='POST':
        ent_name = request.form['name']
        ent_pass = request.form['password']
        ent_confirmed_pass = request.form['c_password']
        if db.session.query(Admin).filter_by(name =ent_name).first():
            flash(f"Admin with name '{ent_name}' is arleady Resgitered Please Login")
            return redirect(url_for('login'))

        elif ent_pass != ent_confirmed_pass:
            flash('Wrong Confirmed Password')
            return render_template('register.html', name = ent_name, password = ent_pass, c_password=ent_confirmed_pass, number =request.form.get('number',type=int))
        else:
            hashed_password = generate_password_hash(ent_pass,'scrypt',8)
            new_admin = Admin(
                name=ent_name, 
                password = hashed_password, 
                number=request.form.get('number',type=int),
                )
            db.session.add(new_admin)
            db.session.commit()
            return redirect(url_for('dashboard'))

    else:
        return render_template('register.html')

@app.route('/checkout', methods = ['POST', 'GET'])
def check_out():
    if request.method =='POST':

        order = Order(
            name = request.form['fullname'],
            phone = request.form['phone'],
            second_phone = request.form['second-phone'],
            city = request.form['city'],
            adress = request.form['adress'],
            message = request.form['msg'],
        )
        db.session.add(order)
        db.session.commit()

        # 2️⃣ Assign cart items of this session to the order
        cart_items = Cart.query.filter_by(session_id=session['session_id'], order_id=None).all()
        for item in cart_items:
            item.order_id = order.id
        db.session.commit()

        # 3️⃣ Optional: clear session cart (start fresh)
        session.pop('session_id', None)
        return render_template('after-order.html')
    else:
        return render_template('checkout.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# give data to js
@app.route("/get-item", methods=["POST"])
def get_item():

    item_id = request.form.get("id",type = int)

    item = db.get_or_404(ItemDetails, item_id)
    imgs_list = [img.img for img in item.item_imgs]
    colors_list = [color.color for color in item.item_colors]
    print(type(imgs_list))
    return jsonify({
        "name": item.name,
        "price": item.price,
        "description": item.description,
        "images": imgs_list,
        "colors": colors_list
    })
    

@app.route('/add-to-cart',methods=['POST'])
def add_to_cart():
    data = request.get_json()
    item_id = int(data['id'])
    print(data)
    item_with_id = db.get_or_404(ItemDetails, item_id)
    item_img = item_with_id.item_imgs[0].img if item_with_id.item_imgs else "default.png"
        # Check if a session ID exists

    cart_prduct = Cart(name = item_with_id.name, 
                       img = item_img,
                       color = data['color'],
                       price= item_with_id.price,
                       amount = int(data['amount']),
                       size = data['size'],
                       session_id=session['session_id'],
                       order_id=None  # Not assigned yet
                       )
    db.session.add(cart_prduct)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Data received!'})

@app.route('/get-cart-items', methods=['POST'])
def get_cart_items():

    cart_items =  Cart.query.filter_by(session_id=session['session_id']).all()
    total_price = sum(item.price*item.amount for item in cart_items)
    items = [item.to_dict() for item in cart_items]
    
    return jsonify({
        'items': items,
        'total_price':total_price
        })

@app.route('/change-amount', methods=['POST'])
def change_item_amount():
    data = request.get_json(force=True)
    item_id = int(data['id'])
    new_amount = int(data['amount'])

    item_to_change = Cart.query.filter_by(session_id=session['session_id'],id=item_id).first()

    if new_amount == 0:
        db.session.delete(item_to_change)
        db.session.commit()
        cart_items = Cart.query.filter_by(session_id=session['session_id']).all()
        total_price = sum(item.price*item.amount for item in cart_items)
        return jsonify({
            'total_price': total_price,
            'price': 0,           # item removed
            'removed': True       # flag for JS
        })
    else:
        item_to_change.amount = new_amount
        db.session.commit()

        cart_items = Cart.query.filter_by(session_id=session['session_id']).all()
        total_price = sum(item.price*item.amount for item in cart_items)
        return jsonify({
            'total_price': total_price,
            'price': item_to_change.price,
            'removed': False
        })

@app.route('/remove-cart-item', methods=['POST'])
def remove_item_amount():

    item_id = request.form['id']
    item_to_change = Cart.query.filter_by(session_id=session['session_id'],id=item_id).first()
    db.session.delete(item_to_change)
    db.session.commit()
    cart_items = Cart.query.filter_by(session_id=session['session_id']).all()
    total_price = sum(item.price*item.amount for item in cart_items)
    print(total_price)
    return jsonify({
            'total_price': total_price,
        })

@app.route('/get-orders', methods=['POST'])
def get_orders():

    state = request.form['state']
    orders_list = Order.query.filter_by(state=state).all()[::-1]

    orders = []

    for order in orders_list:
        ordered_items = [item.to_dict() for item in order.ordered_items]
        data = {
            'id': order.id,
            'username': order.name,
            'first_number': order.phone,
            'second_number': order.second_phone,
            'city': order.city,
            'adress': order.adress,
            'message': order.message,
            'created_at': order.created_at.strftime("%Y-%m-%d %H:%M"),
            'state': order.state,
            'ordered_items': ordered_items
        }

        orders.append(data)
    print(orders)

    return jsonify({'orders': orders})


@app.route('/update-order-state', methods=['POST'])
def update_order_state():

    order_id = request.form.get("id")
    new_state = request.form.get("state")

    order = Order.query.get(order_id)

    if order:
        order.state = new_state
        db.session.commit()
        return jsonify({"success": True})

    return jsonify({"success": False})

@app.before_request
def ensure_session():
    if 'session_id' not in session:
        import uuid
        session['session_id'] = str(uuid.uuid4())

@app.route('/get-order-data', methods = ['POST'])
def get_order_data():
    item_id = int(request.form['id'])
    order = db.session.query(Order).filter_by(id = item_id).first()
    ordered_items = [item.to_dict() for item in order.ordered_items]
    order_data = {
            'id': order.id,
            'username': order.name,
            'first_number': order.phone,
            'second_number': order.second_phone,
            'city': order.city,
            'adress': order.adress,
            'message': order.message,
            'created_at': order.created_at.strftime("%Y-%m-%d %H:%M"),
            'state': order.state,
            'ordered_items': ordered_items
        }
    print(order_data)
    return jsonify(order_data)

# add new item
@app.route("/admin/add-item", methods=["POST"])
def add_item():

    data = request.json

    name = data["name"]
    price = data["price"]
    description = data["description"]
    colors = data["colors"]

    # transform the imgs from the bata64 in to images with name and then post it into superbase storage and then same the public url
    image_links = []
    for img in data["images"]:
        header, encoded = img.split(",", 1)
        binary = base64.b64decode(encoded)
        ext = imghdr.what(None, binary) or "png"
        filename = f"{uuid.uuid4()}.{ext}"

        url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET}/{filename}"
        headers = {
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "apikey": SUPABASE_KEY,
            "Content-Type": f"image/{ext}"
        }

        r = requests.put(url, headers=headers, data=binary)
        if r.status_code not in [200, 201]:
            raise Exception(f"Upload failed: {r.text}")

        # Public URL
        public_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET}/{filename}"
        image_links.append(public_url)

   
    new_item = ItemDetails(name=name, price=price, description=description)
    db.session.add(new_item)
    db.session.commit()  # commit once to get new_item.id

    # Add colors
    for color in colors:
        new_item_color = ItemColor(color=color, item_id=new_item.id)
        db.session.add(new_item_color)

    # Add images
    for link in image_links:
        new_item_img = ItemImg(img=link, item_id=new_item.id)
        db.session.add(new_item_img)

    db.session.commit()  # final commit after adding all
    print(name, price, description,colors,image_links)
    return jsonify({"status":"ok"})

@app.route('/delete-item',methods=['POST'])
def delete():
    data = request.get_json()
    id = data["id"]
    targeted_item=db.get_or_404(ItemDetails,id)
    targeted_item.visability =0
    print(id)
    db.session.commit()

    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True)