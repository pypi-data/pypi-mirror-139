# ios.cmds
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



"""Cisco IOS configuration commands module.

This module parses Cisco IOS configuration files into a dictionary.
"""



# --- imports ---



from deepops import deepsetdefault, deepget
from netaddr import IPNetwork

from .utils import (
    interface_canonicalize,
    ip_acl_ext_rule_canonicalize,
    ipv6_acl_rule_canonicalize,
    expand_set )

from ..config import IndentedContextualCommand
from ..misc import get_all_subclasses



# --- configuration command classes ---



# Cmd is created to be a shorthand for the IndentedContextualCommand
# class as we'll be using it a lot

Cmd = IndentedContextualCommand



# SYSTEM



class Cmd_Comment(Cmd):
    # we don't really need to match comments as they do nothing but it
    # avoids chugging through the entire list of commands and doing
    # nothing
    match = r"!.*"


class Cmd_Hostname(Cmd):
    match = r"hostname (?P<hostname>\S+)"

    def parse(self, cfg, hostname):
        cfg["hostname"] = hostname



# INTERFACE ...



class Cmd_Int(Cmd):
    match = r"interface (?P<int_name>\S+)"
    enter_context = "interface"

    def parse(self, cfg, int_name):
        int_name = interface_canonicalize(int_name)

        i = deepsetdefault(cfg, "interface", int_name)

        # IOS has an odd behaviour that, when an interface is created in
        # configure mode, it will default to shutdown or not, depending
        # on its type; in startup configurations, however, they are
        # always not shutdown
        #
        # we default to not shutdown, unless this has been explicitly
        # overridden: this has the effect of 'no shutdown'ing the
        # interface, if it is being created
        i.setdefault("shutdown", False)

        return i


class CmdContext_Int(Cmd):
    context = "interface"


class Cmd_Int_ARPTime(CmdContext_Int):
    match = r"arp timeout (?P<time>\d+)"

    def parse(self, cfg, time):
        cfg["arp-timeout"] = int(time)


class Cmd_Int_CDPEna(CmdContext_Int):
    match = r"(?P<no>no )?cdp enable"

    def parse(self, cfg, no):
        # we allow CDP to be 'no cdp enable' to clear the CDP status
        cfg["cdp-enable"] = not no


class Cmd_Int_ChnGrp(CmdContext_Int):
    match = r"channel-group (?P<id_>\d+)(?P<mode> .+)?"

    def parse(self, cfg, id_, mode):
        cfg["channel-group"] = int(id_), mode


class Cmd_Int_Desc(CmdContext_Int):
    match = r"description (?P<desc>.+)"

    def parse(self, cfg, desc):
        cfg["description"] = desc


class Cmd_Int_Encap(CmdContext_Int):
    match = r"encapsulation (?P<encap>dot1q \d+( native)?)"

    def parse(self, cfg, encap):
        # lower case the encapsulation definition as IOS stores 'dot1q'
        # as 'dot1Q'
        cfg["encapsulation"] = encap.lower()


class Cmd_Int_IPAccGrp(CmdContext_Int):
    match = r"ip access-group (?P<acl_name>\S+) (?P<dir_>in|out)"

    def parse(self, cfg, acl_name, dir_):
        cfg.setdefault("ip-access-group", {})[dir_] = acl_name


# ip address ...


class Cmd_Int_IPAddr(CmdContext_Int):
    match = r"ip address (?P<addr>\S+ \S+)"

    def parse(self, cfg, addr):
        cfg["ip-address"] = addr


class Cmd_Int_IPAddrSec(CmdContext_Int):
    match = r"ip address (?P<addr>\S+ \S+) secondary"

    def parse(self, cfg, addr):
        # secondary address - record it in a list
        cfg.setdefault("ip-address-secondary", set()).add(addr)


# ...


class Cmd_Int_IPFlowMon(CmdContext_Int):
    match = r"ip flow monitor (?P<flowmon>\S+) (?P<dir_>input|output)"

    def parse(self, cfg, flowmon, dir_):
        deepsetdefault(cfg, "ip-flow-monitor")[dir_] = flowmon


class Cmd_Int_IPHlprAddr(CmdContext_Int):
    match = r"ip helper-address (?P<addr>(global )?\S+)"

    def parse(self, cfg, addr):
        cfg.setdefault("ip-helper-address", set()).add(addr)


class Cmd_Int_IPIGMPVer(CmdContext_Int):
    match = r"ip igmp version (?P<ver>\S+)"

    def parse(self, cfg, ver):
        cfg["ip-igmp-version"] = ver


class Cmd_Int_IPMcastBdry(CmdContext_Int):
    match = r"ip multicast boundary (?P<acl>\S+)"

    def parse(self, cfg, acl):
        cfg["ip-multicast-boundary"] = acl


# ip ospf ...


class Cmd_Int_IPOSPFArea(CmdContext_Int):
    match = r"ip ospf (?P<proc>\d+) area (?P<area>[.0-9]+)"

    def parse(self, cfg, proc, area):
        cfg.setdefault("ip-ospf", {})["area"] = {
            "process": int(proc), "id": area }


class Cmd_Int_IPOSPFAuth(CmdContext_Int):
    match = r"ip ospf authentication( (?P<auth>\S+))?"

    def parse(self, cfg, auth):
        cfg.setdefault("ip-ospf", {})["authentication"] = auth


class Cmd_Int_IPOSPFCost(CmdContext_Int):
    match = r"ip ospf cost (?P<cost>\d+)"

    def parse(self, cfg, cost):
        cfg.setdefault("ip-ospf", {})["cost"] = int(cost)


class Cmd_Int_IPOSPFDeadIvl(CmdContext_Int):
    match = r"ip ospf dead-interval (?P<interval>\d+)"

    def parse(self, cfg, interval):
        cfg.setdefault("ip-ospf", {})["dead-interval"] = int(interval)


class Cmd_Int_IPOSPFHelloIvl(CmdContext_Int):
    match = r"ip ospf hello-interval (?P<interval>\d+)"

    def parse(self, cfg, interval):
        cfg.setdefault("ip-ospf", {})["hello-interval"] = int(interval)


class Cmd_Int_IPOSPFMsgDigKey(CmdContext_Int):
    match = r"ip ospf message-digest-key (?P<id_>\d+) md5 (?P<md5>.+)"

    def parse(self, cfg, id_, md5):
        m = deepsetdefault(cfg, "ip-ospf", "message-digest-key")
        m[int(id_)] = md5


class Cmd_Int_IPOSPFNet(CmdContext_Int):
    match = (r"ip ospf network (?P<net>broadcast|non-broadcast|"
             r"point-to-multipoint|point-to-point)")

    def parse(self, cfg, net):
        cfg.setdefault("ip-ospf", {})["network"] = net


# ip pim ...


class Cmd_Int_IPPIMMode(CmdContext_Int):
    match = r"ip pim (?P<mode>(sparse|dense|sparse-dense)-mode)"

    def parse(self, cfg, mode):
        cfg.setdefault("ip-pim", {})["mode"] = mode


class Cmd_Int_IPPIMBSRBdr(CmdContext_Int):
    match = r"ip pim bsr-border"

    def parse(self, cfg):
        cfg.setdefault("ip-pim", {})["bsr-border"] = True


# ...


class Cmd_Int_IPProxyARP(CmdContext_Int):
    match = r"(?P<no>no )?ip proxy-arp"

    def parse(self, cfg, no):
        cfg["ip-proxy-arp"] = not no


class Cmd_Int_IPVerifyUni(CmdContext_Int):
    match = r"ip verify unicast (?P<opt>.+)"

    def parse(self, cfg, opt):
        cfg["ip-verify-unicast"] = opt


class Cmd_Int_IPv6Addr(CmdContext_Int):
    match = r"ipv6 address (?P<addr>\S+)"

    def parse(self, cfg, addr):
        # IPv6 addresses involve letters so we lower case for
        # consistency
        cfg.setdefault("ipv6-address", set()).add(addr.lower())


class Cmd_Int_IPv6MultBdry(CmdContext_Int):
    match = r"ipv6 multicast boundary scope (?P<scope>\S+)"

    def parse(self, cfg, scope):
        cfg["ipv6-multicast-boundary-scope"] = scope


class Cmd_Int_IPv6PIMBSRBdr(CmdContext_Int):
    match = r"ipv6 pim bsr border"

    def parse(self, cfg):
        cfg.setdefault("ipv6-pim", {})["bsr-border"] = True


class Cmd_Int_IPv6TrafFilt(CmdContext_Int):
    match = r"ipv6 traffic-filter (?P<acl_name>\S+) (?P<dir_>in|out)"

    def parse(self, cfg, acl_name, dir_):
        cfg.setdefault("ipv6-traffic-filter", {})[dir_] = acl_name


class Cmd_Int_IPv6VerifyUni(CmdContext_Int):
    match = r"ipv6 verify unicast (?P<opt>.+)"

    def parse(self, cfg, opt):
        cfg["ipv6-verify-unicast"] = opt


# ospfv3 ...


class Cmd_Int_OSPFv3Area(CmdContext_Int):
    match = r"ospfv3 (?P<proc>\d+) area (?P<area>[.0-9]+)"

    def parse(self, cfg, proc, area):
        cfg.setdefault("ospfv3", {})["area"] = {
            "process": int(proc), "id": area }


class Cmd_Int_OSPFv3Cost(CmdContext_Int):
    match = r"ospfv3 cost (?P<cost>\d+)"

    def parse(self, cfg, cost):
        cfg.setdefault("ospfv3", {})["cost"] = int(cost)


class Cmd_Int_OSPFv3DeadIvl(CmdContext_Int):
    match = r"ospfv3 dead-interval (?P<interval>\d+)"

    def parse(self, cfg, interval):
        cfg.setdefault("ospfv3", {})["dead-interval"] = int(interval)


class Cmd_Int_OSPFv3HelloIvl(CmdContext_Int):
    match = r"ospfv3 hello-interval (?P<interval>\d+)"

    def parse(self, cfg, interval):
        cfg.setdefault("ospfv3", {})["hello-interval"] = int(interval)


class Cmd_Int_OSPFv3Net(CmdContext_Int):
    match = (r"ospfv3 network (?P<net>broadcast|non-broadcast|"
             r"point-to-multipoint|point-to-point)")

    def parse(self, cfg, net):
        cfg.setdefault("ospfv3", {})["network"] = net


# ...


class Cmd_Int_ServPol(CmdContext_Int):
    match = (r"service-policy( type (?P<type_>\S+))? (?P<dir_>input|output)"
             r" (?P<policy>\S+)")

    def parse(self, cfg, type_, dir_, policy):
        deepsetdefault(cfg, "service-policy", dir_)[type_] = policy


class Cmd_Int_Shutdown(CmdContext_Int):
    match = r"(?P<no>no )?shutdown"

    def parse(self, cfg, no):
        cfg["shutdown"] = not no


# standby ...


class Cmd_Int_StandbyIP(CmdContext_Int):
    match = r"standby (?P<grp>\d+) ip (?P<addr>\S+)"

    def parse(self, cfg, grp, addr):
        deepsetdefault(
            cfg, "standby", "group", int(grp))["ip"] = addr


class Cmd_Int_StandbyIPSec(CmdContext_Int):
    match = r"standby (?P<grp>\d+) ip (?P<addr>\S+) secondary"

    def parse(self, cfg, grp, addr):
        deepsetdefault(
            cfg, "standby", "group", int(grp), "ip-secondary",
            last=set()).add(addr)


class Cmd_Int_StandbyIPv6(CmdContext_Int):
    match = r"standby (?P<grp>\d+) ipv6 (?P<addr>\S+)"

    def parse(self, cfg, grp, addr):
        deepsetdefault(
            cfg, "standby", "group", int(grp), "ipv6", last=set()).add(addr)


class Cmd_Int_StandbyPreempt(CmdContext_Int):
    match = r"standby (?P<grp>\d+) preempt"

    def parse(self, cfg, grp):
        deepsetdefault(
            cfg, "standby", "group", int(grp))["preempt"] = True


class Cmd_Int_StandbyPri(CmdContext_Int):
    match = r"standby (?P<grp>\d+) priority (?P<pri>\d+)"

    def parse(self, cfg, grp, pri):
        deepsetdefault(
            cfg, "standby", "group", int(grp))["priority"] = int(pri)


class Cmd_Int_StandbyTimers(CmdContext_Int):
    match = r"standby (?P<grp>\d+) timers (?P<timers>\d+ \d+)"

    def parse(self, cfg, grp, timers):
        deepsetdefault(
            cfg, "standby", "group", int(grp))["timers"] = timers


class Cmd_Int_StandbyTrk(CmdContext_Int):
    match = r"standby (?P<grp>\d+) track (?P<obj>\d+)( (?P<extra>.+))?"

    def parse(self, cfg, grp, obj, extra):
        deepsetdefault(
            cfg, "standby", "group", int(grp), "track")[obj] = extra


class Cmd_Int_StandbyVer(CmdContext_Int):
    match = r"standby version (?P<ver>\d)"

    def parse(self, cfg, ver):
        deepsetdefault(cfg, "standby")["version"] = int(ver)


# ...


class Cmd_Int_StormCtrl(CmdContext_Int):
    match = r"storm-control (?P<traffic>\S+) level (?P<level>[0-9.]+)"

    def parse(self, cfg, traffic, level):
        deepsetdefault(cfg, "storm-control")[traffic] = float(level)


# switchport ...


class Cmd_Int_SwPort(CmdContext_Int):
    match = r"(?P<no>no )?switchport"

    def parse(self, cfg, no):
        cfg["switchport"] = not no


class Cmd_Int_SwPortMode(CmdContext_Int):
    match = r"switchport mode (?P<mode>\S+)"

    def parse(self, cfg, mode):
        cfg["switchport-mode"] = mode


class Cmd_Int_SwPortNoNeg(CmdContext_Int):
    match = r"switchport nonegotiate"

    def parse(self, cfg):
        cfg["switchport-nonegotiate"] = True


class Cmd_Int_SwPortTrkNtv(CmdContext_Int):
    match = r"switchport trunk native vlan (?P<vlan>\d+)"

    def parse(self, cfg, vlan):
        cfg["switchport-trunk-native"] = int(vlan)


class Cmd_Int_SwPortTrkAlw(CmdContext_Int):
    match = (r"switchport trunk allowed vlan "
             r"((?P<complete>(none|all))|(?P<add>add )?(?P<vlans>[0-9,-]+))")

    def parse(self, cfg, complete, add, vlans):
        if complete:
            # 'all' is the same as no configuration present
            if complete == "all":
                if "switchport-trunk-allow" in cfg:
                    cfg.pop("switchport-trunk-allow")

            # 'none' is explicitly no VLANs
            elif complete == "none":
                cfg["switchport-trunk-allow"] = set()

        elif add:
            cfg.setdefault("switchport-trunk-allow", set()).update(
                expand_set(vlans))

        else:
            cfg["switchport-trunk-allow"] = expand_set(vlans)



# ...


class Cmd_Int_VRFFwd(CmdContext_Int):
    match = (r"vrf forwarding (?P<name>\S+)")

    def parse(self, cfg, name):
        cfg["vrf-forwarding"] = name


class Cmd_Int_XConn(CmdContext_Int):
    match = r"xconnect (?P<remote>[0-9.]+ \d+ .+)"

    def parse(self, cfg, remote):
        cfg["xconnect"] = remote



# IP ACCESS-LIST STANDARD



class Cmd_ACLStdRule(Cmd):
    match = r"access-list (?P<num>\d{1,2}|1[3-9]\d{2}) (?P<rule>.+)"

    def parse(self, cfg, num, rule):
        deepsetdefault(
            cfg, "ip-access-list-standard", num, last=[]).append(rule)


class Cmd_IPACL_Std(Cmd):
    match = r"ip access-list standard (?P<acl_name>.+)"
    enter_context = "ip-acl_std"

    def parse(self, cfg, acl_name):
        return deepsetdefault(
                   cfg, "ip-access-list-standard", acl_name, last=[])


class Cmd_IPACL_Std_Rule(Cmd):
    context = "ip-acl_std"
    match = r"(?P<rule>(permit|deny) +.+)"

    def parse(self, cfg, rule):
        cfg.append(rule)


class Cmd_ACLExtRule(Cmd):
    match = r"access-list (?P<num>1\d{2}|2[0-6]\d{2}) (?P<rule>.+)"

    def parse(self, cfg, num, rule):
        deepsetdefault(
            cfg, "ip-access-list-extended", num, last=[]
            ).append(ip_acl_ext_rule_canonicalize(rule))


class Cmd_IPACL_Ext(Cmd):
    match = r"ip access-list extended (?P<name>.+)"
    enter_context = "ip-acl_ext"

    def parse(self, cfg, name):
        return deepsetdefault(cfg, "ip-access-list-extended", name, last=[])


class Cmd_IPACL_Ext_Rule(Cmd):
    context = "ip-acl_ext"
    match = r"(?P<rule>(permit|deny) +.+)"

    def parse(self, cfg, rule):
        cfg.append(ip_acl_ext_rule_canonicalize(rule))



# IPV6 ACCESS-LIST ...



class Cmd_IPv6ACL(Cmd):
    match = r"ipv6 access-list (?P<name>.+)"
    enter_context = "ipv6-acl"

    def parse(self, cfg, name):
        return deepsetdefault(cfg, "ipv6-access-list", name, last=[])


class Cmd_IPv6ACL_Rule(Cmd):
    context = "ipv6-acl"
    match = r"(?P<rule>(permit|deny) +.+)"

    def parse(self, cfg, rule):
        cfg.append(ipv6_acl_rule_canonicalize(rule))



# IP AS-PATH ACCESS-LIST ...



class Cmd_IPASPathACL(Cmd):
    match = (r"ip as-path access-list (?P<num>\d+) (?P<action>permit|deny)"
             r" (?P<re>\S+)")

    def parse(self, cfg, num, action, re):
        l = deepsetdefault(cfg, "ip-as-path-access-list", int(num), last=[])
        l.append( (action, re) )



# IP[V6] PREFIX-LIST ...



class Cmd_IPPfx(Cmd):
    match = r"ip prefix-list (?P<list_>\S+) (seq \d+ )?(?P<rule>.+)"

    def parse(self, cfg, list_, rule):
        deepsetdefault(cfg, "ip-prefix-list", list_, last=[]).append(rule)


class Cmd_IPv6Pfx(Cmd):
    match = r"ipv6 prefix-list (?P<list_>\S+) (seq \d+ )?(?P<rule>.+)"

    def parse(self, cfg, list_, rule):
        deepsetdefault(
            cfg, "ipv6-prefix-list", list_, last=[]).append(rule.lower())



# IP[V6] ROUTE ...



class Cmd_IPRoute(Cmd):
    match = r"ip route (?P<route>.+)"

    def parse(self, cfg, route):
        cfg.setdefault("ip-route", set()).add(route)


class Cmd_IPv6Route(Cmd):
    match = r"ipv6 route (?P<route>.+)"

    def parse(self, cfg, route):
        # IPv6 addresses involve letters so we lower case for
        # consistency
        cfg.setdefault("ipv6-route", set()).add(route.lower())




# ROUTER BGP ...



class Cmd_RtrBGP(Cmd):
    # ASNs can be in 'n' as well as 'n.n' format
    match = r"router bgp (?P<as_>\d+(\.\d+)?)"
    enter_context = "router-bgp"

    def parse(self, cfg, as_):
        return deepsetdefault(cfg, "router", "bgp", as_)


class CmdContext_RtrBGP(Cmd):
    context = "router-bgp"


class CmdContext_RtrBGP_NbrFallOver(CmdContext_RtrBGP):
    match = (r"neighbor (?P<nbr>\S+) fall-over"
             r" (bfd (?P<bfd>single-hop|multi-hop)|route-map (?P<rtmap>\S+))")

    def parse(self, cfg, nbr, bfd, rtmap):
        deepsetdefault(cfg, "neighbor", nbr)["fall-over"] = (
            { "bfd": bfd } if bfd else { "route-map": rtmap })


class CmdContext_RtrBGP_NbrPwd(CmdContext_RtrBGP):
    match = r"neighbor (?P<nbr>\S+) password( (?P<enc>\d)) (?P<pwd>\S+)"

    def parse(self, cfg, nbr, enc, pwd):
        deepsetdefault(cfg, "neighbor", nbr)["password"] = {
            "encryption": int(enc), "password": pwd
        }


class CmdContext_RtrBGP_NbrPrGrp(CmdContext_RtrBGP):
    match = r"neighbor (?P<nbr>\S+) peer-group"

    def parse(self, cfg, nbr):
        deepsetdefault(cfg, "neighbor", nbr)["type"] = "peer-group"


class CmdContext_RtrBGP_NbrPrGrpMbr(CmdContext_RtrBGP):
    match = r"neighbor (?P<nbr>\S+) peer-group (?P<grp>\S+)"

    def parse(self, cfg, nbr, grp):
        deepsetdefault(cfg, "neighbor", nbr)["peer-group"] = grp


class CmdContext_RtrBGP_NbrRemAS(CmdContext_RtrBGP):
    match = r"neighbor (?P<nbr>\S+) remote-as (?P<rem_as>\d+(\.\d+)?)"

    def parse(self, cfg, nbr, rem_as):
        deepsetdefault(cfg, "neighbor", nbr)["remote-as"] = rem_as


class CmdContext_RtrBGP_NbrUpdSrc(CmdContext_RtrBGP):
    match = r"neighbor (?P<nbr>\S+) update-source (?P<int_name>\S+)"

    def parse(self, cfg, nbr, int_name):
        deepsetdefault(cfg, "neighbor", nbr)["update-source"] = int_name


# router bgp ... address-family ...


class Cmd_RtrBGP_AF(CmdContext_RtrBGP):
    match = (r"address-family (?P<af>ipv[46]( (?P<cast>unicast|multicast))?|"
             r"vpnv4|vpnv6)( vrf (?P<vrf>\S+))?")

    enter_context = "router-bgp-af"

    def parse(self, cfg, af, cast, vrf):
        # unicast/multicast is optional - if omitted, we assume unicast
        if not cast:
            af += " unicast"

        # put VRFs under a 'vrf' key in the configuration dictionary
        if vrf:
            return deepsetdefault(cfg, "vrf", vrf, "address-family", af)

        # put non-VRFs directly under the router process
        return deepsetdefault(cfg, "address-family", af)


class CmdContext_RtrBGP_AF(Cmd):
    context = "router-bgp-af"


class CmdContext_RtrBGP_AF_NbtAct(CmdContext_RtrBGP_AF):
    match = r"neighbor (?P<nbr>\S+) activate"

    def parse(self, cfg, nbr):
        deepsetdefault(cfg, "neighbor", nbr)["activate"] = True


class CmdContext_RtrBGP_AF_NbrAddPath(CmdContext_RtrBGP_AF):
    match = (r"neighbor (?P<nbr>\S+) additional-paths"
             r"(( (?P<snd>send))?( (?P<rcv>receive))?|( (?P<dis>disable)))")

    def parse(self, cfg, nbr, snd, rcv, dis):
        # additional paths is a set of all matching types (or 'disable')
        s = deepsetdefault(cfg, "neighbor", nbr)["additional-paths"] = {
            a for a in (snd, rcv, dis) if a }


class CmdContext_RtrBGP_AF_NbrAdvAddPath(CmdContext_RtrBGP_AF):
    match = (r"neighbor (?P<nbr>\S+) advertise additional-paths"
             r"( (?P<all>all))?"
             r"( (?P<best>best( (?P<best_n>\d+))))?"
             r"( (?P<grp_best>group-best))?")

    def parse(self, cfg, nbr, all, best, best_n, grp_best):
        a = deepsetdefault(cfg, "neighbor", nbr, "advertise")
        if all:
            a["all"] = True
        if best:
            a["best"] = best_n
        if grp_best:
            a["group-best"] = True


class CmdContext_RtrBGP_AF_NbrFltLst(CmdContext_RtrBGP_AF):
    match = (r"neighbor (?P<nbr>\S+) filter-list (?P<list_>\d+)"
             r" (?P<dir_>in|out)")

    def parse(self, cfg, nbr, list_, dir_):
        deepsetdefault(cfg, "neighbor", nbr, "filter-list")[dir_] = int(list_)


class CmdContext_RtrBGP_AF_NbrMaxPfx(CmdContext_RtrBGP_AF):
    match = (r"neighbor (?P<nbr>\S+) maximum-prefix (?P<max>\d+)"
             r"( (?P<thresh>\d+))?")

    def parse(self, cfg, nbr, max, thresh):
        m = deepsetdefault(cfg, "neighbor", nbr, "maximum-prefix")
        m["max"] = int(max)
        if thresh:
            m["threshold"] = int(thresh)


class CmdContext_RtrBGP_AF_NbrNHSelf(CmdContext_RtrBGP_AF):
    match = r"neighbor (?P<nbr>\S+) next-hop-self"

    def parse(self, cfg, nbr):
        deepsetdefault(cfg, "neighbor", nbr)["next-hop-self"] = True


class CmdContext_RtrBGP_AF_NbrPfxLst(CmdContext_RtrBGP_AF):
    match = (r"neighbor (?P<nbr>\S+) prefix-list (?P<list_>\S+)"
             r" (?P<dir_>in|out)")

    def parse(self, cfg, nbr, list_, dir_):
        deepsetdefault(cfg, "neighbor", nbr, "prefix-list")[dir_] = list_


class CmdContext_RtrBGP_AF_NbrRtMap(CmdContext_RtrBGP_AF):
    match = r"neighbor (?P<nbr>\S+) route-map (?P<rtmap>\S+) (?P<dir_>in|out)"

    def parse(self, cfg, nbr, rtmap, dir_):
        deepsetdefault(cfg, "neighbor", nbr, "route-map")[dir_] = rtmap


class CmdContext_RtrBGP_AF_NbrSndCmty(CmdContext_RtrBGP_AF):
    match = (r"neighbor (?P<nbr>\S+) send-community"
             r"( (?P<cmty>standard|extended|both))?")

    def parse(self, cfg, nbr, cmty):
        # this command adjusts the current state of the setting rather
        # than replacing it (e.g. entering "extended" when only
        # "standard" is set will change to "both")
        #
        # we don't worry about that but track each setting independently
        c = deepsetdefault(cfg, "neighbor", nbr, "send-community", last=set())
        if cmty in (None, "standard", "both"):
            c.add("standard")
        if cmty in ("extended", "both"):
            c.add("extended")


class CmdContext_RtrBGP_AF_NbrSoftRe(CmdContext_RtrBGP_AF):
    match = r"neighbor (?P<nbr>\S+) soft-reconfiguration inbound"

    def parse(self, cfg, nbr):
        deepsetdefault(cfg, "neighbor", nbr)["soft-reconfiguration"] = (
            "inbound")


class CmdContext_RtrBGP_AF_Redist(CmdContext_RtrBGP_AF):
    match = (r"redistribute (?P<proto>static|connected|ospf \d+|ospfv3 \d+)"
             r"( route-map (?P<rtmap>\S+))?( metric (?P<met>\d+))?")

    def parse(self, cfg, proto, rtmap, met):
        r = deepsetdefault(cfg, "redistribute", proto)
        if rtmap:
            r["route-map"] = rtmap
        if met:
            r["metric"] = int(met)



# ROUTER OSPF ...



class Cmd_RtrOSPF(Cmd):
    match = r"router ospf (?P<proc>\d+)"
    enter_context = "router-ospf"

    def parse(self, cfg, proc):
        return deepsetdefault(cfg, "router", "ospf", int(proc))


class CmdContext_RtrOSPF(Cmd):
    context = "router-ospf"


class Cmd_RtrOSPF_Id(CmdContext_RtrOSPF):
    match = r"router-id (?P<id_>[.0-9]+)"

    def parse(self, cfg, id_):
        cfg["id"] = id_


class Cmd_RtrOSPF_AreaNSSA(CmdContext_RtrOSPF):
    match = (r"area (?P<area>\S[.0-9]+)"
             r" nssa(?P<no_redist> no-redistribution)?"
             r"(?P<no_summ> no-summary)?")

    def parse(self, cfg, area, no_redist, no_summ):
        a = set()
        if no_redist: a.add("no-redistribution")
        if no_summ: a.add("no-summary")
        deepsetdefault(cfg, "area", area)["nssa"] = a


class Cmd_RtrOSPF_PasvInt(CmdContext_RtrOSPF):
    match = r"(?P<no>no )?passive-interface (?P<int_name>\S+)"

    def parse(self, cfg, no, int_name):
        p = deepsetdefault(cfg, "passive-interface")
        if int_name == "default":
            if not no:
                p["default"] = True
        else:
            deepsetdefault(
                p, "interface")[interface_canonicalize(int_name)] = not no



# ROUTER OSPFV3 ...



class Cmd_RtrOSPFv3(Cmd):
    match = r"router ospfv3 (?P<proc>\d+)"
    enter_context = "router-ospfv3"

    def parse(self, cfg, proc):
        return deepsetdefault(cfg, "router", "ospfv3", int(proc))


class CmdContext_RtrOSPFv3(Cmd):
    context = "router-ospfv3"


class Cmd_RtrOSPFv3_Id(CmdContext_RtrOSPFv3):
    match = r"router-id (?P<id_>[.0-9]+)"

    def parse(self, cfg, id_):
        cfg["id"] = id_


class Cmd_RtrOSPFv3_AreaNSSA(CmdContext_RtrOSPFv3):
    match = (r"area (?P<area>\S[.0-9]+)"
             r" nssa(?P<no_redist> no-redistribution)?"
             r"(?P<no_summ> no-summary)?")

    def parse(self, cfg, area, no_redist, no_summ):
        a = set()
        if no_redist: a.add("no-redistribution")
        if no_summ: a.add("no-summary")
        deepsetdefault(cfg, "area", area)["nssa"] = a


class Cmd_RtrOSPFv3_AF(CmdContext_RtrOSPFv3):
    # "unicast" on the end is effectively ignored
    match = r"address-family (?P<af>ipv4|ipv6)( unicast)?"
    enter_context = "router-ospfv3-af"

    def parse(self, cfg, af):
        return deepsetdefault(cfg, "address-family", af)


class CmdContext_RtrOSPFv3_AF(CmdContext_RtrOSPFv3):
    context = "router-ospfv3-af"


class Cmd_RtrOSPFv3_AF_PasvInt(CmdContext_RtrOSPFv3_AF):
    match = r"(?P<no>no )?passive-interface (?P<int_name>\S+)"

    def parse(self, cfg, no, int_name):
        p = deepsetdefault(cfg, "passive-interface")
        if int_name == "default":
            if not no:
                p["default"] = True
        else:
            deepsetdefault(
                p, "interface")[interface_canonicalize(int_name)] = not no


class Cmd_RtrOSPFv3_PasvInt(CmdContext_RtrOSPFv3):
    match = r"(?P<no>no )?passive-interface (?P<int_name>\S+)"

    def parse(self, cfg, no, int_name):
        # the handling of this command outside of an address-family
        # block is a bit odd - it isn't stored at the router process
        # level but in the address family block and only affects the
        # currently defined address families, so if an address family
        # is added later, this will not propagate down
        for af in cfg.get("address-family", []):
            p = deepsetdefault(cfg, "address-family", af, "passive-interface")
            if int_name == "default":
                if not no:
                    p["default"] = True
            else:
                deepsetdefault(
                    p, "interface")[interface_canonicalize(int_name)] = not no



# [NO] SPANNING-TREE ...



class Cmd_NoSTP(Cmd):
    match = r"no spanning-tree vlan (?P<tags>[-0-9,]+)"

    def parse(self, cfg, tags):
        cfg.setdefault(
            "no-spanning-tree-vlan", set()).update(expand_set(tags))


class Cmd_STPPri(Cmd):
    match = r"spanning-tree vlan (?P<tags>[-0-9,]+) priority (?P<pri>\d+)"

    def parse(self, cfg, tags, pri):
        cfg_stp_pri = cfg.setdefault("spanning-tree-vlan-priority", {})
        for tag in expand_set(tags):
            cfg_stp_pri[int(tag)] = int(pri)



# TRACK ...



class Cmd_Track(Cmd):
    match = r"track (?P<obj>\d+)"
    enter_context = "track"

    def parse(self, cfg, obj):
        # if there is no criterion, we're modifying an existing object,
        # which must have already been defined, so we deliberately don't
        # create it with deepsetdefault() but just deepget() it with
        # default_error set, to force an error here, if it doesn't exist
        return deepget(cfg, "track", int(obj), default_error=True)


class CmdContext_Track(Cmd):
    context = "track"


class Cmd_Track_Delay(CmdContext_Track):
    match = r"delay (?P<delay>.+)"

    def parse(self, cfg, delay):
        cfg["delay"] = delay


class Cmd_Track_IPVRF(CmdContext_Track):
    match = r"ip vrf (?P<vrf_name>\S+)"

    def parse(self, cfg, vrf_name):
        cfg["ip-vrf"] = vrf_name


class Cmd_Track_IPv6VRF(CmdContext_Track):
    match = r"ipv6 vrf (?P<vrf_name>\S+)"

    def parse(self, cfg, vrf_name):
        cfg["ipv6-vrf"] = vrf_name


class Cmd_Track_Obj(CmdContext_Track):
    match = r"object (?P<obj>.+)"

    def parse(self, cfg, obj):
        deepsetdefault(cfg, "object", last=set()).add(obj)


class Cmd_TrackRoute(Cmd):
    match = (r"track (?P<obj>\d+)"
           r" (?P<proto>ip|ipv6) route"
           r" (?P<net>[0-9a-fA-F.:]+/\d+|[0-9.]+ [0-9.]+)"
           r" (?P<extra>metric .+|reachability)")
    enter_context = "track"

    def parse(self, cfg, obj, proto, net, extra):
        # the 'net' can be in 'network netmask' or CIDR format, but the
        # netaddr.IPNetwork() object requires a slash between the
        # network and netmask, so we just change the space to a slash
        net = IPNetwork(net.replace(" ", "/"))

        # reconstruct a normalised version of the criterion
        criterion = ("%s route %s %s" % (proto, net, extra))

        # create the new track object and store the criterion in it
        t = deepsetdefault(cfg, "track", int(obj))
        t["criterion"] = criterion

        # return the track object for the new context
        return t


class Cmd_TrackOther(Cmd):
    match = r"track (?P<obj>\d+) (?P<other>(interface .+|list .+|stub-object))"
    enter_context = "track"

    def parse(self, cfg, obj, other):
        t = deepsetdefault(cfg, "track", int(obj))
        t["criterion"] = other

        return t



# VLAN ...



class Cmd_VLAN(Cmd):
    match = r"vlan (?P<tag>\d+)"
    enter_context = "vlan"

    def parse(self, cfg, tag):
        # create the VLAN configuration entry, setting an 'exists' key
        # as we might stop other information in here that isn't in the
        # VLAN definition itself in IOS (e.g. STP priority) in future
        v = deepsetdefault(cfg, "vlan", int(tag))
        v["exists"] = True

        return v


class CmdContext_VLAN(Cmd):
    context = "vlan"


class Cmd_VLAN_Name(CmdContext_VLAN):
    match = r"name (?P<name>\S+)"

    def parse(self, cfg, name):
        cfg["name"] = name



# VRF ...



class Cmd_VRF(Cmd):
    match = r"vrf definition (?P<name>\S+)"
    enter_context = "vrf"

    def parse(self, cfg, name):
        return deepsetdefault(cfg, "vrf", name)


class CmdContext_VRF(Cmd):
    context = "vrf"


class Cmd_VRF_RD(CmdContext_VRF):
    match = r"rd (?P<rd>\S+)"

    def parse(self, cfg, rd):
        cfg["rd"] = rd


class Cmd_VRF_RT(CmdContext_VRF):
    match = r"route-target (?P<dir_>import|export|both) (?P<rt>\S+)"

    def parse(self, cfg, dir_, rt):
        if dir_ in { "import", "both" }:
            deepsetdefault(cfg, "route-target", "import", last=set()).add(rt)
        if dir_ in { "export", "both" }:
            deepsetdefault(cfg, "route-target", "export", last=set()).add(rt)


class Cmd_VRF_AF(CmdContext_VRF):
    # "unicast" on the end is effectively ignored
    match = r"address-family (?P<af>ipv4|ipv6)( unicast)?"
    enter_context = "vrf-af"

    def parse(self, cfg, af):
        return deepsetdefault(cfg, "address-family", af)


class CmdContext_VRF_AF(Cmd):
    context = "vrf-af"


class Cmd_VRF_AF_RT(CmdContext_VRF_AF):
    match = r"route-target (?P<dir_>import|export|both) (?P<rt>\S+)"

    def parse(self, cfg, dir_, rt):
        if dir_ in { "import", "both" }:
            deepsetdefault(cfg, "route-target", "import", last=set()).add(rt)
        if dir_ in { "export", "both" }:
            deepsetdefault(cfg, "route-target", "export", last=set()).add(rt)



# commands is the list of commands to add to the parser - it is all
# subclasses of Cmd (IndentedContextualCommand) which have the 'match'
# attribute defined
#
# the CiscoIOSConfig class adds these to the object upon instantiation,
# by the _add_commands() method.

commands = [ c for c in get_all_subclasses(Cmd) if c.match is not None ]
