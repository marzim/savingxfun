import web

web.config.debug = False

urls = (
'/', 'Index',
'/login/?','login.Login',
'/users/?','login.Users',
'/users/edit/(\d+)', 'login.EditUser',
'/logout/?','Logout',
'/register/?', 'register.Register',
'/savings/?', 'savings.Savings',
'/savings/contributions/?', 'savings.Contributions',
'/savings/notes/?', 'savings.Notes',
'/savings/notes/add/?', 'savings.AddNotes',
'/savings/contributions/view/(\d+)', 'savings.ViewContributions',
'/savings/contributions/add/(\d+)/(\d+)', 'savings.NewContributions',
'/savings/guidelines/?', 'savings.Guidelines',
'/savings/loans/?', 'savings.Loans',
'/savings/loans/add/?', 'savings.AddLoan',
'/savings/loans/edit/(\d+)', 'savings.EditLoan',
'/savings/customers/?', 'savings.Customers',
'/savings/customers/add/?', 'savings.AddCustomer',
'/savings/customers/interestearned/?', 'savings.CustomersEarned',
'/errorpage/?','ErrorPage',
'/savings/customers/edit/(\d+)', 'savings.EditCustomer',
)

app = web.application(urls, globals())
store = web.session.DiskStore('sessions')
session = web.session.Session(app, store, initializer={'login': 0, 'privilege': 0, 'user': 'anonymous'})

web.config.smtp_server = 'smtp.gmail.com'
web.config.smtp_port = 587
web.config.smtp_username = 'savingxfun@gmail.com'
web.config.smtp_password = 'mar_180)(*'
web.config.smtp_starttls = True

t_globals = {
 'datestr': web.datestr,
 'session': session,
 'web': web,
 }

render = web.template.render('/home/savingxfun/main/savingxfun/templates', base='base', globals=t_globals)

def logged():
    if session.login > 0:
        return True
    else:
        return False

def withprivilege():
    if session.privilege == 1:
        return True
    else:
        return False

def logging(text):
    file = open("/home/savingxfun/main/savingxfun/log.txt", "wt")
    print >> file, text

def superuser():
    if session.user == "admin":
        return True
    else:
        return False

def formatNumber(number):
    return '{:20,.2f}'.format(number)

def sendemail(to, subject, message):
    web.sendmail('savingxfun@gmail.com', to, subject, message)

class Index:
    def GET(self):
        """Show page"""
        return render.index(10)

class Logout:
    def GET(self):
        session.login = 0
        session.kill()
        raise web.seeother('/')

class ErrorPage:
    def GET(self):
        return render.errorpage()

def notfound():
    raise web.seeother('/errorpage')

#app.notfound = notfound
application = app.wsgifunc()

