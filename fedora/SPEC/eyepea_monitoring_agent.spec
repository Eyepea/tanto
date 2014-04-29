Name: 			eyepea-monitoring-agent
Version:		0.9
Release:        	4%{?dist}
Summary: 		Eyepea Monitoring agent for passive nagios checks

License: 		GNU Affero General Public License v3
URL:                    https://pypi.python.org/pypi/eyepea-monitoring-agent
Source0: 		https://pypi.python.org/packages/source/e/eyepea-monitoring-agent/eyepea-monitoring-agent-0.9.tar.gz

BuildArch:             noarch
Requires:              pynsca
Requires:              python-mcrypt
Requires:              python-configobj
Requires:              python-requests
Requires:              nagios-plugins-all

%description
To monitor the servers with Shinken, Nagios or Icinga, system administrators usually configure active checks of the monitored servers. It means the monitoring system must have a direct network access to the monitored server. With Eyepea monitoring agent, this model is reverted, it does passive checks of your monitored servers. You don't need to open an access from your monitoring system to the monitored servers.The main use case of this tool is to monitor distant servers in a complex network where you can't connect directly for security reasons, typically with a large client. You need only to open NSCA or HTTP(S) port from the monitored server to the monitoring system.

%prep
%setup -q


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
#python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
%{__python} setup.py install --single-version-externally-managed -O1 --root $RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf

%files
%files -f INSTALLED_FILES
%defattr(-,root,root)

%doc



%changelog
* Sat Apr 06 2013 Tyler Bennett <tylerb@trix2voip.com> - 0.9-4
- changed dependency nagios-plugins to nagios-plugins-all

* Sat Apr 06 2013 Tyler Bennett <tylerb@trix2voip.com> - 0.9-3
- added dependy of nagios-plugins to requires list

* Sat Apr 06 2013 Tyler Bennett <tylerb@trix2voip.com> - 0.9-2
- initial build

