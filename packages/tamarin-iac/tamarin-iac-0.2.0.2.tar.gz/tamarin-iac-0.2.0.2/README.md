# Tamarin - Infrastructure as Code

<img src="img/tamarin.png" width="200"> 

Tamarin is a tool to provide Virtual Machines on any operating systems.

It was created initally to replace vagrant for the Mac M1, once the VirtualBox was not compatible with this new processor.

## Installation on Mac

    brew install qemu
    python3 -m pip install tamarin-iac

## How to use it

First you have to create a base image, like you do with any normal Linux installation:

    tamarin image create debian -iso debian.iso


First create a file called inventory.yml

Example:

    inventory:
        image: debian
        ssh-password: alisson
        ssh-user: root
        vms:
            - name: sandbox
              memory: 512
              port-forward:
              - '2222:22'
   

Then you can check your inventory using:

    $ tamarin status

    +-----------+---------+
    | Name      | status  |
    +-----------+---------+
    | webserver | Stopped |
    | database  | Stopped |
    +-----------+---------+

Run your VM:

    $ tamarin start
    [+] Creating VM: webserver
    [+] Setting up VM: webserver on port 4022
    [!] Waiting port 4022 to be open
    [+] VM Ready!
    [+] Setting the hostname

Access via ssh:

    (base) alissonmachado@Alissons-Air Tamarin % ssh root@localhost -p 4022
    root@localhost's password: 
    
    Linux webserver 5.10.0-11-amd64 #1 SMP Debian 5.10.92-1 (2022-01-18) x86_64
    root@webserver:~# 


