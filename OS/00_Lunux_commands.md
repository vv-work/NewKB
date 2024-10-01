# Linux commands

## New list

`du -m ` - to see the size of the file in MB
`lsblk`     - to see the list of the devices.
`touch`     - to create File
`cat`       - to see the content of the file
`bat`       - to see the content of the file with `syntax highlighting`

`ddcutil setvcp 10 50` -set brightness to 50

## Remember

`htop`  - to see resource usage
`tree`  - see the hirarchy


`sudo umount /dev/sdX1`  - to unmount the device (if it is mounted)
`sudo mkfs.exfat -n <name_of_drive> -s 4K /dev/sdX` 
`sudo fsck.exfat /dev/sdX` - to check if SD is formatted in exFAT



### 2. **Write the image to the flash drive:**
Once the file is decompressed, use `dd` to write the `.image` file to the flash drive:

```bash
sudo dd if=8gb_flash.image of=/dev/sdX bs=1G
```

- Replace `/dev/sdX` with the correct device letter for your flash drive (e.g., `/dev/sdb`).
- `bs=1G`: This sets the block size to 1 GB, allowing for faster writing when dealing with large files.

### **Notes on the `.image` file extension in this context:**
- The `.image` file represents a **disk image** of the entire 8 GB flash drive. It's a sector-by-sector copy of the data, including the partition table, boot sectors, and file system.
- Writing this `.image` file to a new flash drive will **replicate** the original drive's structure, meaning the new flash drive will be an exact clone of the original.
- This process is commonly used for flashing pre-configured operating systems or bootable images onto drives like USB sticks or SD cards.


