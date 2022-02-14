from enum import Enum
from collections import namedtuple

# This is a surprising technique that is not an obvious extension to the language
class fe_fstype(namedtuple("fe_fstype", "id name"), Enum):
    EP_FE_GENERIC   =  8,   "generic"
    EP_FE_NFS       =  9,   "fe_nfs"
    EP_FE_ISCSI     = 10,   "fe_iscsi"
    EP_FE_CIFS      = 24,   "fe_cifs"
    EP_FE_NFS4      = 25,   "fe_nfs4"
    EP_FE_CIFSipv6  = 26,   "fe_cifs/ip6"
    EP_FE_NFSipv6   = 27,   "fe_nfs/ip6"
    EP_FE_NFS4ipv6  = 28,   "fe_nfs4/ip6"
    EP_FE_SMB2      = 29,   "fe_smb2"
    EP_FE_SMB2ipv6  = 30,   "fe_smb2/ip6"
    EP_FE_SMB21     = 35,   "fe_smb21"
    EP_FE_SMB21ipv6 = 36,   "fe_smb21/ip6"
    EP_FE_SMB30     = 37,   "fe_smb30"
    EP_FE_SMB30ipv6 = 38,   "fe_smb30/ip6"

    
class fe_payload_list(Enum):
        increasing      = 1 # bytes start at 00 and increase, wrapping if needed.
        decreasing      = 2 # bytes start at FF and decrease, wrapping if needed.
        random          = 3 # generate a new random payload each time sent.
        
        random_fixed    = 4 # Means generate one random payload, and send it over
                            # and over again.
        
        zeros           = 5 # Payload is all zeros (00).
        ones            = 6 # Payload is all ones  (FF).
        
        PRBS_4_0_3      = 7     # Use linear feedback shift register to generate pseudo random sequence.
                         # First number is bit-length of register, second two are TAPS (zero-based indexs)
                         # Seed value is always 1.
        
        PRBS_7_0_6     = 8 # PRBS (see above)
        PRBS_11_8_10   = 9 # PRBS (see above)
        PRBS_15_0_14   = 10 # PRBS (see above)
        custom         = 11 # Enter your own payload with the set_endp_payload cmd.

    
class fe_fio_flags(Enum):
        CHECK_MOUNT   =   0x1,    # (1) Attempt to verify NFS and SMB mounts match the configured values.
        AUTO_MOUNT    =   0x2,    # (2) Attempt to mount with the provided information if not already mounted.
        AUTO_UNMOUNT  =   0x4,    # (4)   Attempt to un-mount when stopping test.
        O_DIRECT      =   0x8,    # (8)   Open file with O_DIRECT flag, disables caching.  Must use block-size read/write calls.
        UNLINK_BW     =  0x10,    # (16)  Unlink file before writing.  This works around issues with CIFS for some file-servers.
        O_LARGEFILE   =  0x20,    # (32)  Open files with O_LARGEFILE.  This allows greater than 2GB files on 32-bit systems.
        UNMOUNT_FORCE =  0x40,    # (64)  Use -f flag when calling umount
        UNMOUNT_LAZY  =  0x80,    # (128)  Use -l flag when calling umount
        USE_FSTATFS   = 0x100,    # (256) Use fstatfs system call to verify file-system type when opening files.
                                    # This can take a bit of time on some file systems, but it can be used
                                    # to detect un-expected file-system unmounts and such.
        
        O_APPEND      = 0x200     # (512) Open files for writing with O_APPEND instead
                                    # of O_TRUNC.  This will cause files to grow ever larger.

    
    # base_endpoint_types cribbed from BaseEndpoint.java
    # we are unlikely to need this dictionary
class fe_base_endpoint_types(Enum):
    EP_FE_GENERIC = 8
    EP_FE_NFS = 9
    EP_FE_ISCSI = 10
    EP_FE_CIFS = 24
    EP_FE_NFS4 = 25
    EP_FE_CIFS6 = 26
    EP_FE_NFS6 = 27
    EP_FE_NFS46 = 28
    EP_FE_SMB2 = 29
    EP_FE_SMB26 = 30
    EP_FE_SMB21 = 35
    EP_FE_SMB216 = 36
    EP_FE_SMB30 = 37
    EP_FE_SMB306 = 38

