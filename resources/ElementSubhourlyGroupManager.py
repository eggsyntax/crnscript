'''
Created on Jan 12, 2011

@author: jesse.davis
'''
from gov.noaa.ncdc.crn.domain import Element

class ElementSubhourlyGroupManager():
    '''
    Returns a subgroup and/or subhourly time for an element. Temporary class to be replaced by
    a manager in crnshared. Get an instance using ElementSubhourlyGroupManager.getManager()
    rather than creating a new instance.
    
    Note that while ids and times are keyed by actual element id (since they're unique per
    element id), names and descriptions are keyed by artificial group id (since there's only
    one per group). Note further that subhourlyTime and subhourlyName *must* be populated 
    before the id is changed to a group id. Ideally it'd be nice to find some way to ensure
    that...
    '''

    # Prefer passing around a single instance, which will gradually accumulate any elements
    # needed, to creating a new Manager each time.
    managerInstance = None
    @staticmethod
    def getManager():
        if ElementSubhourlyGroupManager.managerInstance is None:
            ElementSubhourlyGroupManager.managerInstance = ElementSubhourlyGroupManager()
        return ElementSubhourlyGroupManager.managerInstance
    
    def __init__(self):
        if ElementSubhourlyGroupManager.managerInstance is not None:
            raise TypeError("Do not attempt to instantiate ElementSubhourlyGroupManager"+
                            "directly; instead call ElementSubhourlyGroupManager.getManager().")
        self.subhourlyName = {}
        self.subhourlyId = {}
        self.subhourlyDescription = {}
        self.subhourlyTime = {}
        self.elementsgenerated = {}


    def generateElement(self,subId):
        self.populateMaps()
        try:
            e = self.elementsgenerated[subId]
        except KeyError:
            e = Element(subId,self.subhourlyName[subId],self.subhourlyDescription[subId])
        self.elementsgenerated[subId] = e
        return e
    
    def getId(self,elId):
        if not self.subhourlyId: self.populateIds()
        try:
            return self.subhourlyId[elId]
        except KeyError:
            return None
    
    def getTime(self,elId):
        if not self.subhourlyTime: self.populateTimes()
        try:
            return self.subhourlyTime[elId]
        except KeyError:
            return None
        
    def getNameFromId(self,id):
        if not self.subhourlyName: self.populateNames()
        try:
            return self.subhourlyName[id]
        except KeyError:
            try:
                return self.subhourlyName[self.getId(id)]
            except KeyError:
                return None
    
    def getDescriptionFromId(self,id):
        if not self.subhourlyDescription: self.populateDescriptions()
        try:
            return self.subhourlyDescription[id]
        except KeyError:
            try:
                return self.subhourlyDescription[self.getId(id)]
            except KeyError:
                return None

    def getAllIds(self):
        if not self.subhourlyId: self.populateIds()
        return set(self.subhourlyId.values())

    def populateMaps(self):
        if not self.subhourlyTime: self.populateTimes()
        if not self.subhourlyName: self.populateNames()
        if not self.subhourlyDescription: self.populateDescriptions()
        if not self.subhourlyId: self.populateIds()

    def populateIds(self):
        self.subhourlyId[314]=10000
        self.subhourlyId[315]=10000
        self.subhourlyId[316]=10000
        self.subhourlyId[317]=10000

        self.subhourlyId[319]=10001
        self.subhourlyId[320]=10001
        self.subhourlyId[321]=10001
        self.subhourlyId[322]=10001
        self.subhourlyId[323]=10001
        self.subhourlyId[324]=10001
        self.subhourlyId[325]=10001
        self.subhourlyId[326]=10001
        self.subhourlyId[327]=10001
        self.subhourlyId[328]=10001
        self.subhourlyId[329]=10001
        self.subhourlyId[330]=10001
        
        self.subhourlyId[331]=10002
        self.subhourlyId[332]=10002
        self.subhourlyId[333]=10002
        self.subhourlyId[334]=10002
        self.subhourlyId[335]=10002
        self.subhourlyId[336]=10002
        self.subhourlyId[337]=10002
        self.subhourlyId[338]=10002
        self.subhourlyId[339]=10002
        self.subhourlyId[340]=10002
        self.subhourlyId[341]=10002
        self.subhourlyId[342]=10002
        
        self.subhourlyId[30]=10003
        self.subhourlyId[31]=10003
        self.subhourlyId[32]=10003
        self.subhourlyId[33]=10003
        
        self.subhourlyId[62]=10004
        self.subhourlyId[63]=10004
        self.subhourlyId[64]=10004
        self.subhourlyId[65]=10004
        
        self.subhourlyId[74]=10005
        self.subhourlyId[75]=10005
        self.subhourlyId[76]=10005
        self.subhourlyId[77]=10005
        
        
        self.subhourlyId[53]=10006
        self.subhourlyId[54]=10006
        self.subhourlyId[55]=10006
        self.subhourlyId[56]=10006
        
        
        self.subhourlyId[87]=10007
        self.subhourlyId[96]=10007
        self.subhourlyId[105]=10007
        self.subhourlyId[114]=10007
        self.subhourlyId[123]=10007
        self.subhourlyId[132]=10007
        self.subhourlyId[141]=10007
        self.subhourlyId[150]=10007
        self.subhourlyId[159]=10007
        self.subhourlyId[168]=10007
        self.subhourlyId[177]=10007
        self.subhourlyId[186]=10007
        
        self.subhourlyId[88]=10008
        self.subhourlyId[97]=10008
        self.subhourlyId[106]=10008
        self.subhourlyId[115]=10008
        self.subhourlyId[124]=10008
        self.subhourlyId[133]=10008
        self.subhourlyId[142]=10008
        self.subhourlyId[151]=10008
        self.subhourlyId[160]=10008
        self.subhourlyId[169]=10008
        self.subhourlyId[178]=10008
        self.subhourlyId[187]=10008
        
        self.subhourlyId[89]=10009
        self.subhourlyId[98]=10009
        self.subhourlyId[107]=10009
        self.subhourlyId[116]=10009
        self.subhourlyId[125]=10009
        self.subhourlyId[134]=10009
        self.subhourlyId[143]=10009
        self.subhourlyId[152]=10009
        self.subhourlyId[161]=10009
        self.subhourlyId[170]=10009
        self.subhourlyId[179]=10009
        self.subhourlyId[188]=10009
        
        self.subhourlyId[90]=10010
        self.subhourlyId[99]=10010
        self.subhourlyId[108]=10010
        self.subhourlyId[117]=10010
        self.subhourlyId[126]=10010
        self.subhourlyId[135]=10010
        self.subhourlyId[144]=10010
        self.subhourlyId[153]=10010
        self.subhourlyId[162]=10010
        self.subhourlyId[171]=10010
        self.subhourlyId[180]=10010
        self.subhourlyId[189]=10010
        
        self.subhourlyId[91]=10011
        self.subhourlyId[100]=10011
        self.subhourlyId[109]=10011
        self.subhourlyId[118]=10011
        self.subhourlyId[127]=10011
        self.subhourlyId[136]=10011
        self.subhourlyId[145]=10011
        self.subhourlyId[154]=10011
        self.subhourlyId[163]=10011
        self.subhourlyId[172]=10011
        self.subhourlyId[181]=10011
        self.subhourlyId[190]=10011
        
        self.subhourlyId[92]=10012
        self.subhourlyId[101]=10012
        self.subhourlyId[110]=10012
        self.subhourlyId[119]=10012
        self.subhourlyId[128]=10012
        self.subhourlyId[137]=10012
        self.subhourlyId[146]=10012
        self.subhourlyId[155]=10012
        self.subhourlyId[164]=10012
        self.subhourlyId[173]=10012
        self.subhourlyId[182]=10012
        self.subhourlyId[191]=10012
        
        self.subhourlyId[93]=10013
        self.subhourlyId[102]=10013
        self.subhourlyId[111]=10013
        self.subhourlyId[120]=10013
        self.subhourlyId[129]=10013
        self.subhourlyId[138]=10013
        self.subhourlyId[147]=10013
        self.subhourlyId[156]=10013
        self.subhourlyId[165]=10013
        self.subhourlyId[174]=10013
        self.subhourlyId[183]=10013
        self.subhourlyId[192]=10013
        
        self.subhourlyId[94]=10014
        self.subhourlyId[103]=10014
        self.subhourlyId[112]=10014
        self.subhourlyId[121]=10014
        self.subhourlyId[130]=10014
        self.subhourlyId[139]=10014
        self.subhourlyId[148]=10014
        self.subhourlyId[157]=10014
        self.subhourlyId[166]=10014
        self.subhourlyId[175]=10014
        self.subhourlyId[184]=10014
        self.subhourlyId[193]=10014
        
        self.subhourlyId[95]=10015
        self.subhourlyId[104]=10015
        self.subhourlyId[113]=10015
        self.subhourlyId[122]=10015
        self.subhourlyId[131]=10015
        self.subhourlyId[140]=10015
        self.subhourlyId[149]=10015
        self.subhourlyId[158]=10015
        self.subhourlyId[167]=10015
        self.subhourlyId[176]=10015
        self.subhourlyId[185]=10015
        self.subhourlyId[194]=10015
        
        self.subhourlyId[359]=10016
        self.subhourlyId[358]=10016
        self.subhourlyId[357]=10016
        self.subhourlyId[356]=10016
        self.subhourlyId[355]=10016
        self.subhourlyId[354]=10016
        self.subhourlyId[353]=10016
        self.subhourlyId[352]=10016
        self.subhourlyId[351]=10016
        self.subhourlyId[350]=10016
        self.subhourlyId[349]=10016
        self.subhourlyId[348]=10016
        
        self.subhourlyId[407]=10017
        self.subhourlyId[406]=10017
        self.subhourlyId[405]=10017
        self.subhourlyId[404]=10017
        self.subhourlyId[403]=10017
        self.subhourlyId[402]=10017
        self.subhourlyId[401]=10017
        self.subhourlyId[400]=10017
        self.subhourlyId[399]=10017
        self.subhourlyId[398]=10017
        self.subhourlyId[397]=10017
        self.subhourlyId[396]=10017
        
        self.subhourlyId[395]=10018
        self.subhourlyId[394]=10018
        self.subhourlyId[393]=10018
        self.subhourlyId[392]=10018
        self.subhourlyId[391]=10018
        self.subhourlyId[390]=10018
        self.subhourlyId[389]=10018
        self.subhourlyId[388]=10018
        self.subhourlyId[387]=10018
        self.subhourlyId[386]=10018
        self.subhourlyId[385]=10018
        self.subhourlyId[384]=10018
        
        self.subhourlyId[383]=10019
        self.subhourlyId[382]=10019
        self.subhourlyId[381]=10019
        self.subhourlyId[380]=10019
        self.subhourlyId[379]=10019
        self.subhourlyId[378]=10019
        self.subhourlyId[377]=10019
        self.subhourlyId[376]=10019
        self.subhourlyId[375]=10019
        self.subhourlyId[374]=10019
        self.subhourlyId[373]=10019
        self.subhourlyId[372]=10019
        
        self.subhourlyId[371]=10020
        self.subhourlyId[370]=10020
        self.subhourlyId[369]=10020
        self.subhourlyId[368]=10020
        self.subhourlyId[367]=10020
        self.subhourlyId[366]=10020
        self.subhourlyId[365]=10020
        self.subhourlyId[364]=10020
        self.subhourlyId[363]=10020
        self.subhourlyId[362]=10020
        self.subhourlyId[361]=10020
        self.subhourlyId[360]=10020
        
        self.subhourlyId[411]=10021
        self.subhourlyId[412]=10021
        self.subhourlyId[413]=10021
        self.subhourlyId[414]=10021
        self.subhourlyId[415]=10021
        self.subhourlyId[416]=10021
        self.subhourlyId[417]=10021
        self.subhourlyId[418]=10021
        self.subhourlyId[419]=10021
        self.subhourlyId[420]=10021
        self.subhourlyId[421]=10021
        self.subhourlyId[422]=10021
        
        self.subhourlyId[426]=10022
        self.subhourlyId[427]=10022
        self.subhourlyId[428]=10022
        self.subhourlyId[429]=10022
        self.subhourlyId[430]=10022
        self.subhourlyId[431]=10022
        self.subhourlyId[432]=10022
        self.subhourlyId[433]=10022
        self.subhourlyId[434]=10022
        self.subhourlyId[435]=10022
        self.subhourlyId[436]=10022
        self.subhourlyId[437]=10022
        
        self.subhourlyId[571]=10023
        self.subhourlyId[572]=10023
        self.subhourlyId[573]=10023
        self.subhourlyId[574]=10023
        self.subhourlyId[575]=10023
        self.subhourlyId[576]=10023
        self.subhourlyId[577]=10023
        self.subhourlyId[578]=10023
        self.subhourlyId[579]=10023
        self.subhourlyId[580]=10023
        self.subhourlyId[581]=10023
        self.subhourlyId[582]=10023

        self.subhourlyId[583]=10024
        self.subhourlyId[584]=10024
        self.subhourlyId[585]=10024
        self.subhourlyId[586]=10024
        self.subhourlyId[587]=10024
        self.subhourlyId[588]=10024
        self.subhourlyId[589]=10024
        self.subhourlyId[590]=10024
        self.subhourlyId[591]=10024
        self.subhourlyId[592]=10024
        self.subhourlyId[593]=10024
        self.subhourlyId[594]=10024
        
        self.subhourlyId[595]=10025
        self.subhourlyId[596]=10025
        self.subhourlyId[597]=10025
        self.subhourlyId[598]=10025
        self.subhourlyId[599]=10025
        self.subhourlyId[600]=10025
        self.subhourlyId[601]=10025
        self.subhourlyId[602]=10025
        self.subhourlyId[603]=10025
        self.subhourlyId[604]=10025
        self.subhourlyId[605]=10025
        self.subhourlyId[606]=10025
        
        self.subhourlyId[607]=10026
        self.subhourlyId[608]=10026
        self.subhourlyId[609]=10026
        self.subhourlyId[610]=10026
        self.subhourlyId[611]=10026
        self.subhourlyId[612]=10026
        self.subhourlyId[613]=10026
        self.subhourlyId[614]=10026
        self.subhourlyId[615]=10026
        self.subhourlyId[616]=10026
        self.subhourlyId[617]=10026
        self.subhourlyId[618]=10026
        
        self.subhourlyId[619]=10027
        self.subhourlyId[620]=10027
        self.subhourlyId[621]=10027
        self.subhourlyId[622]=10027
        self.subhourlyId[623]=10027
        self.subhourlyId[624]=10027
        self.subhourlyId[625]=10027
        self.subhourlyId[626]=10027
        self.subhourlyId[627]=10027
        self.subhourlyId[628]=10027
        self.subhourlyId[629]=10027
        self.subhourlyId[630]=10027
        
        self.subhourlyId[631]=10028
        self.subhourlyId[632]=10028
        self.subhourlyId[633]=10028
        self.subhourlyId[634]=10028
        self.subhourlyId[635]=10028
        self.subhourlyId[636]=10028
        self.subhourlyId[637]=10028
        self.subhourlyId[638]=10028
        self.subhourlyId[639]=10028
        self.subhourlyId[640]=10028
        self.subhourlyId[641]=10028
        self.subhourlyId[642]=10028
        
        self.subhourlyId[643]=10029
        self.subhourlyId[644]=10029
        self.subhourlyId[645]=10029
        self.subhourlyId[646]=10029
        self.subhourlyId[647]=10029
        self.subhourlyId[648]=10029
        self.subhourlyId[649]=10029
        self.subhourlyId[650]=10029
        self.subhourlyId[651]=10029
        self.subhourlyId[652]=10029
        self.subhourlyId[653]=10029
        self.subhourlyId[654]=10029
        
        self.subhourlyId[655]=10030
        self.subhourlyId[656]=10030
        self.subhourlyId[657]=10030
        self.subhourlyId[658]=10030
        self.subhourlyId[659]=10030
        self.subhourlyId[660]=10030
        self.subhourlyId[661]=10030
        self.subhourlyId[662]=10030
        self.subhourlyId[663]=10030
        self.subhourlyId[664]=10030
        self.subhourlyId[665]=10030
        self.subhourlyId[666]=10030
        
        self.subhourlyId[667]=10031
        self.subhourlyId[668]=10031
        self.subhourlyId[669]=10031
        self.subhourlyId[670]=10031
        self.subhourlyId[671]=10031
        self.subhourlyId[672]=10031
        self.subhourlyId[673]=10031
        self.subhourlyId[674]=10031
        self.subhourlyId[675]=10031
        self.subhourlyId[676]=10031
        self.subhourlyId[677]=10031
        self.subhourlyId[678]=10031
        
        self.subhourlyId[679]=10032
        self.subhourlyId[680]=10032
        self.subhourlyId[681]=10032
        self.subhourlyId[682]=10032
        self.subhourlyId[683]=10032
        self.subhourlyId[684]=10032
        self.subhourlyId[685]=10032
        self.subhourlyId[686]=10032
        self.subhourlyId[687]=10032
        self.subhourlyId[688]=10032
        self.subhourlyId[689]=10032
        self.subhourlyId[690]=10032
        
        self.subhourlyId[691]=10033
        self.subhourlyId[692]=10033
        self.subhourlyId[693]=10033
        self.subhourlyId[694]=10033
        self.subhourlyId[695]=10033
        self.subhourlyId[696]=10033
        self.subhourlyId[697]=10033
        self.subhourlyId[698]=10033
        self.subhourlyId[699]=10033
        self.subhourlyId[700]=10033
        self.subhourlyId[701]=10033
        self.subhourlyId[702]=10033
        
        self.subhourlyId[703]=10034
        self.subhourlyId[704]=10034
        self.subhourlyId[705]=10034
        self.subhourlyId[706]=10034
        self.subhourlyId[707]=10034
        self.subhourlyId[708]=10034
        self.subhourlyId[709]=10034
        self.subhourlyId[710]=10034
        self.subhourlyId[711]=10034
        self.subhourlyId[712]=10034
        self.subhourlyId[713]=10034
        self.subhourlyId[714]=10034
        
        self.subhourlyId[715]=10035
        self.subhourlyId[716]=10035
        self.subhourlyId[717]=10035
        self.subhourlyId[718]=10035
        self.subhourlyId[719]=10035
        self.subhourlyId[720]=10035
        self.subhourlyId[721]=10035
        self.subhourlyId[722]=10035
        self.subhourlyId[723]=10035
        self.subhourlyId[724]=10035
        self.subhourlyId[725]=10035
        self.subhourlyId[726]=10035
        
        self.subhourlyId[727]=10036
        self.subhourlyId[728]=10036
        self.subhourlyId[729]=10036
        self.subhourlyId[730]=10036
        self.subhourlyId[731]=10036
        self.subhourlyId[732]=10036
        self.subhourlyId[733]=10036
        self.subhourlyId[734]=10036
        self.subhourlyId[735]=10036
        self.subhourlyId[736]=10036
        self.subhourlyId[737]=10036
        self.subhourlyId[738]=10036
        
        self.subhourlyId[739]=10037
        self.subhourlyId[740]=10037
        self.subhourlyId[741]=10037
        self.subhourlyId[742]=10037
        self.subhourlyId[743]=10037
        self.subhourlyId[744]=10037
        self.subhourlyId[745]=10037
        self.subhourlyId[746]=10037
        self.subhourlyId[747]=10037
        self.subhourlyId[748]=10037
        self.subhourlyId[749]=10037
        self.subhourlyId[750]=10037
        
        self.subhourlyId[751]=10038
        self.subhourlyId[752]=10038
        self.subhourlyId[753]=10038
        self.subhourlyId[754]=10038
        self.subhourlyId[755]=10038
        self.subhourlyId[756]=10038
        self.subhourlyId[757]=10038
        self.subhourlyId[758]=10038
        self.subhourlyId[759]=10038
        self.subhourlyId[760]=10038
        self.subhourlyId[761]=10038
        self.subhourlyId[762]=10038
        
    def populateTimes(self):
        self.subhourlyTime[437]="60"
        self.subhourlyTime[436]="55"
        self.subhourlyTime[435]="50"
        self.subhourlyTime[434]="45"
        self.subhourlyTime[433]="40"
        self.subhourlyTime[432]="35"
        self.subhourlyTime[431]="30"
        self.subhourlyTime[430]="25"
        self.subhourlyTime[429]="20"
        self.subhourlyTime[428]="15"
        self.subhourlyTime[427]="10"
        self.subhourlyTime[426]="05"
        self.subhourlyTime[422]="60"
        self.subhourlyTime[421]="55"
        self.subhourlyTime[420]="50"
        self.subhourlyTime[419]="45"
        self.subhourlyTime[418]="40"
        self.subhourlyTime[417]="35"
        self.subhourlyTime[416]="30"
        self.subhourlyTime[415]="25"
        self.subhourlyTime[414]="20"
        self.subhourlyTime[413]="15"
        self.subhourlyTime[412]="10"
        self.subhourlyTime[411]="05"
        self.subhourlyTime[348]="60"
        self.subhourlyTime[349]="55"
        self.subhourlyTime[350]="50"
        self.subhourlyTime[351]="45"
        self.subhourlyTime[352]="40"
        self.subhourlyTime[353]="35"
        self.subhourlyTime[354]="30"
        self.subhourlyTime[355]="25"
        self.subhourlyTime[356]="20"
        self.subhourlyTime[357]="15"
        self.subhourlyTime[358]="10"
        self.subhourlyTime[359]="05"
        self.subhourlyTime[360]="60"
        self.subhourlyTime[361]="55"
        self.subhourlyTime[362]="50"
        self.subhourlyTime[363]="45"
        self.subhourlyTime[364]="40"
        self.subhourlyTime[365]="35"
        self.subhourlyTime[366]="30"
        self.subhourlyTime[367]="25"
        self.subhourlyTime[368]="20"
        self.subhourlyTime[369]="15"
        self.subhourlyTime[370]="10"
        self.subhourlyTime[371]="05"
        self.subhourlyTime[372]="60"
        self.subhourlyTime[373]="55"
        self.subhourlyTime[374]="50"
        self.subhourlyTime[375]="45"
        self.subhourlyTime[376]="40"
        self.subhourlyTime[377]="35"
        self.subhourlyTime[378]="30"
        self.subhourlyTime[379]="25"
        self.subhourlyTime[380]="20"
        self.subhourlyTime[381]="15"
        self.subhourlyTime[382]="10"
        self.subhourlyTime[383]="05"
        self.subhourlyTime[384]="60"
        self.subhourlyTime[385]="55"
        self.subhourlyTime[386]="50"
        self.subhourlyTime[387]="45"
        self.subhourlyTime[388]="40"
        self.subhourlyTime[389]="35"
        self.subhourlyTime[390]="30"
        self.subhourlyTime[391]="25"
        self.subhourlyTime[392]="20"
        self.subhourlyTime[393]="15"
        self.subhourlyTime[394]="10"
        self.subhourlyTime[395]="05"
        self.subhourlyTime[396]="60"
        self.subhourlyTime[397]="55"
        self.subhourlyTime[398]="50"
        self.subhourlyTime[399]="45"
        self.subhourlyTime[400]="40"
        self.subhourlyTime[401]="35"
        self.subhourlyTime[402]="30"
        self.subhourlyTime[403]="25"
        self.subhourlyTime[404]="20"
        self.subhourlyTime[405]="15"
        self.subhourlyTime[406]="10"
        self.subhourlyTime[407]="05"
        self.subhourlyTime[348]="60"
        self.subhourlyTime[349]="55"
        self.subhourlyTime[350]="50"
        self.subhourlyTime[351]="45"
        self.subhourlyTime[352]="40"
        self.subhourlyTime[353]="35"
        self.subhourlyTime[354]="30"
        self.subhourlyTime[355]="25"
        self.subhourlyTime[356]="20"
        self.subhourlyTime[357]="15"
        self.subhourlyTime[358]="10"
        self.subhourlyTime[359]="05"
        self.subhourlyTime[342]="60"
        self.subhourlyTime[341]="55"
        self.subhourlyTime[340]="50"
        self.subhourlyTime[339]="45"
        self.subhourlyTime[338]="40"
        self.subhourlyTime[337]="35"
        self.subhourlyTime[336]="30"
        self.subhourlyTime[335]="25"
        self.subhourlyTime[334]="20"
        self.subhourlyTime[333]="15"
        self.subhourlyTime[332]="10"
        self.subhourlyTime[331]="05"
        self.subhourlyTime[330]="60"
        self.subhourlyTime[329]="55"
        self.subhourlyTime[328]="50"
        self.subhourlyTime[327]="45"
        self.subhourlyTime[326]="40"
        self.subhourlyTime[325]="35"
        self.subhourlyTime[324]="30"
        self.subhourlyTime[323]="25"
        self.subhourlyTime[322]="20"
        self.subhourlyTime[321]="15"
        self.subhourlyTime[320]="10"
        self.subhourlyTime[319]="05"
        self.subhourlyTime[317]="60"
        self.subhourlyTime[316]="45"
        self.subhourlyTime[315]="30"
        self.subhourlyTime[314]="15"
        self.subhourlyTime[194]="60"
        self.subhourlyTime[185]="55"
        self.subhourlyTime[176]="50"
        self.subhourlyTime[167]="45"
        self.subhourlyTime[158]="40"
        self.subhourlyTime[149]="35"
        self.subhourlyTime[140]="30"
        self.subhourlyTime[131]="25"
        self.subhourlyTime[122]="20"
        self.subhourlyTime[113]="15"
        self.subhourlyTime[104]="10"
        self.subhourlyTime[95]="05"
        self.subhourlyTime[193]="60"
        self.subhourlyTime[184]="55"
        self.subhourlyTime[175]="50"
        self.subhourlyTime[166]="45"
        self.subhourlyTime[157]="40"
        self.subhourlyTime[148]="35"
        self.subhourlyTime[139]="30"
        self.subhourlyTime[130]="25"
        self.subhourlyTime[121]="20"
        self.subhourlyTime[112]="15"
        self.subhourlyTime[103]="10"
        self.subhourlyTime[94]="05"
        self.subhourlyTime[192]="60"
        self.subhourlyTime[183]="55"
        self.subhourlyTime[174]="50"
        self.subhourlyTime[165]="45"
        self.subhourlyTime[156]="40"
        self.subhourlyTime[147]="35"
        self.subhourlyTime[138]="30"
        self.subhourlyTime[129]="25"
        self.subhourlyTime[120]="20"
        self.subhourlyTime[111]="15"
        self.subhourlyTime[102]="10"
        self.subhourlyTime[93]="05"
        self.subhourlyTime[191]="60"
        self.subhourlyTime[182]="55"
        self.subhourlyTime[173]="50"
        self.subhourlyTime[164]="45"
        self.subhourlyTime[155]="40"
        self.subhourlyTime[146]="35"
        self.subhourlyTime[137]="30"
        self.subhourlyTime[128]="25"
        self.subhourlyTime[119]="20"
        self.subhourlyTime[110]="15"
        self.subhourlyTime[101]="10"
        self.subhourlyTime[92]="05"
        self.subhourlyTime[190]="60"
        self.subhourlyTime[181]="55"
        self.subhourlyTime[172]="50"
        self.subhourlyTime[163]="45"
        self.subhourlyTime[154]="40"
        self.subhourlyTime[145]="35"
        self.subhourlyTime[136]="30"
        self.subhourlyTime[127]="25"
        self.subhourlyTime[118]="20"
        self.subhourlyTime[109]="15"
        self.subhourlyTime[100]="10"
        self.subhourlyTime[91]="05"
        self.subhourlyTime[189]="60"
        self.subhourlyTime[180]="55"
        self.subhourlyTime[171]="50"
        self.subhourlyTime[162]="45"
        self.subhourlyTime[153]="40"
        self.subhourlyTime[144]="35"
        self.subhourlyTime[135]="30"
        self.subhourlyTime[126]="25"
        self.subhourlyTime[117]="20"
        self.subhourlyTime[108]="15"
        self.subhourlyTime[99]="10"
        self.subhourlyTime[90]="05"
        self.subhourlyTime[188]="60"
        self.subhourlyTime[179]="55"
        self.subhourlyTime[170]="50"
        self.subhourlyTime[161]="45"
        self.subhourlyTime[152]="40"
        self.subhourlyTime[143]="35"
        self.subhourlyTime[134]="30"
        self.subhourlyTime[125]="25"
        self.subhourlyTime[116]="20"
        self.subhourlyTime[107]="15"
        self.subhourlyTime[98]="10"
        self.subhourlyTime[89]="05"
        self.subhourlyTime[187]="60"
        self.subhourlyTime[178]="55"
        self.subhourlyTime[169]="50"
        self.subhourlyTime[160]="45"
        self.subhourlyTime[151]="40"
        self.subhourlyTime[142]="35"
        self.subhourlyTime[133]="30"
        self.subhourlyTime[124]="25"
        self.subhourlyTime[115]="20"
        self.subhourlyTime[106]="15"
        self.subhourlyTime[97]="10"
        self.subhourlyTime[88]="05"
        self.subhourlyTime[186]="60"
        self.subhourlyTime[177]="55"
        self.subhourlyTime[168]="50"
        self.subhourlyTime[159]="45"
        self.subhourlyTime[150]="40"
        self.subhourlyTime[141]="35"
        self.subhourlyTime[132]="30"
        self.subhourlyTime[123]="25"
        self.subhourlyTime[114]="20"
        self.subhourlyTime[105]="15"
        self.subhourlyTime[96]="10"
        self.subhourlyTime[87]="05"
        self.subhourlyTime[56]="60"
        self.subhourlyTime[55]="45"
        self.subhourlyTime[54]="30"
        self.subhourlyTime[53]="15"
        self.subhourlyTime[77]="60"
        self.subhourlyTime[76]="45"
        self.subhourlyTime[75]="30"
        self.subhourlyTime[74]="15"
        self.subhourlyTime[65]="60"
        self.subhourlyTime[64]="45"
        self.subhourlyTime[63]="30"
        self.subhourlyTime[62]="15"
        self.subhourlyTime[33]="60"
        self.subhourlyTime[32]="45"
        self.subhourlyTime[31]="30"
        self.subhourlyTime[30]="15"
        self.subhourlyTime[571]="05"
        self.subhourlyTime[572]="10"
        self.subhourlyTime[573]="15"
        self.subhourlyTime[574]="20"
        self.subhourlyTime[575]="25"
        self.subhourlyTime[576]="30"
        self.subhourlyTime[577]="35"
        self.subhourlyTime[578]="40"
        self.subhourlyTime[579]="45"
        self.subhourlyTime[580]="50"
        self.subhourlyTime[581]="55"
        self.subhourlyTime[582]="60"
        self.subhourlyTime[583]="05"
        self.subhourlyTime[584]="10"
        self.subhourlyTime[585]="15"
        self.subhourlyTime[586]="20"
        self.subhourlyTime[587]="25"
        self.subhourlyTime[588]="30"
        self.subhourlyTime[589]="35"
        self.subhourlyTime[590]="40"
        self.subhourlyTime[591]="45"
        self.subhourlyTime[592]="50"
        self.subhourlyTime[593]="55"
        self.subhourlyTime[594]="60"
        self.subhourlyTime[595]="05"
        self.subhourlyTime[596]="10"
        self.subhourlyTime[597]="15"
        self.subhourlyTime[598]="20"
        self.subhourlyTime[599]="25"
        self.subhourlyTime[600]="30"
        self.subhourlyTime[601]="35"
        self.subhourlyTime[602]="40"
        self.subhourlyTime[603]="45"
        self.subhourlyTime[604]="50"
        self.subhourlyTime[605]="55"
        self.subhourlyTime[606]="60"
        self.subhourlyTime[607]="05"
        self.subhourlyTime[608]="10"
        self.subhourlyTime[609]="15"
        self.subhourlyTime[610]="20"
        self.subhourlyTime[611]="25"
        self.subhourlyTime[612]="30"
        self.subhourlyTime[613]="35"
        self.subhourlyTime[614]="40"
        self.subhourlyTime[615]="45"
        self.subhourlyTime[616]="50"
        self.subhourlyTime[617]="55"
        self.subhourlyTime[618]="60"
        self.subhourlyTime[619]="05"
        self.subhourlyTime[620]="10"
        self.subhourlyTime[621]="15"
        self.subhourlyTime[622]="20"
        self.subhourlyTime[623]="25"
        self.subhourlyTime[624]="30"
        self.subhourlyTime[625]="35"
        self.subhourlyTime[626]="40"
        self.subhourlyTime[627]="45"
        self.subhourlyTime[628]="50"
        self.subhourlyTime[629]="55"
        self.subhourlyTime[630]="60"
        self.subhourlyTime[631]="05"
        self.subhourlyTime[643]="05"
        self.subhourlyTime[655]="05"
        self.subhourlyTime[632]="10"
        self.subhourlyTime[644]="10"
        self.subhourlyTime[656]="10"
        self.subhourlyTime[633]="15"
        self.subhourlyTime[645]="15"
        self.subhourlyTime[657]="15"
        self.subhourlyTime[634]="20"
        self.subhourlyTime[646]="20"
        self.subhourlyTime[658]="20"
        self.subhourlyTime[635]="25"
        self.subhourlyTime[647]="25"
        self.subhourlyTime[659]="25"
        self.subhourlyTime[636]="30"
        self.subhourlyTime[648]="30"
        self.subhourlyTime[660]="30"
        self.subhourlyTime[637]="35"
        self.subhourlyTime[649]="35"
        self.subhourlyTime[661]="35"
        self.subhourlyTime[638]="40"
        self.subhourlyTime[650]="40"
        self.subhourlyTime[662]="40"
        self.subhourlyTime[639]="45"
        self.subhourlyTime[651]="45"
        self.subhourlyTime[663]="45"
        self.subhourlyTime[640]="50"
        self.subhourlyTime[652]="50"
        self.subhourlyTime[664]="50"
        self.subhourlyTime[641]="55"
        self.subhourlyTime[653]="55"
        self.subhourlyTime[665]="55"
        self.subhourlyTime[642]="60"
        self.subhourlyTime[654]="60"
        self.subhourlyTime[666]="60"
        self.subhourlyTime[667]="05"
        self.subhourlyTime[679]="05"
        self.subhourlyTime[691]="05"
        self.subhourlyTime[668]="10"
        self.subhourlyTime[680]="10"
        self.subhourlyTime[692]="10"
        self.subhourlyTime[669]="15"
        self.subhourlyTime[681]="15"
        self.subhourlyTime[693]="15"
        self.subhourlyTime[670]="20"
        self.subhourlyTime[682]="20"
        self.subhourlyTime[694]="20"
        self.subhourlyTime[671]="25"
        self.subhourlyTime[683]="25"
        self.subhourlyTime[695]="25"
        self.subhourlyTime[672]="30"
        self.subhourlyTime[684]="30"
        self.subhourlyTime[696]="30"
        self.subhourlyTime[673]="35"
        self.subhourlyTime[685]="35"
        self.subhourlyTime[697]="35"
        self.subhourlyTime[674]="40"
        self.subhourlyTime[686]="40"
        self.subhourlyTime[698]="40"
        self.subhourlyTime[675]="45"
        self.subhourlyTime[687]="45"
        self.subhourlyTime[699]="45"
        self.subhourlyTime[676]="50"
        self.subhourlyTime[688]="50"
        self.subhourlyTime[700]="50"
        self.subhourlyTime[677]="55"
        self.subhourlyTime[689]="55"
        self.subhourlyTime[701]="55"
        self.subhourlyTime[678]="60"
        self.subhourlyTime[690]="60"
        self.subhourlyTime[702]="60"
        self.subhourlyTime[703]="05"
        self.subhourlyTime[704]="10"
        self.subhourlyTime[705]="15"
        self.subhourlyTime[706]="20"
        self.subhourlyTime[707]="25"
        self.subhourlyTime[708]="30"
        self.subhourlyTime[709]="35"
        self.subhourlyTime[710]="40"
        self.subhourlyTime[711]="45"
        self.subhourlyTime[712]="50"
        self.subhourlyTime[713]="55"
        self.subhourlyTime[714]="60"
        self.subhourlyTime[715]="05"
        self.subhourlyTime[727]="05"
        self.subhourlyTime[739]="05"
        self.subhourlyTime[716]="10"
        self.subhourlyTime[728]="10"
        self.subhourlyTime[740]="10"
        self.subhourlyTime[717]="15"
        self.subhourlyTime[729]="15"
        self.subhourlyTime[741]="15"
        self.subhourlyTime[718]="20"
        self.subhourlyTime[730]="20"
        self.subhourlyTime[742]="20"
        self.subhourlyTime[719]="25"
        self.subhourlyTime[731]="25"
        self.subhourlyTime[743]="25"
        self.subhourlyTime[720]="30"
        self.subhourlyTime[732]="30"
        self.subhourlyTime[744]="30"
        self.subhourlyTime[721]="35"
        self.subhourlyTime[733]="35"
        self.subhourlyTime[745]="35"
        self.subhourlyTime[722]="40"
        self.subhourlyTime[734]="40"
        self.subhourlyTime[746]="40"
        self.subhourlyTime[723]="45"
        self.subhourlyTime[735]="45"
        self.subhourlyTime[747]="45"
        self.subhourlyTime[724]="50"
        self.subhourlyTime[736]="50"
        self.subhourlyTime[748]="50"
        self.subhourlyTime[725]="55"
        self.subhourlyTime[737]="55"
        self.subhourlyTime[749]="55"
        self.subhourlyTime[726]="60"
        self.subhourlyTime[738]="60"
        self.subhourlyTime[750]="60"
        self.subhourlyTime[751]="05"
        self.subhourlyTime[752]="10"
        self.subhourlyTime[753]="15"
        self.subhourlyTime[754]="20"
        self.subhourlyTime[755]="25"
        self.subhourlyTime[756]="30"
        self.subhourlyTime[757]="35"
        self.subhourlyTime[758]="40"
        self.subhourlyTime[759]="45"
        self.subhourlyTime[760]="50"
        self.subhourlyTime[761]="55"
        self.subhourlyTime[762]="60"

    def populateNames(self):
        self.subhourlyName[10000]="P15"
        self.subhourlyName[10001]="P5"
        self.subhourlyName[10002]="T5"
        self.subhourlyName[10003]="FM_PCN"
        self.subhourlyName[10004]="PCP_2"
        self.subhourlyName[10005]="PCP_3"
        self.subhourlyName[10006]="FM2_PCN"
        self.subhourlyName[10007]="T1"
        self.subhourlyName[10008]="T2"
        self.subhourlyName[10009]="T3"
        self.subhourlyName[10010]="D1"
        self.subhourlyName[10011]="D2"
        self.subhourlyName[10012]="D3"
        self.subhourlyName[10013]="TB"
        self.subhourlyName[10014]="WET1"
        self.subhourlyName[10015]="WET2"
        self.subhourlyName[10016]="WSPD"
        self.subhourlyName[10017]="WDMAX"
        self.subhourlyName[10018]="WMAX"
        self.subhourlyName[10019]="WDSTD"
        self.subhourlyName[10020]="WDIR"
        self.subhourlyName[10016]="WSPD"
        self.subhourlyName[10021]="TRH"
        self.subhourlyName[10022]="RH"
        self.subhourlyName[10023]="STR_SUB"
        self.subhourlyName[10024]="STC_SUB"
        self.subhourlyName[10025]="STSB_SUB"
        self.subhourlyName[10026]="WIND_SUB"
        self.subhourlyName[10027]="SOLRAD_SUB"
        self.subhourlyName[10028]="SM1005_SUB"
        self.subhourlyName[10029]="SM2005_SUB"
        self.subhourlyName[10030]="SM3005_SUB"
        self.subhourlyName[10031]="ST1005_SUB"
        self.subhourlyName[10032]="ST2005_SUB"
        self.subhourlyName[10033]="ST3005_SUB"
        self.subhourlyName[10034]="ST005_SUB"
        self.subhourlyName[10035]="SMV1005_SUB"
        self.subhourlyName[10036]="SMV2005_SUB"
        self.subhourlyName[10037]="SMV3005_SUB"
        self.subhourlyName[10038]="SMV005_SUB"

    def populateDescriptions(self):
        self.subhourlyDescription[10003]="Geonor wire 1 precip amount for 15 minutes (artificial crnscript element for group)"
        self.subhourlyDescription[10004]="Geonor wire 2 precip amount for 15 minutes (artificial crnscript element for group)"
        self.subhourlyDescription[10005]="Geonor wire 3 precip amount for 15 minutes (artificial crnscript element for group)"
        self.subhourlyDescription[10006]="tipping bucket precip amount for 15 minutes (artificial crnscript element for group)"
        self.subhourlyDescription[10007]="temp sensor 1 average temp for 5 minutes (artificial crnscript element for group)"
        self.subhourlyDescription[10008]="temp sensor 2 average temp for 5 minutes (artificial crnscript element for group)"
        self.subhourlyDescription[10009]="temp sensor 3 average temp for 5 minutes (artificial crnscript element for group)"
        self.subhourlyDescription[10010]="Geonor wire 1 depth for 5 minutes (artificial crnscript element for group)"
        self.subhourlyDescription[10011]="Geonor wire 2 depth for 5 minutes (artificial crnscript element for group)"
        self.subhourlyDescription[10012]="Geonor wire 3 depth for 5 minutes (artificial crnscript element for group)"
        self.subhourlyDescription[10013]="tipping bucket precip amount for 5 minutes (artificial crnscript element for group)"
        self.subhourlyDescription[10014]="wetness sensor channel 1 minimum for 5 minutes (artificial crnscript element for group)"
        self.subhourlyDescription[10015]="wetness sensor channel 2 minimum for 5 minutes (artificial crnscript element for group)"
        self.subhourlyDescription[10000]="calculated Geonor precip for 15 minutes (artificial crnscript element for group)"
        self.subhourlyDescription[10001]="calculated Geonor precip for 5 minutes (artificial crnscript element for group)"
        self.subhourlyDescription[10002]="calculated average temp for 5 minutes (artificial crnscript element for group)"
        self.subhourlyDescription[10016]="average wind speed for 5 minutes (artificial crnscript element for group)"
        self.subhourlyDescription[10017]="direction assoc with peak wind speed for 5 minutes (artificial crnscript element for group)"
        self.subhourlyDescription[10018]="peak wind speed for 5 minutes (artificial crnscript element for group)"
        self.subhourlyDescription[10019]="operational wind direction std dev (degrees) for 5 minutes (artificial crnscript element for group)"
        self.subhourlyDescription[10020]="operational wind direction (degrees) for 5 minutes (artificial crnscript element for group)"
        self.subhourlyDescription[10016]="average wind speed for 5 minutes (artificial crnscript element for group)"
        self.subhourlyDescription[10021]="Temp at RH sensor average for 5 minutes (artificial crnscript element for group)"
        self.subhourlyDescription[10022]="RH percent average for 5 minutes (artificial crnscript element for group)"
        self.subhourlyDescription[10023]="average raw ir surface temp (Celsius) (artificial crnscript element for group)"
        self.subhourlyDescription[10024]="average calibrated ir surface temp (Celsius) (artificial crnscript element for group)"
        self.subhourlyDescription[10025]="average ir surface temp sensor body temp (Celsius) (artificial crnscript element for group)"
        self.subhourlyDescription[10026]="average 1.5 meter wind speed (m/s) (artificial crnscript element for group)"
        self.subhourlyDescription[10027]="average solar radiation (W/m^2) (artificial crnscript element for group)"
        self.subhourlyDescription[10028]="average soil moisture dielectric for set 1 at 5 cm (artificial crnscript element for group)"
        self.subhourlyDescription[10029]="average soil moisture dielectric for set 2 at 5 cm (artificial crnscript element for group)"
        self.subhourlyDescription[10030]="average soil moisture dielectric for set 3 at 5 cm (artificial crnscript element for group)"
        self.subhourlyDescription[10031]="average soil temperature (Celsius) for set 1 at 5 cm (artificial crnscript element for group)"
        self.subhourlyDescription[10032]="average soil temperature (Celsius) for set 2 at 5 cm (artificial crnscript element for group)"
        self.subhourlyDescription[10033]="average soil temperature (Celsius) for set 3 at 5 cm (artificial crnscript element for group)"
        self.subhourlyDescription[10034]="soil temperature layer average (Celsius) at 5 cm (artificial crnscript element for group)"
        self.subhourlyDescription[10035]="soil moisture volumetric (fraction) for set 1 at 5 cm average (artificial crnscript element for group)"
        self.subhourlyDescription[10036]="soil moisture volumetric (fraction) for set 2 at 5 cm average (artificial crnscript element for group)"
        self.subhourlyDescription[10037]="soil moisture volumetric (fraction) for set 3 at 5 cm average (artificial crnscript element for group)"
        self.subhourlyDescription[10038]="soil moisture volumetric layer average (fraction) at 5 cm (artificial crnscript element for group)"

        
def __doctests():
    ''' These doctests are automatically run if you run the module. You should get no output unless there's a 
    problem.
    
    >>> m = ElementSubhourlyGroupManager.getManager()

    >>> m.getTime(314)
    '15'
    >>> m.getId(314)
    10000
    >>> m.generateElement(10000)
    Element 10000:P15:calculated Geonor precip for 15 minutes (artificial crnscript element for group)
    >>> m.getDescriptionFromId(314)
    'calculated Geonor precip for 15 minutes (artificial crnscript element for group)'
    >>> m.getDescriptionFromId(10000)
    'calculated Geonor precip for 15 minutes (artificial crnscript element for group)'
    >>> m.getNameFromId(314)
    'P15'
    >>> m.getNameFromId(10000)
    'P15'
    >>> 10005 in m.getAllIds()
    True
    >>> 314 in m.getAllIds()
    False
    '''
if __name__ == "__main__":
    import doctest #@UnresolvedImport
    doctest.testmod()
