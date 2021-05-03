import web
web.config.debug = False
render = web.template.render('templates/')
###urls = ('/','index')
##urls = ('/(.*)', 'index')
urls=('/', 'index',
'/add', 'add')
db = web.database(
    dbn='postgres',
    host='127.0.0.1',
    port=5432,
    user='postgres',
    pw='password123@'#,
    #db='localhost',
)
class index:
    def GET(self):#,name):
        #name = 'Bob' 
        #return render.index(name)
        #i = web.input(name=None)
        #return render.index(i.name)
        #return render.index(name)
        todos = db.select('todo')
        return render.index(todos)
class add:
    def POST(self):
        i = web.input()
        n = db.insert('todo', title=i.title)
        post_data=web.input(name=[])
        raise web.seeother('/')

    
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
