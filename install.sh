#!/bin/bash
echo "AIM installer (version 1.0.0)"
if test "`whoami`" != "root"; then
	echo "This script must be run as root."
	exit
fi

echo "Copying AIM to /usr/bin..."
cp aim.py /usr/bin/aim
chmod a+rx /usr/bin/aim

echo "Creating /usr/share/aim directory..."
mkdir /usr/share/aim
chmod a+r /usr/share/aim

echo "Adding /usr/share/aim to path..."
echo "#!/bin/bash" >> /etc/profile.d/aim.sh
echo "export PATH=\$PATH:/usr/share/aim" >> /etc/profile.d/aim.sh

echo "Done."
