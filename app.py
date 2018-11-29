#!flask/bin/python

from flask import Flask, jsonify,request
from datetime import datetime
import objectpath

app = Flask(__name__)

pantry = [
    {
         'id':1,
	 'item':u'Baked Beans',
	 'exp_date':'28/08/2018',
	 'exp':False
    },
    {
         'id':2,
	 'item':u'Spagetti',
	 'exp_date':'01/09/2018',
	 'exp':False
    },
    {
	 'id':3,
	 'item':u'Olive Oil',
 	 'exp_date':'25/08/2018',
	 'exp':False
    },
    {
	 'id':4,
	 'item':u'Tomato & Onion Mix',
	 'exp_date':'28/10/2018',
	 'exp':False
    }

]

recipe = [
    {
         'id':1,
	 'name':u'Pasta Mix',
	 'ingredients':['Spagetti','Tomato & Onion Mix','Olive Oil','Basil'],
	 'instructions':['Bring water to a boil',
	                  'Add a cup of Olive Oil',
			  'Add Spagetti',
			  'Boil for approx 20min',
			  'Drain water',
			  'Rinse pasta with cold water',
			  'Add tin of Tomatoe & Onion Mix',
			  'Stir while on stove for 5min',
			  'Serve']
    }
]

#get all items
@app.route('/foody/api/pantry/',methods=['GET'])
def get_items():
   return jsonify({'pantry':pantry})

#get one item using item id
@app.route('/foody/api/pantry/<int:item_id>',methods=['GET'])
def get_item(item_id):
    item = [item for item in pantry if item['id'] == item_id]
    if len(item) == 0:
        abort(404)

    return jsonify({'item':item[0]})

#get all recipes
@app.route('/foody/api/recipe/',methods=['GET'])
def get_recipes():
    return jsonify({'recipe':recipe})


#add items to pantry
@app.route('/foody/api/pantry',methods=['POST'])
def add_item():
    if not request.json or not 'item' in request.json:
        print "Abort"

    item = {
        'id':pantry[-1]['id'] +1,
        'item':request.json[0]['item'],
        'exp_date':request.json[1]['exp_date'],
        'exp':False
    }
    pantry.append(item)
    return jsonify({'item':item}),201

@app.route('/foody/api/suggested/',methods=['GET'])
#TODO: Iterate through recipes to get maches on ingedients and pantry items in stock
def check_recipe():
    tree_obj_pantry = objectpath.Tree(pantry)
    pantry_items = tuple(tree_obj_pantry.execute('$..item'))
    exp_dates = tuple(tree_obj_pantry.execute('$..exp_date'))
    response = []
    #TODO: check date needs to be today
    check_date = datetime.strptime("30/08/2018","%d/%m/%Y")

    for c,item in enumerate(recipe[0]['ingredients']):
        if item in pantry_items:
            item_date = datetime.strptime(exp_dates[pantry_items.index(item)],"%d/%m/%Y")
            if item_date < check_date:
                response.append("%s,expired at %s" %(item,exp_dates[c]))
                pass
            else:
                response.append("%s, in stock" %item)

        else:
            response.append("%s, out of stock" %item)

    return jsonify({'response':response})




#TODO:suggest recipe according to expiry dates
#page through all recipes, and checks against expiry dates

if __name__ == '__main__':
    app.run()
