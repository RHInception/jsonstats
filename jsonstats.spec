%if 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
%endif

Name:          jsonstats
Release:       2%{?dist}
Summary:       Client for exposing system information over a REST interface
Version:       0.5.0

Group:         Development/Libraries
License:       MIT
Source0:       %{name}-%{version}.tar.gz
Url:           https://github.com/tbielawa/restfulstatsjson

BuildArch:     noarch
BuildRequires: python2-devel

%description
A simple REST client which exposes provides arbitrary system
information ('facts'). The fact providing system is plugin
based. Exposing additional facts is as simple as returning a
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

######################################################################
# files for 'jsonstats' package
%files
%defattr(-,root,root)
%{python_sitelib}/jsonstats
%{_bindir}/jsonstats


######################################################################
%changelog
* Mon Nov  4 2013 Tim Bielawa <tbielawa@redhat.com> - 0.5.0-2
- First functional release and RPM distribution.
