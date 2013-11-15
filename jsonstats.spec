%if 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
%endif

Name:            jsonstats
%define _name    jsonstatsd
Release:         1%{?dist}
Summary:         Client for exposing system information over a REST interface
Version:         0.5.0

Group:           Development/Libraries
License:         MIT
Source0:         %{name}-%{version}.tar.gz
Url:             https://github.com/tbielawa/restfulstatsjson

BuildArch:       noarch
Requires:        PyYAML
Requires(post):  chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
BuildRequires:   python2-devel



%description
A simple REST client which exposes provides arbitrary system
information ('facts'). The fact providing system is plugin
based. Exposing additional facts is as simple as returning a JSON
serializable python datastructure.


%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --root=$RPM_BUILD_ROOT
# mkdir -p $RPM_BUILD_ROOT/%{_mandir}/{man1,man5}/
# cp -v docs/man/man1/*.1 $RPM_BUILD_ROOT/%{_mandir}/man1/
# cp -v docs/man/man5/*.5 $RPM_BUILD_ROOT/%{_mandir}/man5/
# mkdir -p $RPM_BUILD_ROOT/%{_datadir}/juicer
# cp -vr share/juicer/completions $RPM_BUILD_ROOT/%{_datadir}/juicer/
# cp -vr share/juicer/juicer.conf $RPM_BUILD_ROOT/%{_datadir}/juicer/

%clean
rm -rf $RPM_BUILD_ROOT

# @@@@@**************@@@@@@@@@@@@@*************@@@@@@@@@@**********
# @@@@@******** NEED TO MAKE CONDITIONAL, SysV/Systemd @@**********
# @@@@@**************@@@@@@@@@@@@@*************@@@@@@@@@@**********


######################################################################
# New stuff
%post
/sbin/chkconfig --add %{_name}

######################################################################
# Get outta here
%preun
if [ $1 -eq 0 ] ; then
    /sbin/service %{_name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{_name}
fi
# @@@@@**************@@@@@@@@@@@@@*************@@@@@@@@@@**********
# @@@@@**** END NEED TO MAKE CONDITIONAL, SysV/Systemd @@**********
# @@@@@**************@@@@@@@@@@@@@*************@@@@@@@@@@**********



######################################################################
# files for 'jsonstats' package
%files
%defattr(-,root,root)
%{python_sitelib}/JsonStats
%if 0%{?rhel} >= 5
# nothing to do on python2.4 boxes (like RHEL5 stock)
%else
%{python_sitelib}/jsonstats*-info
%endif
%{_bindir}/jsonstats*

# @@@***@@@***@@@ conditional for SysV
/etc/init.d/%{_name}
# @@@***@@@***@@@ end conditional for SysV

%config(noreplace)/etc/sysconfig/%{_name}
######################################################################
%changelog
* Mon Nov  4 2013 Tim Bielawa <tbielawa@redhat.com> - 0.5.0-2
- First functional release and RPM distribution.
