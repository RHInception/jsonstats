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
BuildRequires:   python2-devel

######################################################
######################################################
# http://fedoraproject.org/wiki/Packaging:ScriptletSnippets#Macroized_scriptlets_.28Fedora_18.2B.29
Requires(post):  systemd
Requires(preun): systemd
Requires(postun):systemd
BuildRequires:   systemd

%post
%systemd_post %{_name}.service

%preun
%systemd_preun %{_name}.service

%postun
%systemd_postun_with_restart %{_name}.service



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

%clean
rm -rf $RPM_BUILD_ROOT


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


%config(noreplace)/etc/sysconfig/%{_name}
%{_unitdir}/%{_name}.service
######################################################################
%changelog
* Mon Nov  4 2013 Tim Bielawa <tbielawa@redhat.com> - 0.5.0-2
- First functional release and RPM distribution.
