Name:           mod_auth_gssapi
Version:        1.3.1
Release:        3%{?dist}
Summary:        A GSSAPI Authentication module for Apache

Group:          System Environment/Daemons
License:        MIT
URL:            https://github.com/modauthgssapi/mod_auth_gssapi
Source0:        https://github.com/modauthgssapi/%{name}/releases/download/v%{version}/%name-%{version}.tar.gz

Patch0:         0001-Implement-unique-ccache-names.patch
Patch1:         0002-Fix-cred-cache-detection.patch
Patch2:         Fix-backport.patch

BuildRequires:  httpd-devel, krb5-devel, openssl-devel, autoconf, automake, libtool
Requires:       httpd-mmn = %{_httpd_mmn}
Requires:       krb5-libs >= 1.11.5

%description
The mod_auth_gssapi module is an authentication service that implements the
SPNEGO based HTTP Authentication protocol defined in RFC4559.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
export APXS=%{_httpd_apxs}
autoreconf -fi
%configure
make %{?_smp_mflags}


%install
mkdir -p %{buildroot}%{_httpd_moddir}
install -m 755 src/.libs/%{name}.so %{buildroot}%{_httpd_moddir}

# Apache configuration for the module
echo "LoadModule auth_gssapi_module modules/mod_auth_gssapi.so" > 10-auth_gssapi.conf
mkdir -p %{buildroot}%{_httpd_modconfdir}
install -m 644 10-auth_gssapi.conf %{buildroot}%{_httpd_modconfdir}

%files
%doc
%defattr(-,root,root)
%doc README COPYING
%config(noreplace) %{_httpd_modconfdir}/10-auth_gssapi.conf
%{_httpd_moddir}/mod_auth_gssapi.so

%changelog
* Thu Jun 30 2016 Simo Sorce <simo@redhat.com> 1.3.1-3
- Fix backport issue
- related: #1347175

* Wed Jun 15 2016 Simo Sorce <simo@redhat.com> 1.3.1-2
- Add Unique ccache support
- resolves: #1347175

* Thu Sep  3 2015 Simo Sorce <simo@redhat.com> 1.3.1-1
- Various bugfixes and minor new features
- resolves: #1258168
- resolves: #1258171
- resolves: #1258172
- resolves: #1258456

* Thu Apr 21 2015 Simo Sorce <simo@redhat.com> 1.2.0-1
- First RHEL release
- resolves: #1205367
