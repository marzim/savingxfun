#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mc185104
#
# Created:     01/27/2014
# Copyright:   (c) mc185104 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from model import Model
from datetime import date

class SavingsModel:

    db = Model().getDB()
    def get_allsavings(self):
        return

    def get_notes(self):
        return self.db.select('notes', order='id DESC')

    def new_notes(self, date_add, amount, comments):
        self.db.insert('notes', date_add=date_add, amount=amount, comments=comments)

    def delete_notes(self, id):
        self.db.delete('notes', where="id=$id", vars=locals())

    def get_guidelines(self):
        return self.db.select('guides', order='id DESC', vars=locals())[0]

    def update_guidelines(self, id, sharevalue, penalty, patronage):
        self.db.update('guides', where='id=$id', vars=locals(), share_value=sharevalue, penalty=penalty, patronage=patronage)

    def get_loans(self):
        return self.db.select(['customers', 'loans'], where='loans.customerid=customers.id', order='loans.id DESC')

    def get_savingsLoans(self, mymonth=date.today().month, myyear=date.today().year):
        results = self.db.query("select sum(l.amount) as totalloan_amounts, sum(l.total_payment) as totalloan_payments from loans l inner join " +
        "contribution_month cm on month(str_to_date(concat(cm.month,' ',cm.year),'%M %d %Y')) = month(l.date_rel) " +
        "where year(l.date_rel) = " + str(myyear) + " and month(l.date_rel) = " + str(mymonth))

        return results;

    def get_savingsContributions(self, mymonth=date.today().month, myyear=date.today().year):
        results = self.db.query("select sum(c.amount) as contributions_amount, sum(c.penalty) as totalpenalty " +
        "from contributions c inner join contribution_month cm on cm.id = c.month_id " +
        "where year(c.date_paid) = " + str(myyear) + " and month(str_to_date(concat(cm.month,' ',cm.year),'%M %d %Y')) = " + str(mymonth))

        return results;

    def get_post(self,id,uid):
        try:
            return self.db.select('entries', where='id=$id and userid='+ str(uid), vars=locals())[0]
        except IndexError:
            return None

    def get_loan(self,id):
        try:
            return self.db.select('loans', where='id=$id', vars=locals())[0]
        except IndexError:
            return None

    def new_loan(self, customerid, date_rel, date_due, amount, interest, total_payable,
                total_payment, outstanding_bal, fully_paidon):
        self.db.insert('loans', customerid=customerid, date_rel=date_rel, date_due=date_due, amount=amount, interest=interest,
                total_payable=total_payable, total_payment=total_payment, outstanding_bal=outstanding_bal, fully_paidon=fully_paidon)

    def del_post(self,id):
        self.db.delete('entries', where="id=$id", vars=locals())

    def update_loan(self,id, date_rel, date_due, amount, interest, total_payable,
                total_payment, outstanding_bal, fully_paidon):
        self.db.update('loans', where="id=$id", vars=locals(), date_rel=date_rel, date_due=date_due, amount=amount, interest=interest,
                total_payable=total_payable, total_payment=total_payment, outstanding_bal=outstanding_bal, fully_paidon=fully_paidon)


