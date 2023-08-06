## jsserialize.py: serialize python data structures as json strings

This module defines the functions "encode" and "decode",
which encode/decode data to and from json strings.
Unlike the functions in the standard "json" package,
these can automatically handle user-defined classes and circular references.

		jsserialize functions:

		encode(data,custom_encode=None):
			Encode "data" to a json string. 
			Use "custom_encode" to override the default encoding of objects.
			Returns: json string encoding of "data"

		decode(jsonstr,custom_decode=None):
			Recreate data from a json string ("jsonstr").  
			Use "custom_decode" to override the default decoding of objects.
			Returns: the recreated data

Custom encode/decode:

When we encode an object, we create a dictionary of 
name/value pairs giving the object's attributes. This contains 
the info needed to rebuild the object at decode time. The default 
handling requires that the object's class have a default 
constructor (ie., a constructor that doesn't accept arguments, "MyClass()").
If that's not possible, you can pass a custom encoder to "encode" 
(and custom decoder to "decode").

The custom encoder accepts an object and returns a dictionary.
Returning "None" means the object wasn't encoded, and we should
use the default handling. The custom decoder accepts a class name
and dictionary and returns an object. Returning "None" means
it wasn't decoded, and we should use the default handling.
Here's an example: we encode/decode a date from
the python datetime module.

		def custom_encode(obj):
    		if obj.__class__.__name__ == 'date':
        		# 'obj.isoformat()' returns a str
        		return {'isoformat': obj.isoformat()}
    		return None

		def custom_decode(classname,dct):
    		if classname == 'datetime.date':
        		# "fromisoformat" is class method that creates
        		# a date object from an isoformat string
        		return datetime.date.fromisoformat(dct['isoformat'])
    		return None

Note: in "custom_decode", "classname" is the full classname 
(module name, followed by the name in the class definition).

### Requirements and Installation
Requires Python 3.  Install with pip:

		pip install jsserialize

### Dev Notes
This repository contains "jsserialize.py". Additonal files ("setup.py",
"setup.cfg", and "hwoto_pypi.txt") are for uploading the module to pypi.

### Sample Code

		import jsserialize
		
		# We need some data to encode. We'll use a tree built from Nodes.
		# The base class None has a "parent" attribute and a list "kids"
		# containing child nodes. From the base class we define 2 subclasses,
		# "A" and "B". The A class has a "color" attribute whose value is a string.
		# The B class has a "date" attribute whose value is an object of class
		# "date", from the standard python "datetime" module.
		
		import datetime
		nodeid = 0
		class Node():
    		def __init__(self):
        		global nodeid
        		self.id = str(nodeid)
        		nodeid += 1
        		self.parent = None
        		self.kids = []
		
    		def add_kid(self,kid):
        		self.kids.append(kid)
        		kid.parent = self
		
    		def attrs_to_str(self):
        		# child classes override this to return a string giving
        		# attribute name/values.
        		return ''
		
    		def printme(self,indent=''):
        		pid = "None" if self.parent is None else self.parent.id
        		print('%s%s %s parent:%s %s' %
            		(indent,self.__class__.__name__,
            		self.id,pid,self.attrs_to_str()))
        		indent += '  '
        		for k in self.kids:
            		k.printme(indent)
		
		class A(Node):
    		def __init__(self,color='red'):
        		super().__init__()
        		self.color = color
		
    		def attrs_to_str(self):
        		return 'color:%s' % self.color
		
		class B(Node):
    		def __init__(self,date=None):
        		super().__init__()
        		self.date = date
		
    		def attrs_to_str(self):
        		return 'date:%s' % (
            		'None' if self.date is None else self.date.isoformat())
		
		# make the data we'll encode/decode: a tree built from A and B nodes.
		def make_data():
    		root = A()
    		kid1 = A('yellow')
    		kid2 = B(datetime.date.fromordinal(1))
    		root.add_kid(kid1)
    		root.add_kid(kid2)
    		kid2.add_kid( A('blue') )
    		kid2.add_kid( B(datetime.date.today()) )
    		return root
		
		# Here are the custom encode/decode functions. We need them
		# because our data includes objects of class "date"
		# from the python standard "datetime" module, and jsserialize
		# doesn't know how to encode/decode objects of that class.
		# Note that these encode/decode functions only need to handle
		# "date" objects -- our data also includes objects of class "A"
		# and "B", but jsserialize can handle them without our help. (For this
		# to work, we have to make sure our user-defined classes have
		# default constructors).
		
		def custom_encode(obj):
    		if obj.__class__.__name__ == 'date':
        		# 'obj.isoformat()' returns a str
        		return {'isoformat': obj.isoformat()}
    		# returning None tells jsserialize: we didn't encode the
    		# object, you do it.
    		return None
		
		def custom_decode(classname,dct):
    		# Notice that classname is the "full" name for the class:
    		# module name, followed the name that appeared in the
    		# class definition.
    		if classname == 'datetime.date':
        		# "fromisoformat" is class method that creates
        		# a date object from an isoformat string
        		return datetime.date.fromisoformat(dct['isoformat'])
    		# returning None tells jsserialize: we didn't decode the
    		# object, you do it.
    		return None
		
		def test():
    		# create data to be encoded: a tree built from nodes
    		data = make_data()
    		print("data to be encoded:")
    		data.printme()
		
    		# get the json string encoding
    		json_str = jsserialize.encode(data,custom_encode=custom_encode)
		
    		# decode the json_str, recreating the data
    		data2 = jsserialize.decode(json_str, custom_decode=custom_decode)
    		print("\ndecoded data:")
    		data2.printme()
		
    		# print the json string
    		print("\njson string:")
    		print(json_str)
		
		if __name__=='__main__':
    		test()

### Who do I talk to? ###

Al Cramer (ac2.7@1828@gmail.com)

Copyright Al Cramer 2022
