#proto-exp.py
#prototype for scannning exp dates and food description

from datetime import datetime



pantry = {

	'baked beans':{
	  
	   'exp':'30/06/18'
	  },

	'tuna':{
	   
	   'exp':'10/10/18'
	  },
	
	'spageti':{
	   
	   'exp':'20/08/18'
	},

	'olive oil':{
	   'exp':'20/08/18'
	},

	'tomato & onion mix':{
	   'exp':'21/08/18'
	}
}


#recipe

spageti = ['spageti','olive oil','tomato & onion mix','basil','baked beans']

#check_recipe

check_date = datetime.strptime("30/08/18","%d/%m/%y")

def check_recipe(recipe):
    for item in recipe:
        if item in pantry:
            item_date = datetime.strptime(pantry[item]['exp'],"%d/%m/%y")
            if item_date < check_date:
	      print "%s,expired at %s" %(item,pantry[item]['exp'])
	      pass
	    else:
              print "%s, in stock" %item
            
	else:
	    print "%s, out of stock" %item

check_recipe(spageti)

