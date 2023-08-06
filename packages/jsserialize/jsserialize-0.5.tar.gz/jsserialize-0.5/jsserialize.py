import json 
import importlib
import inspect
import sys

# This module defines the functions "encode" and "decode",
# which encode/decode data to and from json strings.
# Unlike the functions in the standard "json"
# package, these can automatically handle objects 
# of user-defined classes (and also deal with circular references).
#
# encode(data,custom_encode=None):
# Encode "data" to a json string. Use "custom_encode"
# to override the default encoding of objects.
#
# decode(jsonstr,custom_decode=None):
# Recreate data from a json string ("jsonstr").  
# Use "custom_decode" to override the default decoding of objects.
#
# Custom encode/decode:
# When we encode an object, we create a dictionary of 
# name/value pairs giving the object's attributes. This contains 
# the info needed to rebuild the object at decode time. The default 
# handling requires that the object's class have a default 
# constructor (ie., a constructor that doesn't accept 
# arguments, "MyClass()"). If that's not possible, you can
# pass a custom encoder to "encode" (and custom decoder to "decode").
# The custom encoder accepts an object and returns a dictionary;
# returning "None" means it wasn't encoded, and we should
# use the default handling. The custom decoder accepts a class name
# and dictionary and returns an object; returning "None" means
# it wasn't decoded, and we should use the default handling.
# Here's an example: we encode/decode a date from
# the datetime module.
#
'''
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
'''
# Note: in "custom_decode", "classname" is the full classname --
# the module name, followed by the name in the class definition.

# Copyright Al Cramer 2022 
# This code distributed under the MIT license

__version__ = '0.5'

# We throw these exceptions
class JSSerializeError(Exception):
    pass

# A reference to an object.
class __Ref():
    def __init__(self,id_=''):
        self.id = id_

    def __str__(self):
        return 'Ref:%s' % self.id

    def printme(self,indent=''):
        print('%s%s' % (indent,self.__str__()) )

# is "data" a leaf in the graph?
def is_leaf(data):
    return (data.__class__.__name__ in
        ['NoneType','bool','int','float','str','__Ref'])

# Walk "data", replacing direct object ref's with "__Ref" objects.
# During the walk, we'll also create a dictionary of objects
# that maps object_id -> object.
def add_refs(data,objdict):
    if is_leaf(data) or str(id(data)) in objdict:
        return

    if isinstance(data,list) or isinstance(data,tuple):
        for i in range(0,len(data)):
            e = data[i]
            add_refs(e,objdict)
            if hasattr(e,'__dict__'):
                if isinstance(data,tuple):
                    raise(JSSerializeError(
'Cannot serialize object in a tuple (use a list instead)'))
                data[i] = __Ref(str(id(e)))
        return

    def walk_dict(dct):
        for key,e in dct.items():
            if key == '*__JSSerializeClsName':
                raise(JSSerializeError(
'Cannot serialize dictionary: the key "*__JSSerializeClsName" is reserved'))
            add_refs(e,objdict)
            if hasattr(e,'__dict__'):
                dct[key] = __Ref(str(id(e)))

    if isinstance(data,dict):
        walk_dict(data)
    elif hasattr(data,'__dict__'):
        objdict[str(id(data))] = data
        walk_dict(data.__dict__)

# Walk "data", replacing "__Ref" objects with direct 
# object references.  This function un-does the transform made by "add_refs".
def resolve_refs(data,visited,objdict):
    if is_leaf(data) or data in visited:
        return

    if isinstance(data,list) or isinstance(data,tuple):
        for i in range(0,len(data)):
            e = data[i]
            if isinstance(e,__Ref):
                data[i] = objdict[e.id]
            resolve_refs(data[i],visited,objdict)
        return

    def walk_dict(dct):
        for key,e in dct.items():
            if isinstance(e,__Ref):
                dct[key] = objdict[e.id]
            resolve_refs(dct[key],visited,objdict)

    if isinstance(data,dict):
        walk_dict(data)
    elif hasattr(data,'__dict__'):
        visited.append(data)
        walk_dict(data.__dict__)

# test/dev
def print_objs(objdict):
    for key,e in objdict.items():
        print('*** %s' % key)
        if hasattr(e,printme):
            e.printme()
        else:
            print(e)
        print('')

def encode(data,custom_encode=None):
    # Serialize "data", returning a json string.

    # Walk tree, replacing direct object ref's with "__Ref" 
    # objects. During the walk, we'll also create a dictionary of objects
    # that maps object_id -> object.
    objdict = {}
    add_refs(data,objdict)
    # enable this code for dev/test/debug.
    # print_objs(objdict)

    # This function called by the json encoder when it finds
    # something that's not a simple scalar (bool, int, float, str)
    # or a list, tuple, or dictionary. So objects that are instances
    # of user-defined classes are handled here. Our job is to return
    # a dictionary that contains the info needed by the json decoder
    # to reconstruct the object. This consists of the class name of 
    # the object, plus the name/value pairs in obj.__dict__.
    # The dictionary entry for the class name has key "*__JSSerializeClsName".
    #
    def obj_to_dict(obj):
        cls = obj.__class__
        clsname = '%s.%s' % (cls.__module__,cls.__name__)
        if custom_encode is not None:
            d = custom_encode(obj)
            if d is not None:
                d['*__JSSerializeClsName'] =  clsname
                return d
        if not hasattr(obj,'__dict__'):
                raise(JSSerializeError(
'cannot encode object of class "%s" (use custom endcode)' % clsname))
        d = {
            '*__JSSerializeClsName': clsname
            }
        for key,v in obj.__dict__.items():
            if key == '__Ref':
                raise(JSSerializeError(
'encode: name "__Ref" is reserved (used by the serializer)'))
            d[key] = v
        return d

    # create the json encoding for [objdict,data]
    json_str =  json.dumps([objdict,data], indent=2, default=obj_to_dict) 

    # Before invoking the json encoder, we replaced direct ref's
    # with __Ref objects. Restore the tree to its
    # original state.
    visited = []
    resolve_refs(data,visited,objdict)

    # return the encoding
    return json_str

def decode(src,custom_decode=None):
    # Recreate data from a json encoded string ("src")

    # Create a dictionary mapping class_name -> class
    classdict = {}
    for modname,mod in sys.modules.items():
        for attrname in dir(mod):
            attr = getattr(mod, attrname)
            if inspect.isclass(attr):            
                classdict['%s.%s' % (modname,attrname)] = attr

    # When the json decoder hits a dictionary, it calls "object_hook"
    # (see below), passing it the dictionary.
    # This is where we re-create objects whose attributes
    # were encoded earlier. If we don't think that this dictionary
    # represents an encoded object, we just return it.
    #
    # During serialization, we added the name/value pair:
    # "*__JSSerializeClsName" : object_classname
    # to the dictionary encoding the object. So if the dictionary
    # we're passed contains the key "*__JSSerializeClsName", we take it to be 
    # an encoded object. This means that, if you try to
    # encode/decode a Python dictionary that contains an entry 
    # named "*__JSSerializeClsName", it's going to except at runtime. 
    # So don't use "*__JSSerializeClsName" as a dictionary key.
    # 
    # A second caveat: to recreate an object of class "MyClass",
    # we call the default constructor ("MyClass()"). If the class
    # has no default constructor, this will also except at runtime.
    # So make sure all your classes have default constructors. 
    def object_hook(dct):
        if '*__JSSerializeClsName' in dct:
            classname = dct['*__JSSerializeClsName']
            if custom_decode is not None:
                _dct = dct.copy()
                del _dct['*__JSSerializeClsName']
                obj = custom_decode(classname,_dct)
                if obj is not None:
                    return obj

            if not classname in classdict:
                raise(JSSerializeError(
    'class "%s" is not defined in any of the loaded modules' % classname))
            try:
                obj = classdict[classname]()
            except:
                raise(JSSerializeError(
    'class "%s" has no default constructor' % classname))
            for key,e in dct.items():
                if key != '*__JSSerializeClsName':
                    setattr(obj,key,e)
            return obj
        return dct

    # Decode "src": we get back an object dictionary and the
    # data (in which direct object ref's have been replaced 
    # by "__Ref" objects) (see "serialize" for details).
    [objdict,data] = json.loads(src,object_hook=object_hook)

    # resolve object refs
    visited = []
    resolve_refs(data,visited,objdict)
    return data


