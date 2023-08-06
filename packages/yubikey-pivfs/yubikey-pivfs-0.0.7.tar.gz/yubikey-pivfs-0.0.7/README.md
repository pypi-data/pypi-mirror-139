# YubiKey PIV FileSystem
## A FUSE filesystem for YubiKey PIV
### Ever wanted to use your YubiKey as a USB flash drive for storing your innermost thoughts? Well... 

### Features
#### Transparent compression
Filesystem content and metadata are compressed using ZSTD at its' highest level of compression. 
#### Transparent encryption
Filesystem content and metadata are protected using ARGON2ID at the data block level using a key derived from the 
allocated slots in conjunction with the private key of the chosen KEY SLOT. The current implementation yields the 
following properties:
- READ access is only possible by *knowledge of the allocated slots and their correct order* and having the ability to 
*perform private key operations using the KEY SLOT*
- WRITE access is granted by *knowledge of the PIV MANAGEMENT KEY*
#### Read-only operating mode
In this mode, the filesystem can just perform READ operations, if WRITE operations are attempted then the *EROFS: read-only file system* error will be raised.
To work in read-only mode, the `--management-key` and/or `--management-key-type` argument(s) must be omitted from the commandline.

### Usage
```
usage: ykpivfs [-h] --pin PIN [--format {no,yes,force}] [--management-key MANAGEMENT_KEY] [--management-key-type {TDES,AES128,AES192,AES256}] [--key-slot KEY_SLOT] [--data-slots DATA_SLOTS [DATA_SLOTS ...]]
               [--block-size BLOCK_SIZE] [--device-serial DEVICE_SERIAL] [--debug]
               mount_point

PIV-slots: {AUTHENTICATION, SIGNATURE, KEY_MANAGEMENT, CARD_AUTH, RETIRED1, RETIRED2, RETIRED3, RETIRED4, RETIRED5, RETIRED6, RETIRED7, RETIRED8, RETIRED9, RETIRED10, RETIRED11, RETIRED12, RETIRED13, RETIRED14, RETIRED15,
RETIRED16, RETIRED17, RETIRED18, RETIRED19, RETIRED20, ATTESTATION}

positional arguments:
  mount_point

options:
  -h, --help            show this help message and exit
  --pin PIN             PIN used for private key operations (e.g. "123456")
  --format {no,yes,force}
                        if the data-slots should be formatted: "no" - does not format; "yes" - formats only if unable to find existing filesystem; "force" - formats even if filesystem already exists
  --management-key MANAGEMENT_KEY
                        key in bytes (e.g. "010203040506070801020304050607080102030405060708")
  --management-key-type {TDES,AES128,AES192,AES256}
                        type of key (e.g. "TDES")
  --key-slot KEY_SLOT   PIV-slot containing the private-key used for deriving the encryption-key
  --data-slots DATA_SLOTS [DATA_SLOTS ...]
                        PIV-slots used for storing data and that represent the keying-material used in deriving the encryption-key
  --block-size BLOCK_SIZE
                        maximum amount of data that can fit into each of the data-slots
  --device-serial DEVICE_SERIAL
                        used with multiple devices to select the desired one based on the serial number
  --debug               shows verbose output

example: "ykpivfs --format yes --pin 123456 --management-key 010203040506070801020304050607080102030405060708 mountpoint"
```

#### Setup
Please decide which PIV slots you want to use for:
- KEY SLOT - private key operations, defaults to `KEY_MANAGEMENT`
- DATA SLOTS - store the filesystem data, defaults to `RETIRED1 RETIRED2 RETIRED3 RETIRED4 RETIRED5 RETIRED6 RETIRED7 RETIRED8 RETIRED9 RETIRED10 RETIRED11 RETIRED12 RETIRED13 RETIRED14 RETIRED15 RETIRED16 RETIRED17 RETIRED18 RETIRED19 RETIRED20`

And apply your selection using the `--key-slot` and `--data-slots` parameters in commandline.

*Please note:*
1. formatting means that all data that resides in the DATA SLOTS will be lost!
2. the order for the slot names in the `--data-slots` parameter matters!

#### First-time startup
Mount the filesystem using `--format yes`, such as:
```
python main.py --format yes --pin 123456 --management-key 010203040506070801020304050607080102030405060708 mountpoint
```
The `--format yes` argument will ensure that the YubiKey is formatted for first use (i.e. it does not already have a valid filesystem).

#### Regular startup
Mount the filesystem using `--format no`, such as:
```
python main.py --format no --pin 123456 --management-key 010203040506070801020304050607080102030405060708 mountpoint
```
The `--format no` argument will ensure that the YubiKey will not be formatted even in the case that no valid filesystem is recognized, this is to safeguard against accidental formatting that may arise due to transient issues.

### Disclaimer
This in an experimental project that may contain a multitude of bugs and may lead to damage of your YubiKey, loss of 
data and/or other unintended consequences and is provided mainly for educational or research purposes without any 
guarantees; please read the full disclaimer in the associated *LICENSE*.
