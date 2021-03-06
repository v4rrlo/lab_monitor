import server
import sys
import argparse

def status(args):
    hypervisor = server.ESXiHypervisor(args.address, "root", "ChangeMe")
    hypervisor.log.info("Getting status of ESXi virtual machine %s ID= %s", args.address, args.vmid)
    hypervisor.log.info("Is vmWareTools installed? %s", hypervisor.check_vmwaretools(args.vmid))
    hypervisor.log.info(hypervisor.get_status(args.vmid))

def shutdown(args):
    hypervisor = server.ESXiHypervisor(args.address, "root", "ChangeMe")
    if args.force:
        hypervisor.log.info("Forced shutdown of ESXi virtual machine %s ID=%s timeout =%s",args.address, args.vmid, args.timeout)
        return hypervisor.execute_shutdown_vm(args.vmid, args.timeout, args.force)
    else:
        hypervisor.log.info("Shutdown of ESXi virtual machine %s ID=%s timeout=%s",args.address, args.vmid, args.timeout)
        return hypervisor.execute_shutdown_vm(args.vmid, args.timeout)

parser = argparse.ArgumentParser(prog="esxi_vm", description='Manage ESXi virtual machine')
subparsers = parser.add_subparsers()
parser_status = subparsers.add_parser("status", help="Display status of ESXi virtual machine")
parser_status.add_argument("address", help="Address of ESXi server")
parser_status.add_argument("vmid", help="ID of running virtual machine")
parser_status.set_defaults(func=status)

parser_shutdown = subparsers.add_parser("shutdown", help="Shutdown ESXi vritual machine")
parser_shutdown.add_argument("-f", "--force", action="store_true", help="Force shutdown of virtual machine (possible data loss)")
parser_shutdown.add_argument("-t", "--timeout", action="store", type=int, default=300, help="Vritual machine shutdown timeout in seconds")
parser_shutdown.add_argument("address", help="Address of ESXi server")
parser_shutdown.add_argument("vmid", help="ID of running virtual machine")
parser_shutdown.set_defaults(func=shutdown)

args = parser.parse_args()
args.func(args)