%define debug_package %{nil}

Name: ea-modsec30-connector-apache24
Summary: WARNING: cPanel v92 or later ONLY - Apache 2.4 connector for ModSecurity v3.0
# the path in %setup needs manually updated since it has a hyphen, should go away once its not alpha/beta
Version: 0.0.9beta1
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4544 for more details
%define release_prefix 9
Release: %{release_prefix}%{?dist}.cpanel
Vendor: cPanel, Inc.
Group: System Environment/Libraries
License: Apache v2
URL: https://github.com/SpiderLabs/ModSecurity-apache

Source0: %{version}.tar.gz
Source1: 800-mod_security30.conf
Source2: modsec30.conf
Source3: modsec2.cpanel.conf
Source4: modsec2.user.conf

Patch0: 0001-Fix-with-libmodsecurity.patch
Patch1: 0002-Update-to-match-Rules-namechange-to-RulesSet-in-ModS.patch
Patch2: 0003-Send-expected-protocol-formatting-to-msc_process_uri.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReq:   no

BuildRequires: ea-modsec30 ea-apache24-devel
Requires: ea-modsec30

# TODO: ZC-7519
# BuildRequires: ea-libcurl
# BuildRequires: ea-libcurl-devel
# BuildRequires: ea-libxml2[-devel]

BuildRequires: curl
BuildRequires: curl-devel
BuildRequires: GeoIP-devel libxml2 libxml2-devel lzma pcre pcre-devel yajl yajl-devel

%description

The ModSecurity-apache connector is the connection point between
 Apache 2.4 and libmodsecurity (ModSecurity v3).

%prep
%setup -q -n ModSecurity-apache-0.0.9-beta1

%patch0 -p1 -b .fix-with-libmodsecurity
%patch1 -p1 -b .update-for-rules-namechange
%patch2 -p1 -b .protocol-fix

%build

# TODO: ZC-7519
# export LDFLAGS="-L/opt/cpanel/libcurl/lib64/ -L/opt/cpanel/ea-libxml2/lib64/"

./autogen.sh
./configure --with-libmodsecurity=/opt/cpanel/ea-modsec30
make

%install

rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT/etc/apache2/modules
/bin/cp -rf ./src/.libs/mod_security3.so $RPM_BUILD_ROOT/etc/apache2/modules/mod_security3.so

mkdir -p $RPM_BUILD_ROOT/etc/apache2/conf.modules.d
/bin/cp -rf %{SOURCE1} $RPM_BUILD_ROOT/etc/apache2/conf.modules.d/800-mod_security30.conf

# For now, use modsec 2 paths since WHM hardcodes them,
#   details at https://enterprise.cpanel.net/projects/EA4/repos/ea-modsec31/browse/DESIGN.md
mkdir -p $RPM_BUILD_ROOT/etc/apache2/conf.d/modsec_vendor_configs
mkdir -p $RPM_BUILD_ROOT/etc/apache2/conf.d/modsec
mkdir -p $RPM_BUILD_ROOT/var/cpanel/templates/apache2_4
mkdir -p $RPM_BUILD_ROOT/var/log/apache2/modsec_audit
/bin/cp -rf %{SOURCE2} $RPM_BUILD_ROOT/etc/apache2/conf.d/modsec30.conf
/bin/cp -rf %{SOURCE3} $RPM_BUILD_ROOT/etc/apache2/conf.d/modsec/modsec2.cpanel.conf
/bin/cp -rf %{SOURCE4} $RPM_BUILD_ROOT/etc/apache2/conf.d/modsec/modsec2.user.conf

%clean
rm -rf $RPM_BUILD_ROOT

%posttrans

/usr/local/cpanel/3rdparty/bin/perl -MWhostmgr::ModSecurity::ModsecCpanelConf -e 'Whostmgr::ModSecurity::ModsecCpanelConf->new->manipulate(sub {})'

%files
%defattr(-, root, root, -)
/etc/apache2/conf.modules.d/800-mod_security30.conf
%attr(0755 root root) /etc/apache2/modules/mod_security3.so
%attr(0755 root root) %dir /etc/apache2/conf.d/modsec_vendor_configs
%attr(1733 root root) %dir /var/log/apache2/modsec_audit

# Don't make modsec30.conf a config file, we need to ensure we own this and can fix as needed
# For now, use modsec 2 paths since WHM hardcodes them,
#   details at https://enterprise.cpanel.net/projects/EA4/repos/ea-modsec31/browse/DESIGN.md
%attr(0600,root,root) /etc/apache2/conf.d/modsec30.conf
%attr(0600,root,root) %config(noreplace) /etc/apache2/conf.d/modsec/modsec2.cpanel.conf
%attr(0600,root,root) %config(noreplace) /etc/apache2/conf.d/modsec/modsec2.user.conf

%changelog
* Wed Mar 16 2022 Travis Holloway <t.holloway@cpanel.net> - 0.0.9beta1-9
- EA-10429: Add patch to send appropriate protocol modsec30

* Thu Dec 16 2021 Dan Muey <dan@cpanel.net> - 0.0.9beta1-8
- ZC-9203: Update DISABLE_BUILD to match OBS

* Tue Nov 02 2021 Julian Brown <julian.brown@cpanel.net> - 0.0.9beta1-7
- ZC-9451: Move modsec30 template to ea-modsec30

* Thu Oct 21 2021 Travis Holloway <t.holloway@cpanel.net> - 0.0.9beta1-6
- EA-10202: Add patch for rules name change in ModSecurity v3.0.5

* Wed Mar 17 2021 Tim Mullin <tim@cpanel.net> - 0.0.9beta1-5
- EA-9421: Set SecRequestBodyLimitAction to ProcessPartial

* Thu Oct 01 2020 Daniel Muey <dan@cpanel.net> - 0.0.9beta1-4
- ZC-7679: Add v92 warning to summary

* Mon Sep 28 2020 Daniel Muey <dan@cpanel.net> - 0.0.9beta1-3
- ZC-7633: Ensure modsec2.cpanel.conf is built after template is installed

* Thu Sep 10 2020 Daniel Muey <dan@cpanel.net> - 0.0.9beta1-2
- ZC-7444: Remove unsupported `SecGsbLookupDb` and `SecGuardianLog` from config

* Tue Aug 18 2020 Daniel Muey <dan@cpanel.net> - 0.0.9beta1-1
- ZC-7367: initial release

