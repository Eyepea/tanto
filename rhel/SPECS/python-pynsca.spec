%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

%global real_name pynsca

Name: python-pynsca
Version: 1.5
Release: 1%{?dist}
License: GPLv3 
Source0: https://pypi.python.org/packages/source/p/pynsca/%{real_name}-%{version}.tar.gz
Group: Development/Languages
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: python-devel
BuildRequires: python-setuptools

Summary: Monitoring daemon
URL: https://pypi.python.org/pypi/pynsca 

%description
Monitoring daemon.

%prep
%setup -n %{real_name}-%{version}

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%post

%files
%defattr(-,root,root,-)
%doc README.txt
%attr(0755,root,root) %{python_sitelib}/pynsca.py*
%{python_sitelib}/pynsca-1.5-py2.6.egg-info/

%dir

%changelog

* Wed Feb 20 2014 Xavier Devlamynck <xd@eyepea.eu> - 1.5-1
- Initial release
