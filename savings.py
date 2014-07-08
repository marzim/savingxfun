import web
import calendar
from savingsmodel import SavingsModel
from customermodel import CustomerModel
from contribmodel import ContributionModel
from base import render,  withprivilege, sendemail, formatNumber, logging
from decimal import Decimal
from datetime import date
from datetime import datetime

model = SavingsModel()
custmodel = CustomerModel()
contribmonth_model = ContributionModel()
contribmodel = ContributionModel()

class Savings:

    def GET(self):
        if withprivilege():
            savings = []
            wamount = contribmodel.get_withdrawnamount()
            outstanding_bal = model.get_outstandingbal()
            cashinbank = model.get_cashinbank()
            if not wamount:
                wamount = 0
            for month in range(1, 12):
                contribamount = 0
                totalpenalty = 0
                totalloan_amounts = 0
                totalloan_payments = 0
                contribamount = self.get_value(model.get_savingsContributions(month)[0].contributions_amount)
                totalpenalty = self.get_value(model.get_savingsContributions(month)[0].totalpenalty)
                totalloan_amounts =  self.get_value(model.get_savingsLoans(month)[0].totalloan_amounts) / 2
                totalloan_payments = self.get_value(model.get_savingsLoans(month)[0].totalloan_payments) / 2
                total = Decimal(contribamount) + Decimal(totalpenalty) + Decimal(totalloan_payments) - Decimal(totalloan_amounts)
                savings.append(self.get_savingsSummary(month, calendar.month_name[month], contribamount, totalpenalty,
                        totalloan_amounts, totalloan_payments, total))

            return render.savingssummary(savings,formatNumber, Decimal(wamount), formatNumber(outstanding_bal), cashinbank, Decimal)
        else:
            raise web.notfound()

    def get_savingsSummary(self, monthid, month, amount, penalty, loan_amount, loan_payment, total):
        savingsSummary = SavingsSummary()
        savingsSummary.monthid = monthid
        savingsSummary.month = month

        savingsSummary.amount = amount
        savingsSummary.penalty = penalty
        savingsSummary.loan_amount = loan_amount
        savingsSummary.loan_payment = loan_payment
        savingsSummary.total = total

        return savingsSummary

    def get_value(self,value):
        if value:
            return value
        else:
            return 0

class SavingsSummary(object):
    def __init__(self, monthid=0, month=None, amount=0, penalty=0, loan_amount=0, loan_payment=0, total=0):
        self.monthid=monthid
        self.month=month
        self.amount=amount
        self.penalty=penalty
        self.loan_amount=loan_amount
        self.loan_payment=loan_payment
        self.total=total

class SavingsWithdraw(object):

    def POST(self):
        if withprivilege():
            data = web.input()
            contribmodel.update_contributions_withdraw(data.customerId, 1)
            raise web.seeother('/savings/contributions/')

class Contributions:

    def GET(self):
        if withprivilege():
            share_value = model.get_guidelines()['share_value']
            contributions = []
            savingsInterest = SavingsInterestShare().calculate()

            for customer in custmodel.get_customers():
                total = customer.number_shares * share_value
                contributions.append(self.get_contribAllCustomer(customer.id, customer.patronage, customer.name,
                            customer.number_shares, total, contribmodel.get_contribbycustid(customer.id),
                            savingsInterest))
            return render.savingscontribs(contributions,formatNumber)
        else:
            raise web.notfound()

    def get_contribAllCustomer(self, custid, custpat, name, numberShares, total, contributions,
                                savingsInterest):
        contribAllcustomer = ContributionAllCustomer()
        contribAllcustomer.custid = custid
        contribAllcustomer.name = name
        contribAllcustomer.numberShares = numberShares
        contribAllcustomer.total = total
        grandTotal = 0
        interest_perCustomer = 0

        for contrib in contributions:
            if contrib.custid == custid:
                grandTotal += contrib.total

        if grandTotal > 0:
            interest_perCustomer = savingsInterest.interestpershare * numberShares + (Decimal(savingsInterest.penaltyshare))

            if custpat != 0:
                interest_perCustomer += Decimal(savingsInterest.patronagepercentage) / Decimal(savingsInterest.numberofpatronage)

        contribAllcustomer.grandTotal = grandTotal
        contribAllcustomer.interestpat = interest_perCustomer
        contribAllcustomer.receivable = Decimal(interest_perCustomer) + Decimal(grandTotal)
        return contribAllcustomer

class ViewContributions:

    def GET(self,customer_id):
        if withprivilege():
            months = contribmonth_model.get_months()
            dict = []
            for month in months:
                dict.append(self.get_contribPerCustomer(month.id, month.month, contribmodel.get_contribbycustid(customer_id)))

            customer = custmodel.get_customerbyid(int(customer_id))
            share_value = formatNumber(customer.number_shares * model.get_guidelines()['share_value'])
            return render.savingscontribcustomer(dict,customer,share_value)
        else:
            raise web.notfound()

    def get_contribPerCustomer(self, monthid, month, contributions):
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

class Notes:
    def GET(self):
        if withprivilege():
            notes = AllNotes().retrieve()
            return render.savingsnotes(notes,formatNumber)

class AddNotes:

    def POST(self):
        if withprivilege():
            data = web.input()
            dateadd = datetime.strptime(data.date_add, '%m-%d-%Y')
            model.new_notes(dateadd, Decimal(data.amount), data.comments)
            return web.seeother('/savings/notes')

class AllNotes(object):
    def __init__(self, id=0,date_add=None,amount=0,comments=None):
        self.id=id
        self.date_add=date_add
        self.amount=amount
        self.comments=comments

    def retrieve(self):
        notes = model.get_notes()
        noteslist = []
        for note in notes:
            allNotes = AllNotes()
            allNotes.id=note.id
            allNotes.date_add=note.date_add
            allNotes.amount=note.amount
            allNotes.comments=note.comments
            noteslist.append(allNotes)
        return noteslist


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
            loansList = []
            for loan in loans:
                loansList.append(SavingsLoan(loan.id,loan.name,loan.date_rel,loan.date_due,
                                loan.amount,loan.interest,loan.total_payable,loan.total_payment,
                                loan.outstanding_bal,loan.fully_paidon))
            return render.savingsloan(loansList,datetime,formatNumber)
        else:
            raise web.notfound()

class SavingsLoan(object):
    def __init__(self,id=0,name=None,date_rel=date.today(),date_due=date.today(),amount=0,interest=0,total_payable=0,total_payment=0,outstanding_bal=0,fully_paidon=date.today()):
        self.id=id
        self.name=name
        self.date_rel=date_rel
        self.date_due=date_due
        self.amount=amount
        self.interest=interest
        self.total_payable=total_payable
        self.total_payment=total_payment
        self.outstanding_bal=outstanding_bal
        self.fully_paidon=fully_paidon


class AddLoan:
    def GET(self):
        if withprivilege():
            customers = custmodel.get_customers()
            return render.savingsnewloan(customers, None, "", "New", "")
        else:
            raise web.notfound()

    def POST(self):
        data = web.input()
        daterel = datetime.strptime(data.date_rel, '%m-%d-%Y')
        model.new_loan(int(data.name),daterel,data.date_due,Decimal(data.amount),
                    Decimal(data.interest),Decimal(data.t_payable),Decimal(data.t_payment),
                    Decimal(data.outs_bal),data.fully_paidon)
        raise web.seeother('/savings/loans')

class EditLoan:
    def GET(self,id):
        if withprivilege():
            loan = model.get_loan(int(id))
            daterel = datetime.strftime(loan.date_rel, '%m-%d-%Y')
            name = custmodel.get_customerbyid(loan.customerid)['name']
            return render.savingsnewloan(None, loan, name, "Edit", daterel)
        else:
            raise web.notfound()

    def POST(self,id):
        try:
            data = web.input()
            daterel = datetime.strptime(data.date_rel, '%m-%d-%Y')
            model.update_loan(int(id),daterel,data.date_due,Decimal(data.amount),
                    Decimal(data.interest),Decimal(data.t_payable),Decimal(data.t_payment),
                    Decimal(data.outs_bal),data.fully_paidon)
            raise web.seeother('/savings/loans')

        except Exception as ex:
            logging(ex)

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

class CustomersEarned:
    def GET(self):
        if withprivilege():
            custearned = []
            savingsInterest = SavingsInterestShare().calculate()
            for customer in custmodel.get_customers():
                patronage=0
                interest_perCustomer = savingsInterest.interestpershare * customer.number_shares + (Decimal(savingsInterest.penaltyshare))
                if customer.patronage != 0:
                    patronage = Decimal(savingsInterest.patronagepercentage) / Decimal(savingsInterest.numberofpatronage)

                custearned.append(CustomersInterestEarned(customer.name,interest_perCustomer,patronage))
            return render.savingscustomersearned(custearned, savingsInterest, formatNumber)
        else:
            raise web.notfound()


class CustomersInterestEarned(object):
    def __init__(self,name=None,interest=0,patronage=0):
        self.name=name
        self.interest=interest
        self.patronage=patronage

class SavingsInterestShare(object):
    def __init__(self,interestpershare=0,patronagepercentage=0,penaltyshare=0,numberofpatronage=0,totalshares=0):
        self.interestpershare=interestpershare
        self.patronagepercentage=patronagepercentage
        self.penaltyshare=penaltyshare
        self.numberofpatronage=numberofpatronage
        self.totalshares=totalshares

    def calculate(self):
        savingsInterest = SavingsInterestShare()
        patronage = model.get_guidelines()['patronage']
        loans = model.get_loans()
        totalinterest = 0
        savingsInterest.numberofpatronage = custmodel.get_numberofpatronage()
        for loan in loans:
            interest = loan.total_payable - loan.amount
            totalinterest += interest

        savingsInterest.totalshares = custmodel.get_totalshares()
        savingsInterest.penaltyshare = Decimal(contribmodel.get_totalpenalty()) / Decimal(savingsInterest.totalshares)
        savingsInterest.patronagepercentage = totalinterest * (float(patronage) / 100)
        savingsInterest.interestpershare = (Decimal(totalinterest) - Decimal(savingsInterest.patronagepercentage)) / Decimal(savingsInterest.totalshares)
        return savingsInterest

