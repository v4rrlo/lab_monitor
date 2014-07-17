import paramiko, time

class ESXiHypervisor:
    #initialazing - connecting to the ESXi server
    def __init__(self, hostname , username, password , own_id):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname, username=username, password=password)
        self.AVMIDS = []
        self.VMSL = {}
        self.H_id = own_id
 
    def get_status(self, Req_id):
        stdin, stdout, stderr = self.ssh.exec_command("/usr/bin/vim-cmd vmsvc/power.getstate " + str(Req_id) + "| tail -1 | awk '{print $2}'")
        stdout = stdout.read()
        stdout = stdout.strip('\n')

        if stdout == "on":
            return True
        else:
            return False
        
    #IDs of VMs are stored in an array, then we loop over IDs and get their statuses
    #If status is 'on', then we shutdown the VM and we add the ID to the list of IDs that are already shutted down by us
    def status(self):
        self.VMIDin, self.VMIDout, self.VMIDerr = self.ssh.exec_command("/usr/bin/vim-cmd vmsvc/getallvms | grep -v Vmid | awk '{print $1}'")
        self.VMIDout = self.VMIDout.read()
        self.VMIDout = self.VMIDout.split()
        
        for i in self.VMIDout:
            VM_id = int(i)
            Act_VM = ESXiVirtualMachine(VM_id, self.H_id, self)
            Act_VM.stat = Act_VM.status()
            if Act_VM.stat:
                self.AVMIDS.append(Act_VM)
            self.VMSL[Act_VM.id] = Act_VM.stat
        return self.VMSL

    #Shutting down every working VM
    def shutdown(self):
        for i in self.AVMIDS:
            if i.stat == False:
                print "VMID down:", i.id
            else:
                result = i.shutdown()
                if result.read() == "":
                    print i.id, "is down"
                    i.stat = False
                else:
                    print i.id, "IS NOT down"
                    print "Shutting down", i.id, " with power.off command"
                    i.force_shutdown()
                    i.stat = False
        time.sleep(10)

        print "All done. Powering off"
        #self.force_shutdown()         #shutting down the hypervisor after work is done

    #Shutting down the hypervisor
    def force_shutdown(self):
        self.ssh.exec_command("/sbin/shutdown.sh")
        self.ssh.exec_command("/sbin/poweroff")

    def force_shutdown_VirtualMachine(self, VM_id):
        stdin, stdout, stderr = self.ssh.exec_command("/usr/bin/vim-cmd vmsvc/power.off " + str(VM_id))
<<<<<<< HEAD
        time.sleep(1)
=======
>>>>>>> b045aebbab7f2a2ada1f7a236f726dd97f274ed6

    def shutdown_VirtualMachine(self, VM_id):
        stdin, stdout, stderr = self.ssh.exec_command("/usr/bin/vim-cmd vmsvc/power.shutdown " + str(VM_id))
        time.sleep(1)
        return stderr

class ESXiVirtualMachine:

    def __init__(self, VMid, H_id, hypervisor):
        self.id = VMid
        self.stat = None
        self.H_id = H_id
        self.ESXiHypervisor = hypervisor

    #Returning status of a VM
    def status(self):
        return ESXiHypervisor.get_status(self.ESXiHypervisor, self.id)

    #Shutting down a VM
    def shutdown(self):
        return ESXiHypervisor.shutdown_VirtualMachine(self.ESXiHypervisor, self.id)
    
    #Force shutting down of a VM    
    def force_shutdown(self):
        return ESXiHypervisor.force_shutdown_VirtualMachine(self.ESXiHypervisor, self.id)


