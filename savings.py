import web
from savingsmodel import SavingsModel
from customermodel import CustomerModel
from contribmodel import ContributionModel
from base import render,  withprivilege, sendemail, formatNumber, logging
from decimal import Decimal
from datetime import date

model = SavingsModel()
custmodel = CustomerModel()
contribmonth_model = ContributionModel()
contribmodel = ContributionModel()

class Savings:

    def GET(self):
        if withprivilege():
            savings = model.get_allsavings()
            return render.savingssummary(savings)
        else:
            raise web.notfound()

class Contributions:

    def GET(self):
        if withprivilege():
            share_value = model.get_guidelines()['share_value']
            dict = []
            patronage = model.get_guidelines()['patronage']
            loans = model.get_loans()
            totalinterest = 0
            numberofpatronage = custmodel.get_numberofpatronage()
            for loan in loans:
                interest = loan.total_payable - loan.amount
                totalinterest += interest

            totalshares = custmodel.get_totalshares()
            totalpenalty = contribmodel.get_totalpenalty()
            for customer in custmodel.get_customers():
                total = customer.number_shares * share_value
                dict.append(self.get_contribAllCustomer(customer.id, customer.patronage, customer.name,
                            customer.number_shares, total, contribmodel.get_contribbycustid(customer.id),
                            patronage, totalshares,totalinterest, numberofpatronage, totalpenalty))
            return render.savingscontribs(dict)
        else:
            raise web.notfound()

    def get_contribAllCustomer(self, custid, custpat, name, numberShares, total, contributions,
                                patronage, totalshares, totalinterest, numberofpat, totalpenalty):
        contribAllcustomer = ContributionAllCustomer()
        contribAllcustomer.custid = custid
        contribAllcustomer.name = name
        contribAllcustomer.numberShares = numberShares
        contribAllcustomer.total = formatNumber(total)
        grandTotal = 0
        interest_perShare = 0
        interest_perCustomer = 0

        for contrib in contributions:
            if contrib.custid == custid:
                grandTotal += contrib.total

        if grandTotal > 0:
            patronage_interest = totalinterest * (float(patronage) / 100)
            interest_perShare = (Decimal(totalinterest) - Decimal(patronage_interest)) / Decimal(totalshares)
            interest_perCustomer = interest_perShare * numberShares + (Decimal(totalpenalty) / Decimal(totalshares))

            if custpat != 0:
                interest_perCustomer += Decimal(patronage_interest) / Decimal(numberofpat)

            logging("totalinterest: " + str(totalinterest) + " pat1: " + str(patronage_interest)
            + " interest: " + str(interest_perShare) + " interestpercustomer: " + str(interest_perCustomer) +
            " penalty: " + str(totalpenalty))

        contribAllcustomer.grandTotal = formatNumber(grandTotal)
        contribAllcustomer.interestpat = formatNumber(interest_perCustomer)
        contribAllcustomer.receivable = formatNumber(Decimal(interest_perCustomer) + Decimal(grandTotal))
        return contribAllcustomer


class ViewContributions:

    def GET(self,customer_id):
        if withprivilege():
            months = contribmonth_model.get_months()
            dict = []
            for month in months:
                dict.append(self.get_contribPerCustomer(month.id, month.month, file, contribmodel.get_contribbycustid(customer_id)))

            customer = custmodel.get_customerbyid(int(customer_id))
            share_value = formatNumber(customer.number_shares * model.get_guidelines()['share_value'])
            return render.savingscontribcustomer(dict,customer,share_value)
        else:
            raise web.notfound()

    def get_contribPerCustomer(self, monthid, month, file, contributions):
        contribpercustomer = ContributionPerCustomer()
        contribpercustomer.monthid = monthid
        contribpercustomer.month = month

        for contrib in contributions:
            if contrib.month_id == contribpercustomer.monthid:
                contribpercustomer.amount = formatNumber(contrib.amount)
                contribpercustomer.penalty = formatNumber(contrib.penalty)
                contribpercustomer.total = formatNumber(contrib.total)
                return contribpercustomer

        return contribpercustomer

class ContributionPerCustomer(object):
    def __init__(self, monthid=0, month=None, amount=0, penalty=0, total=0):
        self.monthid=monthid
        self.month=month
        self.amount=amount
        self.penalty=penalty
        self.total=total

class ContributionAllCustomer(object):
    def __init__(self, custid=0, name=None, numberShares=0, total=0, grandTotal=0, interestpat=0, receivable=0):
        self.custid=custid
        self.name=name
        self.numberShares=numberShares
        self.total=total
        self.grandTotal=grandTotal
        self.interestpat=interestpat
        self.receivable=receivable

class NewContributions:
    def GET(self, month_id, customer_id):
        if withprivilege():
            customer = custmodel.get_customerbyid(int(customer_id))
            contributions = contribmodel.get_specificContrib(int(customer_id), int(month_id))
            contribution = ''
            for contrib in contributions:
                if contrib.date_paid.year == date.today().year:
                    contribution = contrib
            values = {'customer': customer,
                    'month': contribmonth_model.get_month(month_id)['month'],
                    'shared_value': '{:20,.2f}'.format(customer.number_shares * model.get_guidelines()['share_value']),
                    'contrib': contribution,
                    'penalty':model.get_guidelines()['penalty'],
                    }
            return render.savingsnewcontrib(**values)
        else:
            raise web.notfound()

    def POST(self, month_id, customer_id):
        data = web.input()
        contribs = contribmodel.get_specificContrib(customer_id, month_id)
        contrib_id = 0
        for contrib in contribs:
            if contrib.date_paid.year == date.today().year:
                contrib_id = int(contrib.id)
        amount = data.newcontrib_amount.replace(',','')
        penalty = data.newcontrib_penalty.replace(',','')
        total = data.newcontrib_total.replace(',','')
        if contrib_id == 0:
            contribmodel.new_contribution(month_id, customer_id, Decimal(amount), int(data.ispenalty_hv),
                    Decimal(penalty), Decimal(total))
        else:
            contribmodel.update_contribution(contrib_id, month_id, customer_id, Decimal(amount), int(data.ispenalty_hv),
                    Decimal(penalty), Decimal(total))
        raise web.seeother('/savings/contributions/view/' + customer_id)

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

    def POST(self):
        data = web.input()
        model.update_guidelines(1, data.share_value, data.penalty, data.patronage)
        raise web.seeother('/savings/guidelines')

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
            custmodel.new_customer(data.name, Decimal(data.numbershares), int(data.patronage_hv), data.address, data.cellno, data.email)
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
            custmodel.update_customer(int(id), Decimal(data.numbershares), int(data.patronage_hv), data.address, data.cellno, data.email)
            raise web.seeother("/savings/customers")
        except Exception as ex:
            print ex


