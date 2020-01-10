Name:           mod_auth_gssapi
Version:        1.5.1
Release:        5%{?dist}
Summary:        A GSSAPI Authentication module for Apache

Group:          System Environment/Daemons
License:        MIT
URL:            https://github.com/modauthgssapi/mod_auth_gssapi
Source0:        https://github.com/modauthgssapi/%{name}/releases/download/v%{version}/%name-%{version}.tar.gz

Patch0: report-file-operation-errors-as-warnings.patch
Patch1: Allow-admins-to-selectively-suppress-negotiation.patch
Patch2: Fix-strtol-error-checking.patch
Patch3: Handle-extra-large-NSS-entries.patch
Patch4: Document-gssapi-no-negotiate.patch

BuildRequires:  httpd-devel, krb5-devel, openssl-devel, autoconf, automake, libtool
Requires:       httpd-mmn = %{_httpd_mmn}
Requires:       krb5-libs >= 1.11.5

%description
The mod_auth_gssapi module is an authentication service that implements the
SPNEGO based HTTP Authentication protocol defined in RFC4559.

%prep
%setup -q
%patch0 -p1 -b .report-file-operation-errors-as-warnings
%patch1 -p1 -b .Allow-admins-to-selectively-suppress-negotiation
%patch2 -p1 -b .Fix-strtol-error-checking
%patch3 -p1 -b .Handle-extra-large-NSS-entries
%patch4 -p1 -b .Document-gssapi-no-negotiate

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
* Fri Oct 27 2017 Robbie Harwood <rharwood@redhat.com> - 1.5.1-5
- Document gssapi-no-negotiate
- Resolves: #1309041

* Wed Oct 04 2017 Robbie Harwood <rharwood@redhat.com> - 1.5.1-4
- Handle large NSS entries (>1024)
- Resolves: #1498176

* Mon Oct 02 2017 Robbie Harwood <rharwood@redhat.com> - 1.5.1-3
- Allow admins to suppress negotiation selectively
- Resolves: #1309041

* Mon Mar 27 2017 Simo Sorce <simo@redhat.com> - 1.5.1-2
- Fix log level on some messages
- resolves: #1433362

* Thu Mar  9 2017 Simo Sorce <simo@redhat.com> - 1.5.1-1
- Korabl-Sputnik 4 launch (1.5.1)
- resolves: #1403194

* Tue Jun 21 2016 Simo Sorce <simo@redhat.com> 1.4.0-1
- Lunar Reconnaissance Orbiter (2009) release (1.4.0)
- resolves: #1346883
- resolves: #1343422

* Thu Sep  3 2015 Simo Sorce <simo@redhat.com> 1.3.1-1
- Various bugfixes and minor new features
- resolves: #1258168
- resolves: #1258171
- resolves: #1258172
- resolves: #1258456

* Wed Apr 29 2015 Simo Sorce <simo@redhat.com> 1.2.0-1
- First RHEL release
- resolves: #1205367
