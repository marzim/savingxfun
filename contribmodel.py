#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mc185104
#
# Created:     1/27/2014
# Copyright:   (c) mc185104 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import datetime
from model import Model

class ContributionModel:

    db = Model().getDB()
    def get_months(self):
        return self.db.select('contribution_month', order='id ASC')

    def get_month(self,id):
        try:
            return self.db.select('contribution_month', where='id=$id', vars=locals())[0]
        except IndexError:
            return None

    def get_contribbycustid(self, custid):
        try:
            return self.db.select('contributions', where='custid=' + str(custid))
        except IndexError:
            return None

    def get_totalpenalty(self):
        results = self.db.query("select sum(penalty) as totalpenalty from contributions")
        return results[0].totalpenalty

    def get_specificContrib(self, customer_id, month_id):
        return self.db.select('contributions', where='custid=$customer_id and month_id=$month_id', vars=locals())

    def new_contribution(self, month_id, custid, amount, ispenalty, penalty, total):
        self.db.insert('contributions', month_id=month_id, custid=custid, amount=amount, ispenalty=ispenalty,
                        penalty=penalty, total=total, date_paid=datetime.datetime.utcnow())

    def update_contribution(self, id, month_id, custid, amount, ispenalty, penalty, total):
        self.db.update('contributions', where='id=$id', vars=locals(), month_id=month_id, custid=custid, amount=amount, ispenalty=ispenalty,
                        penalty=penalty, total=total, date_paid=datetime.datetime.utcnow())


