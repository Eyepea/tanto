%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

Name:           python-mcrypt
Version:        1.1 
Release:        5%{?dist}
Summary:        Python interface to mcrypt library

License:        LGPL
URL:            https://pypi.python.org/pypi/python-mcrypt/1.1
Source0:        http://labix.org/download/python-mcrypt/python-mcrypt-1.1.tar.gz

BuildRequires:  python-devel libmcrypt-devel gcc
Requires:  libmcrypt

%description
Python interface to mcrypt library

%prep
%setup -n python-mcrypt-1.1


%build
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root %{buildroot} --record=INSTALLED_FILES

 
%files
%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root,-)
%doc AUTHORS LICENSE NEWS README test.py


%changelog
* Tue May 20 2014 Xavier Devlamynck <xd@eyepea.eu> - 1.1-5
- fixed a lot of crappy stuffs

* Sat Apr 06 2013 Tyler Bennett <tylerb@trix2voip.com> - 1.1-4
- fixed issues with spec file not building

* Sat Apr 06 2013 Tyler Bennett <tylerb@trix2voip.com> - 1.1-3
- second attempt at building with a few fixes of spec file

* Sat Apr 06 2013 Tyler Bennett <tylerb@trix2voip.com> - 1.1-2
- initial build of python-mcrypt

