Name:           pynsca         
Version:        1.3
Release:        2%{?dist}
Summary:        A very simple module to allow nagios service check results to be submitted via NSCA. 

License:        MPL-1.1
URL:            https://pypi.python.org/pypi/pynsca/1.3
Source0:        https://pypi.python.org/packages/source/p/pynsca/pynsca-1.3.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Packager:       Tyler Bennett <tylerb@trix2voip.com>
Requires:       python-mcrypt
%description
A very simple module to allow nagios service check results to be submitted via NSCA.

%prep
#%setup -q -n pyncsa-%{version}
%setup -q
%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%build


%install
rm -rf RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{python_sitelib}
install -pm 755 pynsca.py $RPM_BUILD_ROOT%{python_sitelib}/

%clean
#[ "$RPM_BUILD_ROOT" != / ] && rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(-,root,root,-)
%doc
%{python_sitelib}/*


%changelog
* Sat Apr 06 2013 Tyler Bennett <tylerb@trix2voip.com> - 1.3-2
- initial build of pynsca

