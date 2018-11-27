import idautils
import idaapi
import idc
import json

from guids import edk_guids, ami_guids, edk2_guids

OFFSET = {
    "InstallProtocolInterface": 0x80,
    "ReinstallProtocolInterface": 0x88,
    "UninstallProtocolInterface": 0x90,
    "HandleProtocol": 0x98,
    "RegisterProtocolNotify": 0xA8,
    "OpenProtocol": 0x118,
    "CloseProtocol": 0x120,
    "OpenProtocolInformation": 0x128,
    "ProtocolsPerHandle": 0x130,
    "LocateHandleBuffer": 0x138,
    "LocateProtocol": 0x140,
    "InstallMultipleProtocolInterfaces": 0x148,
    "UninstallMultipleProtocolInterfaces": 0x150,
}

LEA_NUM = {
    "InstallProtocolInterface": 2,
    "ReinstallProtocolInterface": 1,
    "UninstallProtocolInterface": 1,
    "HandleProtocol": 1,
    "RegisterProtocolNotify": 1,
    "OpenProtocol": 1,
    "CloseProtocol": 1,
    "OpenProtocolInformation": 1,
    "LocateHandleBuffer": 2,
    "LocateProtocol": 1,
#   "InstallMultipleProtocolInterfaces": 2,
#   "UninstallMultipleProtocolInterfaces": x,
}

def SetHexRaysComment(address, text):
    cfunc = idaapi.decompile(address)
    tl = idaapi.treeloc_t()
    tl.ea = address
    tl.itp = idaapi.ITP_SEMI
    cfunc.set_user_cmt(tl, text)
    cfunc.save_user_cmts()

def get_guid(address):
    CurrentGUID = []
    CurrentGUID.append(idc.Dword(address))
    CurrentGUID.append(idc.Word(address + 4))
    CurrentGUID.append(idc.Word(address + 6))
    for addr in range(address + 8, address + 16, 1):
        CurrentGUID.append(idc.Byte(addr))
    return CurrentGUID

class Analyser(object):
    def __init__(self):
        idc.Til2Idb(-1, "EFI_GUID")
        idc.Til2Idb(-1, "EFI_SYSTEM_TABLE")
        idc.Til2Idb(-1, "EFI_RUNTIME_SERVICES")
        idc.Til2Idb(-1, "EFI_BOOT_SERVICES")


        self.gBServices = {}
        self.gBServices["InstallProtocolInterface"] = []
        self.gBServices["ReinstallProtocolInterface"] = []
        self.gBServices["UninstallProtocolInterface"] = []
        self.gBServices["HandleProtocol"] = []
        self.gBServices["RegisterProtocolNotify"] = []
        self.gBServices["OpenProtocol"] = []
        self.gBServices["CloseProtocol"] = []
        self.gBServices["OpenProtocolInformation"] = []
        self.gBServices["ProtocolsPerHandle"] = []
        self.gBServices["LocateHandleBuffer"] = []
        self.gBServices["LocateProtocol"] = []
        self.gBServices["InstallMultipleProtocolInterfaces"] = []
        self.gBServices["UninstallMultipleProtocolInterfaces"] = []

        self.Protocols = {}
        self.Protocols["AmiGuids"] = ami_guids.ami_guids
        self.Protocols["EdkGuids"] = edk_guids.edk_guids
        self.Protocols["Edk2Guids"] = edk2_guids.edk2_guids
        self.Protocols["All"] = [
            # {
            #   address: ...
            #   service: ...
            #   guid: ...
            # }, 
            # ...
        ]
        self.Protocols["PropGuids"] = []

    @staticmethod
    def help():
        print("Methods:")
        print(" * analyser.get_boot_services()")
        print("   - check: analyser.gBServices[<service_name>]")
        print(" * analyser.list_boot_services()")
        print(" * analyser.make_comments()")
        print(" * analyser.get_protocols()")
        print("   - check: analyser.Protocols['All']")
        print(" * analyser.get_prot_names()")
        print("   - check: analyser.Protocols['All']")
        print(" * analyser.print_all()")

    def get_boot_services(self):
        for ea_start in idautils.Functions():
            for ea in idautils.FuncItems(ea_start):
                if (idc.GetMnem(ea) == "call") and (idc.get_operand_value(ea, 0) == OFFSET["InstallProtocolInterface"]):
                    if self.gBServices["InstallProtocolInterface"].count(ea) == 0:
                        self.gBServices["InstallProtocolInterface"].append(ea)
                if (idc.GetMnem(ea) == "call") and (idc.get_operand_value(ea, 0) == OFFSET["ReinstallProtocolInterface"]):
                    if self.gBServices["ReinstallProtocolInterface"].count(ea) == 0:
                        self.gBServices["ReinstallProtocolInterface"].append(ea)
                if (idc.GetMnem(ea) == "call") and (idc.get_operand_value(ea, 0) == OFFSET["UninstallProtocolInterface"]):
                    if self.gBServices["UninstallProtocolInterface"].count(ea) == 0:
                        self.gBServices["UninstallProtocolInterface"].append(ea)
                if (idc.GetMnem(ea) == "call") and (idc.get_operand_value(ea, 0) == OFFSET["HandleProtocol"]):
                    if self.gBServices["HandleProtocol"].count(ea) == 0:
                        self.gBServices["HandleProtocol"].append(ea)
                if (idc.GetMnem(ea) == "call") and (idc.get_operand_value(ea, 0) == OFFSET["RegisterProtocolNotify"]):
                    if self.gBServices["RegisterProtocolNotify"].count(ea) == 0:
                        self.gBServices["RegisterProtocolNotify"].append(ea)
                if (idc.GetMnem(ea) == "call") and (idc.get_operand_value(ea, 0) == OFFSET["OpenProtocol"]):
                    if self.gBServices["OpenProtocol"].count(ea) == 0:
                        self.gBServices["OpenProtocol"].append(ea)
                if (idc.GetMnem(ea) == "call") and (idc.get_operand_value(ea, 0) == OFFSET["CloseProtocol"]):
                    if self.gBServices["CloseProtocol"].count(ea) == 0:
                        self.gBServices["CloseProtocol"].append(ea)
                if (idc.GetMnem(ea) == "call") and (idc.get_operand_value(ea, 0) == OFFSET["OpenProtocolInformation"]):
                    if self.gBServices["OpenProtocolInformation"].count(ea) == 0:
                        self.gBServices["OpenProtocolInformation"].append(ea)
                if (idc.GetMnem(ea) == "call") and (idc.get_operand_value(ea, 0) == OFFSET["ProtocolsPerHandle"]):
                    if self.gBServices["ProtocolsPerHandle"].count(ea) == 0:
                        self.gBServices["ProtocolsPerHandle"].append(ea)
                if (idc.GetMnem(ea) == "call") and (idc.get_operand_value(ea, 0) == OFFSET["LocateHandleBuffer"]):
                    if self.gBServices["LocateHandleBuffer"].count(ea) == 0:
                        self.gBServices["LocateHandleBuffer"].append(ea)
                if (idc.GetMnem(ea) == "call") and (idc.get_operand_value(ea, 0) == OFFSET["LocateProtocol"]):
                    if self.gBServices["LocateProtocol"].count(ea) == 0:
                        self.gBServices["LocateProtocol"].append(ea)
                if (idc.GetMnem(ea) == "call") and (idc.get_operand_value(ea, 0) == OFFSET["InstallMultipleProtocolInterfaces"]):
                    if self.gBServices["InstallMultipleProtocolInterfaces"].count(ea) == 0:
                        self.gBServices["InstallMultipleProtocolInterfaces"].append(ea)
                if (idc.GetMnem(ea) == "call") and (idc.get_operand_value(ea, 0) == OFFSET["UninstallMultipleProtocolInterfaces"]):
                    if self.gBServices["UninstallMultipleProtocolInterfaces"].count(ea) == 0:
                        self.gBServices["UninstallMultipleProtocolInterfaces"].append(ea)
    
    def list_boot_services(self):
        for service in self.gBServices:
            for address in self.gBServices[service]:
                print("\t [{0}] EFI_BOOT_SERVICES->{1}".format(hex(address), service))

    def make_comments(self):
        for service in self.gBServices:
            for address in self.gBServices[service]:
                SetHexRaysComment(address, "EFI_BOOT_SERVICES->{0}".format(service))
                idc.MakeComm(address, "EFI_BOOT_SERVICES->{0}".format(service))

    def get_protocols(self):
        for service_name in self.gBServices:
            if service_name in LEA_NUM.keys():
                for address in self.gBServices[service_name]:
                    ea = address
                    lea_counter = 0
                    while (True):
                        ea = idc.prev_head(ea)
                        if (idc.GetMnem(ea) == "lea"):
                            lea_counter += 1
                            if (lea_counter == LEA_NUM[service_name]):
                                break
                    for xref in idautils.DataRefsFrom(ea):
                        if (idc.GetMnem(xref) == ""):
                            CurrentGUID = get_guid(xref)
                            protocol_record = {}
                            protocol_record["address"] = xref
                            protocol_record["service"] = service_name
                            protocol_record["guid"] = CurrentGUID
                            if self.Protocols["All"].count(protocol_record) == 0:
                                self.Protocols["All"].append(protocol_record)

    def get_prot_names(self):
        for index in range(len(self.Protocols["All"])):
            fin = False
            for prot_name in self.Protocols["Edk2Guids"].keys():
                guid_idb = self.Protocols["All"][index]["guid"]
                guid_conf = self.Protocols["Edk2Guids"][prot_name]
                if (guid_idb == guid_conf):
                    self.Protocols["All"][index]["protocol_name"] = prot_name
                    self.Protocols["All"][index]["protocol_place"] = "edk2_guids"
                    fin = True
                    break
            if fin: continue
            for prot_name in self.Protocols["EdkGuids"].keys():
                guid_idb = self.Protocols["All"][index]["guid"]
                guid_conf = self.Protocols["EdkGuids"][prot_name]
                if (guid_idb == guid_conf):
                    self.Protocols["All"][index]["protocol_name"] = prot_name
                    self.Protocols["All"][index]["protocol_place"] = "edk_guids"
                    fin = True
                    break
            if fin: continue
            for prot_name in self.Protocols["Edk2Guids"].keys():
                guid_idb = self.Protocols["All"][index]["guid"]
                guid_conf = self.Protocols["Edk2Guids"][prot_name]
                if (guid_idb == guid_conf):
                    self.Protocols["All"][index]["protocol_name"] = prot_name
                    self.Protocols["All"][index]["protocol_place"] = "ami_guids"
                    fin = True
                    break
            if fin: continue
            if not "protocol_name" in self.Protocols["All"][index]:
                self.Protocols["All"][index]["protocol_name"] = "ProprietaryProtocol"
                self.Protocols["All"][index]["protocol_place"] = "unknown"

    @classmethod
    def print_all(cls):
        analyser = cls()
        analyser.get_boot_services()
        print("\r\nBoot services:")
        analyser.list_boot_services()
        analyser.get_protocols()
        analyser.get_prot_names()
        data = analyser.Protocols["All"]
        print("\r\nProtocols:")
        for element in data:
            guid_str = "[guid] " + str(map(hex, element["guid"]))
            print("\t [address] " + hex(element["address"]))
            print("\t [service] " + element["service"])
            print("\t [protocol_name] " + element["protocol_name"])
            print("\t [protocol_place] " + element["protocol_place"])
            print("\t " + guid_str)
            print("\t " + "*" * len(guid_str))

def main():
    print("Usage:")
    print(" * analyser = Analyser()")
    print(" * analyser.help()")
    Analyser().print_all()

if __name__=="__main__":
    main()