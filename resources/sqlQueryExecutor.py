'''
Created on Oct 29, 2010

@author: egg.davis

Allows the execution of an arbitrary SQL select statement. Present for situations where the DAOs can't answer a 
question. Should perhaps have a sugar coating in pythonutilities. Please use with caution, as there is no protection
against queries which return an unacceptably large amount of data.

'''
from crn import dataSource,printlist
import re

def executeQuery(query):
    ''' executes an arbitrary SQL query, returning the resultset as a python list. '''
    connection = getConnection()
    statement = connection.prepareStatement(query)
    forbiddenWords = "insert|update|delete"
    if re.search(forbiddenWords,query,re.IGNORECASE):
        raise Exception("Queries containing inserts, updates, or deletions are forbidden.")
    resultset = statement.executeQuery()
    return listFromResultSet(resultset)

def listFromResultSet(resultset):
    numColumns = resultset.getMetaData().getColumnCount()
    resultlist = []
    while resultset.next():
        row = []
        for i in range(numColumns):
            row.append(str(resultset.getString(i+1))) # damn thing is 1-indexed
        resultlist.append(row)
    return resultlist


def getConnection():
    connection = dataSource.getConnection()
    #print "Connection:",type(connection)
    return connection


