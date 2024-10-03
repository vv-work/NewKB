# Remote Access 

- Write notes on Algorithms used in SSH keys
    - how `logarithms` are used in cryptography ? 
    - how asymetric encryption works ? 
- Write notes on encrypted drive on Linux ?

- What types of drive formatting exist ? 

- What is [Mosh](https://mosh.org/) ? 
    - How does it work ? 
    - How is it different from SSH ?
What a fuck is **SHA-2** ?

- What is Termius solution ?

If I can just run though my CV while wrting notes, It would save me so much yak shaving.
 
## SSH keys 

`ed25519` - Edwards-curve Digital Signature Algorithm (EdDSA) 
    - Algorithm elliptic curve cryptography

`RSA` - Rivest-Shamir-Adleman

### SSH server setup 

On local linux machine

#### OpenSSH installation

```bash 
sudo pacman -S openssh

```
#### Enable and start SSHD

```bash
sudo systemctl enable sshd
sudo systemctl start sshd
```




