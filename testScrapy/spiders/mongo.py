"""

from flask_pymongo import PyMongo
#from blog.models import Blog, Post
import datetime

app.config['MONGO_DBNAME']='AppPythonR'
app.config['MONGO_URI']='mongodb://127.0.0.1:27017/AppPythonR'


mongo = PyMongo(app)	#contiene la conexion a mongo
def count_blog():
	cnt=0
	blog=mongo.db.Blog
	num_reg=blog.find().count()
	if num_reg==None:
		return cnt
	else:
		return num_reg

def get_max_id(_collection):
	id=[]
	if _collection=='blog':
		collection=mongo.db.Blog
	if _collection=='post':
		collection=mongo.db.Post
	if _collection=='author':
		collection=mongo.db.User
	if _collection=='category':
		collection=mongo.db.category
	max_id=collection.find().sort([('id', -1)]).limit(1)   #recupera el ultimo id de la colleccion author
	for reg in max_id:
		id.append(reg['id'])
		id.append(reg['_id'])
	return id

def get_id_author():
	id=[]
	author=mongo.db.User
	max_id=author.find().sort([('id', -1)]).limit(1)   #recupera el ultimo id de la colleccion author
	for reg in max_id:
		id.append(reg['id'])
	return id

def get_id_blog():
	id=[]
	blog=mongo.db.Blog
	max_id=blog.find().sort([('id', -1)]).limit(1)   #recupera el ultimo id
	for reg in max_id:
		id.append(reg['id'])
	return id

def find_login_operation(usr):
	b=[]
	collection=mongo.db.User
	a =collection.find({'username':usr})
	for reg in a:
		b.append(reg['username'])
		b.append(reg['password'])
	return b


def drop_twitts():
	try:
		coll_insert_twitts=mongo.db.insert_twitts
		coll_insert_twitts.drop()
		return True
	except:
		return False

def insert_twitts(numero,Twett,prob_si,prob_no,V4):
	try:
		coll_insert_twitts=mongo.db.insert_twitts

		coll_insert_twitts.insert({'numero': numero ,'Twett': Twett, 'prob_si':prob_si,'prob_no':prob_no,'flag':V4,'date':datetime.datetime.now() })
		return True
	except:
		return False


def update_active_inactive(numero):
	numero=int(numero)
	try:
		collection=mongo.db.insert_twitts
		result = collection.update({"numero": numero}, {"$set": {'flag':0}},upsert=False)
		return True
	except:
		return False




def update_inactive_active(numero):
	numero=int(numero)
	try:
		collection=mongo.db.insert_twitts
		result = collection.update({"numero": numero}, {"$set": {'flag':1}},upsert=False)
		return True
	except:
		return False

def find_tweets_objective():
	collection=mongo.db.insert_twitts
	a =collection.find({},{'numero':1,'Twett':1,'prob_si':1,'prob_no':1,'flag':1})
	return a

def find_tweets_others():
	collection=mongo.db.others_twitter
	a =collection.find({flag:0},{numero:1,Twett:1,prob_si:1,prob_no:1,flag:1})
	return a	
"""		

"""
def update_operation():
	return True



def insert_author_operation(id, fullname,email,username,password,is_author=False):
	coll_author=mongo.db.User
	coll_author.insert({'id': id,'fullname':fullname,'email':email,'username': username,'password':password,'is_author':is_author})
	return True

def insert_category(new_category):
	id=[]
	coll_category=mongo.db.category
	valida_existe=coll_category.find({'name':new_category})
	if valida_existe:
		return "category already exist"
	else:
		max_id=coll_category.find().sort([('id', -1)]).limit(1)   #recupera el ultimo id de la colleccion author
	for reg in max_id:
		id.append(reg['id'])
	id_=id[0]+1
	coll_category.insert({'id':id_,'name':new_category})
	return "Category added"

def get_id_new_category(new_category):
	_id=[]
	coll_category=mongo.db.category
	id_nc=coll_category.find({'name':new_category})
	for i in id_nc:
		_id.append(i['id'])
	if len(_id) > 1:
		value=_id[len(_id)-1]
	else:
		value=_id[0]
	return value

def get_category_name(id_category):
	_id=[]
	coll_category=mongo.db.category
	id_nc=coll_category.find({'id':id_category})
	for i in id_nc:
		_id.append(i['name'])
	if len(_id) > 1:
		value=_id[len(_id)-1]
	else:
		value=_id[0]
	return value

def insert_post(title,body,usr,category):
	_id_post=0
	coll_post=mongo.db.Post
	coll_blog=mongo.db.Blog
	coll_author=mongo.db.User
	author_id=[]
	blog_id=[]
	id_a=coll_author.find({'username':usr},{'id':1,'_id':0})
	for reg in id_a:
		author_id.append(reg['id'])
	id_b=coll_blog.find({'admin':author_id[0]},{'admin':1,'id':1,'_id':0})
	for reg in id_b:
		blog_id.append(reg['id'])
	post_id=get_max_id('post')
	if post_id:
		_id_post=post_id[0]
	else:
		_id_post=0
	if _id_post==None:
		_id_post=1
	else:
		_id_post+=1
	slug=True
	publish_date=datetime.datetime.now()
	live=True
	_category_id=category
	coll_post.insert({'id':float(_id_post),
					  'blog_id':blog_id[0],
					  'author_id':author_id[0],
					  'title':title,
					  'body':body,
					  'Slug':slug,
					  'publish_date':publish_date,
					  'live':live,
					  'category_id':float(_category_id)})
	return float(_id_post)

def id_blog_author():
	A=[]
	max_id_author=get_max_id('author')
	max_id_blog=get_max_id('blog')
	if max_id_author and max_id_blog:
		id_author=max_id_author[0]
		id_blog=max_id_blog[0]
	else:
		id_author=0
		id_blog=0
	if id_author==None or id_blog==None:
		id_author=1
		id_blog=1
	else:
		id_author+=1
		id_blog+=1
	A=[id_author,id_blog]
	return A

def get_posts():
	posts=[]
	collection=mongo.db.Post
	a =collection.find({"id": {"$lt": 10}}).sort([("id", 1), ("publish_date", -1)])
	return a


def get_post_edit(id_):
	post=[]
	Post=mongo.db.Post
	max_id=Post.find({'id':id_})
	for reg in max_id:
		post.append(reg['_id'])
		post.append(reg['id'])
		post.append(reg['blog_id'])
		post.append(reg['author_id'])
		post.append(reg['title'])
		post.append(reg['body'])
		post.append(reg['Slug'])
		post.append(reg['publish_date'])
		post.append(reg['live'])
	return post
"""