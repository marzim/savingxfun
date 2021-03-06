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
from datetime import date
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

    def get_contribbycustid(self, custid, withdrawn=0, myyear=date.today().year):
        try:
            return self.db.select('contributions', where='custid=' + str(custid) + ' and withdrawn=' + str(withdrawn) + ' and year(date_paid)=' + str(myyear))
        except IndexError:
            return None

    def get_totalpenalty(self, myyear=date.today().year):
        results = self.db.query("select sum(penalty) as totalpenalty from contributions where year(date_paid)=" + str(myyear))
        return results[0].totalpenalty

    def get_withdrawnamount(self, myyear=date.today().year):
        results = self.db.query("select sum(amount) as totalamount from contributions where withdrawn=1 and year(date_paid)=" + str(myyear))
        return results[0].totalamount

    def get_specificContrib(self, customer_id, month_id, myyear=date.today().year):
        return self.db.select('contributions', where='custid=$customer_id and month_id=$month_id and year(date_paid)=' + str(myyear), vars=locals())

    def new_contribution(self, month_id, custid, amount, ispenalty, penalty, total):
        self.db.insert('contributions', month_id=month_id, custid=custid, amount=amount, ispenalty=ispenalty,
                        penalty=penalty, total=total, date_paid=datetime.datetime.utcnow(),withdrawn=0)

    def update_contribution(self, id, month_id, custid, amount, ispenalty, penalty, total, withdrawn=0):
        self.db.update('contributions', where='id=$id', vars=locals(), month_id=month_id, custid=custid, amount=amount, ispenalty=ispenalty,
                        penalty=penalty, total=total, date_paid=datetime.datetime.utcnow(), withdrawn=withdrawn)

    def update_contributions_withdraw(self, custid, withdrawn=0, myyear=date.today().year):
        self.db.update('contributions', where='custid=$custid and year(date_paid)=' + str(myyear), vars=locals(), withdrawn=withdrawn)


