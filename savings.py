import web
from savingsmodel import SavingsModel
from customermodel import CustomerModel
from base import render,  withprivilege
from decimal import Decimal

model = SavingsModel()
custmodel = CustomerModel()

class Savings:

    def GET(self):
        if withprivilege():
            savings = model.get_allsavings()
            return render.savings(savings)
        else:
            raise web.notfound()

class Contributions:

    def GET(self):
        if withprivilege():
            return
        else:
            raise web.notfound()

class Loans:

    def GET(self):
        if withprivilege():
            loans = model.get_loans()
            return render.savingsloan(loans)
        else:
            raise web.notfound()

class AddLoan:
    def GET(self):
        if withprivilege():
            customers = custmodel.get_customers()
            return render.savingsnewloan(customers, None, "", "New")
        else:
            raise web.notfound()

    def POST(self):
        data = web.input()
        model.new_loan(int(data.name),data.date_rel,data.date_due,Decimal(data.amount),
                    Decimal(data.interest),Decimal(data.t_payable),Decimal(data.t_payment),
                    Decimal(data.outs_bal),data.fully_paidon)
        raise web.seeother('/savings/loans')

class EditLoan:
    def GET(self,id):
        if withprivilege():
            loan = model.get_loan(int(id))
            name = custmodel.get_customerbyid(loan.customerid)['name']
            return render.savingsnewloan(None, loan, name, "Edit")
        else:
            raise web.notfound()

    def POST(self,id):
        try:
            data = web.input()
            model.update_loan(int(id),data.date_rel,data.date_due,Decimal(data.amount),
                    Decimal(data.interest),Decimal(data.t_payable),Decimal(data.t_payment),
                    Decimal(data.outs_bal),data.fully_paidon)
            raise web.seeother('/savings/loans')

        except Exception as ex:
            print ex


class Guidelines:
    def GET(self):
        if withprivilege():
            guides = model.get_guidelines()
            return render.savingsguide(guides)
        else:
            raise web.notfound()

class Customers:
    def GET(self):
        if withprivilege():
            customers = custmodel.get_customers()
            return render.savingscustomers(customers)
        else:
            raise web.notfound()

class AddCustomer:
    def GET(self):
        if withprivilege():
            return render.savingsnewcustomer({
                'error' : '',
                'state':"New",
                }, None)
        else:
            raise web.notfound()

    def POST(self):
        data = web.input()
        if not self.userisexist(data.name):
            custmodel.new_customer(data.name, data.address, data.cellno, data.email)
            raise web.seeother("/savings/customers")
        else:
            return render.savingsnewcustomer({
                'error': "Username already exist",
                'state': "New"
            }, data)

    def userisexist(self,name):
        user = custmodel.get_customerbyname(name)
        if user is None:
            return False
        else:
            return True

class EditCustomer:
    def GET(self, id):
        if not withprivilege():
            raise web.seeother('/savings/customers')

        try:
            customer = custmodel.get_customerbyid(int(id))
            return render.savingsnewcustomer({
                'error':'',
                'state':'Edit',
            }, customer)
        except Exception as ex:
            print ex

    def POST(self, id):
        data = web.input()
        try:
            custmodel.update_customer(int(id), data.address, data.cellno, data.email)
            raise web.seeother("/savings/customers")
        except Exception as ex:
            print ex


