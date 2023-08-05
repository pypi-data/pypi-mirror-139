from requests import request
from roamPy.pageFunc import pageIterate

class subscriptionPeriod(object):

    def __init__(self, url, header):
        
        self.url = url 
        self.header = header

    
    def getAllSubPeriods(self):
        """
        Exports metadata for all subscription periods. A subscription period refers to a specific
        time frame for an agreement for a subscription. Cost information is associated with the 
        subscription period. A subscription period relates to one subscription but
        one subscription can have multiple subscription periods: one period for each signed agreement.

        :param self: Inherits url and header constructor values from the Roam class
        :return: A json object for every subscription period in the Roam.plus instance 
        """

        urlSubs = self.url + 'subscriptionPeriods'
        
        res = pageIterate(url = urlSubs, header=self.header)

        return(res)


    def getSubPeriodsBefore(self, date):
        """
        Exports the metadata for all subscriptions periods that begin before a given date

        :param self: Inherits url and header constructor values from the Roam class
        :param date: A string containing the data before which the subscription periods
                      should be returned. Must be fomatted 'YYYY-MM-DD'.
        :return: Metadata for all subscription periods beginning before the given date
        """

        urlSubsPeriodsBefore = self.url + 'subscriptionPeriods?filter[startsBefore]=' + date

        subPeriodsBefore = request("GET", url = urlSubsPeriodsBefore, headers=self.header)

        return(subPeriodsBefore.json())
         
    def getSubPeriodsAfter(self, date):
        """
        Exports the metadata for all subscriptions periods that begin after a given date

        :param self: Inherits url and header constructor values from the Roam class
        :param date: A string containing the data after which the subscription periods
                      should be returned. Must be fomatted 'YYYY-MM-DD'.
        :return: Metadata for all subscription periods beginning  after the given date
        """

        urlSubsPeriodsAfter = self.url + 'subscriptionPeriods?filter[startsAfter]=' + date

        subPeriodsAfter = request("GET", url = urlSubsPeriodsAfter, headers=self.header)

        return(subPeriodsAfter.json())

    def getSubPeriodsBetween(self, startDate, endDate):
        """
        Exports the metadata for all subscriptions periods that begin between two given dates

        :param self: Inherits url and header constructor values from the Roam class
        :param startDate: A string containing the data after which the subscription periods
                           should be returned. Must be fomatted 'YYYY-MM-DD'.
        :param endDate: A string containing the data before which the subscription periods
                         should be returned. Must be fomatted 'YYYY-MM-DD'.
        :return: Metadata for all subscription periods beginning between the two dates.
        """

        urlSubsPeriodsBetween = self.url + 'subscriptionPeriods?filter[startsBetween]=' + startDate + '..' + endDate

        subPeriodsBetween = request("GET", url = urlSubsPeriodsBetween, headers=self.header)

        return(subPeriodsBetween.json())

    
    def getSubPeriodById(self, id):
        """
        Exports the metadata for a subscription period with a given id

        :param self:  Inherits url and header constructor values from the Roam class
        :param id:   String containing numeric identifier of a subscription period
        :return: Metadata for the subscription with the given id number
        """
        urlSubPeriodId = self.url + 'subscriptionPeriods/' + id

        subPeriodId = request("GET", url=urlSubPeriodId, headers=self.header)

        return(subPeriodId.json())


    def getSubPeriodByIdwithRel(self, id, relations):
        """
        !This Method does not work. The endpoint is listed in the API docs but returns an error!

        Exports metadata for a subscription period with a given id and includes URLs of related 
        objects. 

        :param self: Inherits url and header constructor values from the Roam class
        :param id:   String containing numeric identifier of a subscription period
        :param relations: List of strings describing the realted record urls to return. 
                            Can be 'products' or 'vendor' or both.
        :return: Currently nothing as endpoint does not work yet. 
        """

        relStr = ','.join([str(item) for item in relations])

        urlSubPeriodIdwRel = self.url +'subscriptionPeriods/' + id + '?include=' + relStr

        subPeriodidwRel = request("GET", url=urlSubPeriodIdwRel, headers=self.header)

        return(subPeriodidwRel.json())

   



        