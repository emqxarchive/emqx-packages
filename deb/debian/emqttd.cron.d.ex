#
# Regular cron jobs for the emqttd package
#
0 4	* * *	root	[ -x /usr/bin/emqttd_maintenance ] && /usr/bin/emqttd_maintenance
