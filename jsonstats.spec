# Depends on redhat-rpm-config
%define distribution %(/usr/lib/rpm/redhat/dist.sh --disttype)
%define distribution_version %(/usr/lib/rpm/redhat/dist.sh --distnum)
%define python_minor_version %(%{__python} -c "import platform; print(platform.python_version_tuple()[1])")

%if "el" == "%{distribution}"
%{!?rhel: %define rhel %{distribution_version}}
%endif

%if 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
%endif

Name:            jsonstats
%define _name    jsonstatsd
Release:         1%{?dist}
Summary:         Client for exposing system information over a REST interface
Version:         0.6.0

Group:           Development/Libraries
License:         MIT
Source0:         %{name}-%{version}.tar.gz
Url:             https://github.com/tbielawa/restfulstatsjson

BuildArch:        noarch
# Common *Requires
Requires:         PyYAML
BuildRequires:    python2-devel
BuildRequires:    redhat-rpm-config


######################################################################
# RHEL 5/6
%if "%{distribution}" == "el"
# begin inner-if
%if 0%{?rhel} <= 6
Requires(post):   chkconfig
Requires(preun):  chkconfig
Requires(preun):  initscripts
Requires(postun): initscripts
%define boot_system sysv
%endif

######################################################################
# distribution is not "el", so probably fedora
%else

######################################################################
# Fedora =< 17 require systemd-units && systemd
%if 0%{?fedora} > 0
%if 0%{?fedora} <= 17
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units
%define boot_system systemd_old
%endif
%endif


######################################################################
# Fedora > 17 just requires systemd
%if 0%{?fedora} > 17
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
BuildRequires:    systemd
%define boot_system systemd_new
%endif

######################################################################
# (same w/ RHEL7+)
%if 0%{?rhel} >= 7
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
BuildRequires:    systemd
%define boot_system systemd_new
%endif

%endif

######################################################################
# Define the name of the init script to include in the %files section
######################################################################
%if %{boot_system} == "sysv"
%define init_script /etc/init.d/jsonstatsd
%else
%define init_script /usr/lib/systemd/system/%{_name}.service
%endif



######################################################################
# And this ends our *Requires madness. Let's set up the proper
# pre/post script handlers for registering the jsonstatsd service with
# the system init
######################################################################

######################################################################
# BEGIN SysV
# Reference: http://fedoraproject.org/wiki/Packaging:SysVInitScript#Initscripts_in_spec_file_scriptlets
######################################################################
%if %{boot_system} == "sysv"
%post
/sbin/chkconfig --add %{_name}

%preun
if [ $1 -eq 0 ] ; then
    /sbin/service %{_name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{_name}
fi

%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service ${_name} condrestart >/dev/null 2>&1 || :
fi
%endif
######################################################################
# END SysV
######################################################################

######################################################################
# BEGIN Systemd - Fedora 17 and older
# Reference: http://fedoraproject.org/wiki/Packaging:ScriptletSnippets#Manual_scriptlets_.28Fedora_17_or_older.29
######################################################################
%if %{boot_system} == "systemd_old"
%post
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable %{_name}.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{_name}.service > /dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart %{_name}.service >/dev/null 2>&1 || :
fi
%endif
######################################################################
# END Systemd - Fedora 17 and older
######################################################################

######################################################################
# BEGIN Systemd - Fedora 18+ & RHEL7+
######################################################################
%if %{boot_system} == "systemd_new"
%post
%systemd_post %{_name}.service

%preun
%systemd_preun %{_name}.service

%postun
%systemd_postun_with_restart %{_name}.service
%endif
######################################################################
# END Systemd - Fedora 18+ & RHEL7+
######################################################################

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
%{__mkdir_p} $RPM_BUILD_ROOT%{_localstatedir}/log/%{_name}

%clean
rm -rf $RPM_BUILD_ROOT

######################################################################
# files for 'jsonstats' package
%files
%defattr(-,root,root)
%{python_sitelib}/*
%{_bindir}/%{_name}
%{init_script}
%config(noreplace)/etc/sysconfig/%{_name}
%if 0%{?python_minor_version} > 4
%attr(0755,root,root) %dir %{_localstatedir}/log/%{_name}
%endif

######################################################################

%changelog
* Sun Nov 17 2013 Tim Bielawa <tbielawa@redhat.com> - 0.6.0-1
- Now daemonizes and has proper init scripts

* Mon Nov  4 2013 Tim Bielawa <tbielawa@redhat.com> - 0.5.0-2
- First functional release and RPM distribution.
