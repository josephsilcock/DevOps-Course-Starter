# Deploying on a VM

There are scripts to deploy the app on a VM using ansible. The controller needs SSH access to the host, and ansible must
be installed. If ansible is not already installed on the controller, install it using:
```bash
$ sudo pip install ansible
```
Add the IP address of the host machines to `ansible-inventory`, and change the `remote_user` in `ansible-playbook.yml`
to the username of the host machines, then run the following to deploy the app:
```bash
ansible-playbook ansible-playbook.yml -i ansible-inventory
```
