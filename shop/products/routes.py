from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app, photos
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import secrets, os


@app.route('/')
def home():
    products = Addproduct.query.filter(Addproduct.stock > 0)
    barnds = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return render_template('products/index.html', title='All products', products=products, barnds=barnds)


@app.route('/brand/<int:id>', methods=['GET', 'POST'])
def get_brand(id):
    brand = Addproduct.query.filter_by(brand_id=id)
    barnds = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return render_template('products/index.html', title='All products', brand=brand, barnds=barnds)


@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if 'email' not in session:
        flash(f'You must be logged in', 'danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand) 
        flash(f'The Brand {getbrand} has been added successfully', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', brands='brands')


@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    if 'email' not in session:
        flash(f'You must be logged in', 'danger')
        return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == "POST":
        updatebrand.name = brand
        flash(f'Brand has been updated successfully', 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html', title='Update brand page', updatebrand=updatebrand)


@app.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(brand)
        db.session.commit()
        flash(f'Brand name {brand.name} has been deleted successfully', 'success')
        return redirect(url_for('admin'))
    flash(f'{brand.name} can\'t be deleted', 'warning')
    return redirect(url_for('admin'))


@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if 'email' not in session:
        flash(f'You must be logged in', 'danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getcat = request.form.get('category')
        cat = Category(name=getcat)
        db.session.add(cat)
        flash(f'The Category {getcat} has been added successfully', 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html')


@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
    if 'email' not in session:
        flash(f'You must be logged in', 'danger')
        return redirect(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == "POST":
        updatecat.name = category
        flash(f'Category name has been updated successfully', 'success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/updatebrand.html', title='Update brand page', updatecat=updatecat)


@app.route('/deletecategory/<int:id>', methods=['POST'])
def deletecategory(id):
    category = Category.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(category)
        db.session.commit()
        flash(f'Category name {category.name} has been deleted successfully', 'success')
        return redirect(url_for('admin'))
    flash(f'{category.name} can\'t be deleted', 'warning')
    return redirect(url_for('admin'))


@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
    if 'email' not in session:
        flash(f'You must be logged in', 'danger')
        return redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        description = form.description.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        
        addpro = Addproduct(name=name, price=price, discount=discount, stock=stock, colors=colors,
                             description=description, brand_id=brand, category_id=category, image_1=image_1,
                             image_2=image_2, image_3=image_3)
        db.session.add(addpro)
        flash(f'The product {name} has been added to your database', 'success')
        db.session.commit()
        return redirect(url_for('admin')) 
    return render_template('products/addproduct.html', form=form, title='Add Product Page', brands=brands, categories=categories)


@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    form = Addproducts(request.form)
    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.brand_id = brand
        product.category_id = category
        product.colors = form.colors.data
        product.description = form.description.data
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
                
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
                
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        db.session.commit()
        flash(f'Product updated successfully', 'success')
        return redirect(url_for('admin'))
    
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.description.data = product.description
    return render_template('products/updateproduct.html', form=form, title='Update product',
                           brands=brands, categories=categories, product=product)
    
    
@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method == 'POST':
        try:
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_1))
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_2))
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_3))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} has been deleted successfully', 'success')
        return redirect(url_for('admin'))
    flash(f'Error deleting the product', 'danger')        
    return redirect(url_for('admin'))