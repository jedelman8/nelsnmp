from pysnmp.entity.rfc3413.oneliner import cmdgen

SNMP_VERSIONS = ('2c', '3')


class ArgumentError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)    

class SnmpHandler(object):
    

    def __init__(self, **kwargs):

        self.port = 161
        self.version = False
        self.community = False
        self.host = False


        for key in kwargs:
            if key == 'version' and kwargs[key] in SNMP_VERSIONS:   
                self.version = kwargs[key]
            if key == 'community':
                self.community = kwargs[key]
            if key == 'host':
                self.host = kwargs[key]

        if self.version not in SNMP_VERSIONS:
            raise ArgumentError('No valid SNMP version defined')

        if self.version == False or self.host == False:
            print "You have to set version and host"
        if self.version == "2c":
            self.snmp_auth = cmdgen.CommunityData(self.community)

    def get(self, *oidlist):

        snmp_query = []
        for oid in oidlist:
            snmp_query.append(cmdgen.MibVariable(oid,), )

        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            self.snmp_auth,
            cmdgen.UdpTransportTarget((self.host, self.port)),
            *snmp_query
        )

        if errorIndication or errorStatus:
            # Fix error handling
            pass

        return varBinds


    def getnext(self, *oidlist):

        snmp_query = []
        for oid in oidlist:
            snmp_query.append(cmdgen.MibVariable(oid,), )

        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varTable = cmdGen.nextCmd(
            self.snmp_auth,
            cmdgen.UdpTransportTarget((self.host, self.port)),
            *snmp_query
        )

        if errorIndication or errorStatus:
            # Fix error handling
            pass

        return varTable

    def set(self, *snmp_sets):

        cmdGen = cmdgen.CommandGenerator()
        errorIndication, errorStatus, errorIndex, varTable = cmdGen.setCmd(
            self.snmp_auth,
            cmdgen.UdpTransportTarget((self.host, self.port)),
            *snmp_sets
        )

        if errorIndication or errorStatus:
            # Fix error handling
            pass
