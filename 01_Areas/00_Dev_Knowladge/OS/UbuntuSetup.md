# Ubuntu Setup

## Updating os

`sudo vim /etc/update-manager/release-upgrades` - Getting right version

There is couple of options:

`lts` 
`normal`
`none`

[Native update on Azure](https://ubuntu.com/blog/announcing-in-place-upgrade-from-ubuntu-server-to-ubuntu-pro-on-azure)

In Azure CLI run:

`az vm update -g myResourceGroup -n myVmName --license-type UBUNTU_PRO`

and then run these commands in the instance that you have converted:

`sudo apt install ubuntu-advantage-tools`
`sudo pro auto-attach`

Verify that Ubuntu Pro is enabled on your instance by running:

`pro status --all --wait`

Prior to this native functionality existing, the advice was as follows:


## Normal update

`lsb_release -a` - getting current version

apt update
apt upgrade
`sudo apt-get install update-manager-core`
`sudo apt-get install dist-upgrade -y`
`sudo do-release-upgrade`

If you run a firewall, you may need to temporarily open this port. 
As this is potentially dangerous it's not done automatically. 
You can screen or tmux, or if you're ready to proceed with the upgrade. 
Opening port:
`iptables -I INPUT -p tcp --dport 1022 -j ACCEPT`


> After reboot

`sudo do-release-upgrade -d`

> `-d` stnads for **Dev** meaning it's developer version with unstalbe if I wana stable jsut need to stick `do-release-upgrade`
