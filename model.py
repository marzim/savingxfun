#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mc185104
#
# Created:     11/12/2013
# Copyright:   (c) mc185104 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import web

class Model:

    def getDB(self):
        return web.database(dbn='mysql', db='savingxfun$savings', user='savingxfun', pw='mustard_180', host='mysql.server')
