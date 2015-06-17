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


from model import Model

class CustomerModel:

    db = Model().getDB()
    def get_customers(self):
        return self.db.select('customers', order='id DESC')

    def get_customerbyid(self,id):
        try:
            return self.db.select('customers', where='id=$id', vars=locals())[0]
        except IndexError:
            return None

    def get_totalshares(self):
        results = self.db.query("select sum(number_shares) as totalshares from customers")
        return results[0].totalshares

    def get_numberofpatronage(self):
        results = self.db.query("select sum(patronage) as patronage from customers")
        return results[0].patronage

    def get_customerbyname(self,name):
        try:
            return self.db.select('customers', where='name=$name', vars=locals())[0]
        except IndexError:
            return None

    def new_customer(self, name, numbershares, patronage, address, cellno, email, member):
        self.db.insert('customers', name=name, number_shares=numbershares, patronage=patronage, address=address, cellno=cellno, email=email, member=member)

    def del_customer(self,id):
        self.db.delete('customers', where="id=$id", vars=locals())

    def update_customer(self, id, numbershares, patronage, address, cellno, email, member):
        self.db.update('customers', where='id=$id', vars=locals(), number_shares=numbershares, patronage=patronage, address=address, cellno=cellno, email=email, member=member)


