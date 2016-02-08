from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask (__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

#Return the JSON for all the Menu Items at a Restaurant
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    #grab items from backend
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	return jsonify(MenuItem =[i.serialize for i in items])

#Return the JSON for a selected menu item at a Restaurant
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_item_id>/JSON')
def restaurantMenuItemJSON(restaurant_id,menu_item_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    #grab menu item based on id
    item = session.query(MenuItem).filter_by(id=menu_item_id).one()
    return jsonify(MenuItem =item.serialize)

#add JSON API endpoint here
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/menu')

def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
	return render_template( 'menu.html', restaurant=restaurant, items =items, restaurant_id=restaurant_id)

#add a new menu item using the newmenuitem template
@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):

	if request.method == 'POST':
		newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('newmenuitem.html',restaurant_id=restaurant_id)


#edit the menu item based on an Id
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editMenuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
        	editedItem.name = request.form['name']
        if request.method['description']:
        	editedItem.description = request.form['description']
        if request.method['price']:
        	editedItem.price = request.form['price']
        if request.method['course']:
        	editedItem.course = request.form['course']

		session.add(editedItem)
		session.commit()
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:

		return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editMenuItem)


#delete a menu item from our restaurants
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id,menu_id):
	itemToDelete = session.query(Restaurant).filter_by(id=menu_id).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('deleteconfirmation.html, item=itemToDelete')

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
