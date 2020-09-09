%define debug_package %{nil}

Name: ea-modsec30-connector-apache24
Summary: Apache 2.4 connector for ModSecurity v3.0
# the path in %setup needs manually updated since it has a hyphen, should go away once its not alpha/beta
Version: 0.0.9beta1
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4544 for more details
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
Vendor: cPanel, Inc.
Group: System Environment/Libraries
License: Apache v2
URL: https://github.com/SpiderLabs/ModSecurity-apache

Source0: %{version}.tar.gz
# TODO: Source1: ngx_http_modsecurity_module.conf
# TODO: Source2: modsec30.conf
# TODO: Source3: modsec30.cpanel.conf
# TODO: Source4: modsec30.cpanel.conf-generate
# TODO: Source5: modsec30.cpanel.conf.tt
# TODO: Source6: modsec30.user.conf

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReq:   no

BuildRequires: ea-modsec30

Requires: ea-modsec30
# TODO: this was for config gen: Requires: ea-nginx >= 1.19.1-9

%description

The ModSecurity-apache connector is the connection point between
 Apache 2.4 and libmodsecurity (ModSecurity v3).

%prep
%setup -q -n ModSecurity-apache-0.0.9-beta1

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/opt/cpanel/ea-modsec30-connector-apache24
# TODO: mkdir -p $RPM_BUILD_ROOT/etc/nginx/conf.d/modules

mkdir -p $RPM_BUILD_ROOT/etc/nginx/conf.d/modsec_vendor_configs
mkdir -p $RPM_BUILD_ROOT/var/log/nginx/modsec30_audit

/bin/cp -rf ./* $RPM_BUILD_ROOT/opt/cpanel/ea-modsec30-connector-apache24
# TODO: /bin/cp -rf %{SOURCE1} $RPM_BUILD_ROOT/etc/nginx/conf.d/modules/ngx_http_modsecurity_module.conf

# TODO: mkdir -p $RPM_BUILD_ROOT/etc/nginx/conf.d/modsec
# TODO: mkdir -p $RPM_BUILD_ROOT/etc/nginx/ea-nginx/config-scripts/global/
# TODO: /bin/cp -rf %{SOURCE2} $RPM_BUILD_ROOT/etc/nginx/conf.d/modsec30.conf
# TODO: /bin/cp -rf %{SOURCE3} $RPM_BUILD_ROOT/etc/nginx/conf.d/modsec/modsec30.cpanel.conf
# TODO: /bin/cp -rf %{SOURCE4} $RPM_BUILD_ROOT/etc/nginx/ea-nginx/config-scripts/global/modsec30.cpanel.conf-generate
# TODO: /bin/cp -rf %{SOURCE5} $RPM_BUILD_ROOT/etc/nginx/ea-nginx/modsec30.cpanel.conf.tt
# TODO: /bin/cp -rf %{SOURCE6} $RPM_BUILD_ROOT/etc/nginx/conf.d/modsec/modsec30.user.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post

# TODO: /etc/nginx/ea-apache24/config-scripts/global/modsec30.cpanel.conf-generate

%files
%defattr(-, root, root, -)
/opt/cpanel/ea-modsec30-connector-apache24
# TODO: /etc/nginx/conf.d/modules/ngx_http_modsecurity_module.conf
%attr(0755 root root) %dir /etc/apache2/conf.d/modsec_vendor_configs
%attr(1733 root root) %dir /var/log/apache2/modsec30_audit

# Don't make modsec30.conf a config file, we need to ensure we own this and can fix as needed
# TODO: %attr(0600,root,root) /etc/apache2/conf.d/modsec30.conf
# TODO: %attr(0600,root,root) %config(noreplace) /etc/apache2/conf.d/modsec/modsec30.cpanel.conf
# TODO: %attr(0755 root root) /etc/nginx/ea-nginx/config-scripts/global/modsec30.cpanel.conf-generate
# TODO: /etc/nginx/ea-nginx/modsec30.cpanel.conf.tt
# TODO: %attr(0600,root,root) %config(noreplace) /etc/nginx/conf.d/modsec/modsec30.user.conf

%changelog
* Tue Aug 18 2020 Daniel Muey <dan@cpanel.net> - 0.0.9beta1-1
- ZC-7367: initial release

