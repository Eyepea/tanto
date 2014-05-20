%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

Name: tanto
Version: 1.1
Release: 1%{?dist}
License: GPLv3 
Source0: https://projects.eyepea.eu/%{name}-%{version}.tar.bz2
Group: Development/Languages
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: python-devel
BuildRequires: python-setuptools
Requires: python-argparse
Requires: python-configobj
Requires: python-pynsca
Requires: python-requests
Requires: nagios-plugins-all

Summary: Monitoring daemon
URL: http://www.eyepea.eu

%description
Monitoring daemon.

%prep
%setup -n %{name}-%{version}

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
mkdir -p %{buildroot}/etc/tanto/{inputs,outputs}
install -Dpm 644 %{buildroot}/usr/etc/cron.d/tanto %{buildroot}/etc/cron.d/tanto
install -Dpm 644 %{buildroot}/usr/etc/tanto/logging.ini %{buildroot}/etc/tanto/
install -Dpm 644 %{buildroot}/usr/etc/tanto/inputs/nagios_plugins.cfg %{buildroot}/etc/tanto/inputs/
install -Dpm 644 %{buildroot}/usr/etc/tanto/outputs/email.cfg %{buildroot}/etc/tanto/outputs/
install -Dpm 644 %{buildroot}/usr/etc/tanto/outputs/nsca.cfg %{buildroot}/etc/tanto/outputs/
install -Dpm 644 %{buildroot}/usr/etc/tanto/outputs/ws_shinken.cfg %{buildroot}/etc/tanto/outputs/
rm -rf %{buildroot}/usr/etc/
sed -i 's/lib\//lib64\//g' %{buildroot}/etc/tanto/inputs/nagios_plugins.cfg

%clean
rm -rf %{buildroot}

%post

%files
%config /etc/tanto
%config /etc/cron.d/tanto
%defattr(-,root,root,-)
%doc LICENSE README.rst
%{_bindir}/tanto
%dir %{python_sitelib}/monitoring_agent/
%attr(0755,root,root) %{python_sitelib}/monitoring_agent/*.py*
%attr(0755,root,root) %{python_sitelib}/monitoring_agent/*/*.py*
%attr(0755,root,root) %{python_sitelib}/monitoring_agent/*/configspecs/*.cfg
%{python_sitelib}/tanto-%{version}-py2.6.egg-info/

%dir

%changelog

* Tue May 20 2014 Xavier Devlamynck <xd@eyepea.eu> - 1.1-1
- ep-monitoring-agent -> tanto
- upgrade to 1.1

* Wed Feb 20 2014 Xavier Devlamynck <xd@eyepea.eu> - 1.0-1
- Initial release
