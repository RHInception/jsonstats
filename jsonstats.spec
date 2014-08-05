# Depends on redhat-rpm-config
%define distribution %(/usr/lib/rpm/redhat/dist.sh --disttype)
%define distribution_version %(/usr/lib/rpm/redhat/dist.sh --distnum)

%if "el" == "%{distribution}"
%{!?rhel: %define rhel %{distribution_version}}
%endif

%if 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
%endif

# Fedora >= 18, RHEL >= 7, and CentOS >= 7 have migrated to systemd
# and now provide the proper RPM macros
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7 || 0%{?centos} >= 7
%global with_systemd_macros 1
%global with_tmpfiles_macro 1
%endif

Name:            jsonstats
%define _name    jsonstatsd
Release:         4%{?dist}
Summary:         Client for exposing system information over a REST interface
Version:         1.0.3

Group:           Development/Libraries
License:         MIT
Source0:         %{name}-%{version}.tar.gz
Url:             https://github.com/RHInception/jsonstats

BuildArch:        noarch
# Common *Requires
Requires:         PyYAML
BuildRequires:    python2-devel
BuildRequires:    redhat-rpm-config


######################################################################
# Fedora >= 18, RHEL >= 7, and CentOS >= 7
%if 0%{?with_systemd_macros}
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
BuildRequires:    systemd
%endif

# RHEL 5/6
%if ! 0%{?with_systemd_macros}
Requires(post):   chkconfig
Requires(preun):  chkconfig
Requires(preun):  initscripts
Requires(postun): initscripts
%endif

######################################################################
# And this ends our *Requires madness. Let's set up the proper
# pre/post script handlers for creating the jsonstatsd user and
# registering the service with the system init
######################################################################

%pre
getent passwd %{_name} >/dev/null 2>&1 || %{_sbindir}/useradd -M -r --shell %{_sbindir}/nologin  %{_name}

%post
%if 0%{?with_systemd_macros}
%systemd_post %{_name}.service
%else
/sbin/chkconfig --add %{_name}
%endif

%preun
%if 0%{?with_systemd_macros}
%systemd_preun %{_name}.service
%{_sbindir}/userdel -r %{_name} > /dev/null 2>&1
%else
if [ $1 -eq 0 ] ; then
    /sbin/service %{_name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{_name}
    %{_sbindir}/userdel %{_name} > /dev/null 2>&1
fi
%endif

%postun
%if 0%{?with_systemd_macros}
%systemd_postun_with_restart %{_name}.service
%else
if [ "$1" -ge "1" ] ; then
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi
%endif
######################################################################
# END
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
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1/
cp -v docs/man/man1/*.1 $RPM_BUILD_ROOT/%{_mandir}/man1/

%clean
rm -rf $RPM_BUILD_ROOT

######################################################################
# files for 'jsonstats' package
%files
%defattr(-,root,root)
%{python_sitelib}/*
%{_bindir}/%{_name}
%if 0%{?with_systemd_macros}
%{_unitdir}/%{_name}.service
%else
%{_initddir}/%{_name}
%endif
%config(noreplace)/etc/sysconfig/%{_name}
%attr(0755,jsonstatsd,jsonstatsd) %dir %{_localstatedir}/log/%{_name}
%doc %{_mandir}/man1/jsonstatsd*
%doc README.md LICENSE

######################################################################

%changelog
* Mon Aug  4 2014 Chris Murphy <chmurphy@redhat.com> - 1.0.3-4
- Update spec to work with new RHEL 7 and systemd RPM Macros
- Depreciated Fedora 17 and below

* Tue Jul 15 2014 Tim Bielawa <tbielawa@redhat.com> - 1.0.3-3
- Bump for fixes

* Sun Jul  6 2014 Tim Bielawa <tbielawa@redhat.com> - 1.0.3-2
- RPM version includes release string now

* Thu May  8 2014 Tim Bielawa <tbielawa@redhat.com> - 1.0.3-1
- Don't set 'epilog' in option parser on old python boxes

* Thu May  1 2014 Chris Murphy <chmurphy@redhat.com> - 1.0.2-2
- Bumped release because of earlier build conflict

* Thu Apr  3 2014 Tim Bielawa <tbielawa@redhat.com> - 1.0.2-1
- New Plugins: Timestamp
- Better debian compat
- Configurable 'extra plugin' paths
- White/black listing plugins
- Fix init script bug

* Fri Dec 13 2013 Tim Bielawa <tbielawa@redhat.com> - 1.0.1-1
- Bug fixes and useability improvements
- CLI options parsed before plugin loading
- JSON output is sorted
- Facter plugin uses puppet only if available
- Packaging correctly adds/removes jsonstatsd user
- More unit tests

* Wed Nov 27 2013 Tim Bielawa <tbielawa@redhat.com> - 1.0.0-2
- Make log files named consistently

* Wed Nov 20 2013 Tim Bielawa <tbielawa@redhat.com> - 1.0.0-1
- Ready for 1.0.0

* Sun Nov 17 2013 Tim Bielawa <tbielawa@redhat.com> - 0.6.0-1
- Now daemonizes and has proper init scripts

* Mon Nov  4 2013 Tim Bielawa <tbielawa@redhat.com> - 0.5.0-2
- First functional release and RPM distribution.
