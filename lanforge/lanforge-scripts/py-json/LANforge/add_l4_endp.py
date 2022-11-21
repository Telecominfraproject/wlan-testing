# Flags for the add_l4_endp command
HTTP_auth_flags = {
    "BASIC"          : 0x1,     # Basic authentication
    "DIGEST"         : 0x2,     # Digest (MD5) authentication
    "GSSNEGOTIATE"   : 0x4,     # GSS authentication
    "NTLM"           : 0x8,     # NTLM authentication
}
proxy_auth_type_flags = {
    "BASIC"                   : 0x1,       # 1    Basic authentication
    "DIGEST"                  : 0x2,       # 2    Digest (MD5) authentication
    "GSSNEGOTIATE"            : 0x4,       # 4    GSS authentication
    "NTLM"                    : 0x8,       # 8    NTLM authentication
    "USE_PROXY_CACHE"         : 0x20,      # 32   Use proxy cache
    "USE_GZIP_COMPRESSION"    : 0x40,      # 64   Use gzip compression
    "USE_DEFLATE_COMPRESSION" : 0x80,      # 128  Use deflate compression
    "INCLUDE_HEADERS"         : 0x100,     # 256  especially for IMAP
    "BIND_DNS"                : 0x200,     # 512  Make DNS requests go out endpoints Port.
    "USE_IPV6"                : 0x400,     # 1024 Resolve URL is IPv6.  Will use IPv4 if not selected.
    "DISABLE_PASV"            : 0x800,     # 2048 Disable FTP PASV option (will use PORT command)
    "DISABLE_EPSV"            : 0x1000,    # 4096 Disable FTP EPSV option
}