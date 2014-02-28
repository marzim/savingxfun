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

class SavingsModel:

    db = Model().getDB()
    def get_allsavings(self):
        return

    def get_guidelines(self):
        return

    def get_loans(self):
        return self.db.select(['customers', 'loans'], where='loans.customerid=customers.id', order='loans.id DESC')

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


