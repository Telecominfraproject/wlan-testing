This automation assumes that the AP is configured as pass-through AP, not
router:

# Until cloud-sdk is integrated, stop opensync so we can do local config
service opensync stop
service opensync disable

# Configure /etc/config/network to bridge eth ports and wifi devices.

# Disable DHCP
/etc/init.d/dnsmasq disable
/etc/init.d/dnsmasq stop

# Disable DHCP v6
/etc/init.d/odhcpd disable
/etc/init.d/odhcpd stop

# Disable firewall ???
/etc/init.d/firewall disable
/etc/init.d/firewall stop

/etc/init.d/network reload

