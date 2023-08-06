import subprocess
import yaml
import threading
import paramiko
import socket
import time
import sys
from terminaltables import AsciiTable
import os
import shutil




class VirtualMachine(object):
    def __init__(self,vm_config,ssh_user="",ssh_password=""):
        self.qemu_bin = shutil.which("qemu-system-x86_64")
        self.name = vm_config["name"]
        self.memory = vm_config["memory"]
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password
        self.port_forward = vm_config["port-forward"]
        if not os.path.exists(".data"): os.mkdir(".data")

    def setup(self,name, ssh_port):
        attempts = 0
        print("[+] Setting up VM: {0} on port {1}".format(name,ssh_port))
        while attempts < 3:
            try: 
                location = ("127.0.0.1", int(ssh_port))
                a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                a_socket.connect(location)
                banner = a_socket.recv(100)
                if "SSH" in str(banner):
                    print("[+] VM Ready!")
                    break
                else:
                    print("[+] Waiting the VM to start")    
                    time.sleep(10)                  
            except Exception as e:
                print("[!] Waiting port %s to be open"%ssh_port)
                time.sleep(10)
            attempts += 1
        
        attempts = 0
        while attempts < 3:
            try:
                ssh = paramiko.SSHClient()
                ssh.load_system_host_keys()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname='127.0.0.1',port=ssh_port,username=self.ssh_user,password=self.ssh_password)
                print("[+] Setting the hostname")
                stdin,stdout,stderr = ssh.exec_command("hostnamectl set-hostname %s "%name)
                if stderr.channel.recv_exit_status() != 0:
                    stderr.read()
                else:
                    stdout.read()
                break
            except Exception as e:
                print("[+] Waiting for an ssh connection") 
                print(e)
                time.sleep(10)
            attempts += 1

    def create(self):
        print("[+] Creating VM: {0}".format(self.name))
        if not os.path.exists(".data/%s.qcow2"%self.name): shutil.copyfile("debian.qcow2", ".data/%s.qcow2"%self.name)
        params = []
        params.append("{0} --nographic --pidfile .data/{1}.pid".format(self.qemu_bin, self.name))
        params.append("-m %s"%self.memory)
        port_forward = ""
        setup_port = 0
        for p in self.port_forward:
            host_port, guest_port = p.split(":")
            if int(guest_port) == 22: setup_port = host_port
            port_forward += ",hostfwd=tcp::{0}-:{1}".format(host_port,guest_port)
        params.append("-nic user,id=net0"+port_forward)
        params.append("-drive file=.data/%s.qcow2"%self.name)
        qemu_cmd = " ".join(params)
        #print(qemu_cmd)
        output = subprocess.Popen([qemu_cmd],stdout=subprocess.PIPE,shell=True)       
        self.setup(self.name, setup_port)

    def destroy(self,vm):
        if os.path.exists(".data/%s.qcow2"%vm["name"]): 
            shutil.rmtree(".data/%s.qcow2"%vm["name"])
        else:
            print("[+] VM not provisioned or already destroyed")

        
class Tamarin(object):
    def __init__(self,file_name="Inventory.yml"):
        with open(file_name, "r") as f:
            self.inventory = yaml.load(f.read(),Loader=yaml.FullLoader)
            self.ssh_user = self.inventory["inventory"]["ssh-user"]
            self.ssh_password = self.inventory["inventory"]["ssh-password"]

    def usage(self):
        print("""
        Usage:
        tamarin.py [provision|destroy]
        tamarin.py start [vm_name]
        tamarin.py stop [vm_name]
        tamarin.py destroy [vm_name]
        tamarin.py status
        tamarin.py help
        """)

    def provision(self, vm, ssh_port):
        attempts = 0
        while attempts < 3:
            try: 
                location = ("127.0.0.1", ssh_port)
                a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                a_socket.connect(location)
                banner = a_socket.recv(100)
                if "SSH" in str(banner):
                    print("[+] VM Ready!")
                    break
                else:
                    print("[+] Waiting the VM to start")    
                    time.sleep(10)                  
            except Exception as e:
                print(e)
                time.sleep(10)
            attempts += 1

        try:
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname='127.0.0.1',port=ssh_port,username=self.ssh_user,password=self.ssh_password)
            stdin,stdout,stderr = ssh.exec_command("echo %s > /etc/hostname"%vm["name"])
            if stderr.channel.recv_exit_status() != 0:
                stderr.read()
            else:
                stdout.read()
            
        except Exception as e:
            print("[+] Waiting for an ssh connection")            


    def start(self,name=""):
        for vm_config in self.inventory["inventory"]["vms"]:
            if vm_config["name"] == sys.argv[2]:
                    vm = VirtualMachine(vm_config, self.ssh_user, self.ssh_password)
                    t = threading.Thread(target=vm.create,args=())
                    t.start()
                    while t.is_alive():
                        time.sleep(5)
                    t.join()
                    break  

    def status(self):
        table_data = [
                ['Name', 'status'],
            ]
        for vm in self.inventory["inventory"]["vms"]:
            status = "Running" if os.path.exists(".data/{0}.pid".format(vm["name"])) else "Stopped"
            table_data.append([vm["name"], status])
        
        table = AsciiTable(table_data)
        print (table.table)

    def stop(self, vm):
        with open(".data/{0}.pid".format(vm)) as f:
            pid = int(f.read())
            os.kill(pid, 1)
            print("[!] Shutting down VM: {0}".format(sys.argv[2]))

    def destroy(self,vm):
        if os.path.exists(".data/%s.qcow2"%vm): 
            os.remove(".data/%s.qcow2"%vm)
        else:
            print("[+] VM not provisioned or already destroyed")

    
def main():
    tamarin = Tamarin()
    if len(sys.argv) < 2:
        tamarin.usage()
    elif sys.argv[1] == "start":
        tamarin.start(sys.argv[2])                     
    elif sys.argv[1] == "stop":
        tamarin.stop(sys.argv[2])
    elif sys.argv[1] == "destroy":
        tamarin.stop(sys.argv[2])
        tamarin.destroy(sys.argv[2])
    elif sys.argv[1] == "status":
        tamarin.status()
        
if __name__ == "__main__":
    main()