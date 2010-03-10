%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}
%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_version  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP Version => //p') | tail -1)

%define pecl_name memcache-zynga
%define module_name memcache

Summary:      Memcached extension with custom changes for zynga
Name:         php-pecl-memcache-zynga
Version:      2.2.6.0
Release:      %{?php_version}
License:      PHP
Group:        Development/Languages
URL:          http://pecl.php.net/package/%{pecl_name}

Source:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

Source2:      xml2changelog

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-devel >= 4.3.11, php-pear, zlib-devel
Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Provides:     php-pecl(%{pecl_name}) = %{version}-%{release}
%if %{?php_zend_api}0
Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}
%else
Requires:     php-api = %{php_apiver}
%endif
Requires:     php >= %{php_version}
Conflicts:    php-pecl(memcache)

%description
Memcached is a caching daemon designed especially for
dynamic web applications to decrease database load by
storing objects in memory.

This extension allows you to work with memcached through
handy OO and procedural interfaces.

Zynga customization - proxy support added

Memcache can be used as a PHP session handler.

%prep 
%setup -c -q
%{_bindir}/php -n %{SOURCE2} package.xml >CHANGELOG

# avoid spurious-executable-perm
find . -type f -exec chmod -x {} \;


%build
cd %{pecl_name}-%{version}
phpize
chmod +x ./configure
%configure
%{__make} %{?_smp_mflags}


%install
cd %{pecl_name}-%{version}
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{module_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{module_name}.so

; Options for the %{module_name} module

; Whether to transparently failover to other servers on errors
;memcache.allow_failover=1
; Defines how many servers to try when setting and getting data.
;memcache.max_failover_attempts=20
; Data will be transferred in chunks of this size
;memcache.chunk_size=8192
; The default TCP port number to use when connecting to the memcached server 
;memcache.default_port=11211
; Hash function {crc32, fnv}
;memcache.hash_function=crc32
; Hash strategy {standard, consistent}
;memcache.hash_strategy=standard

; Options for enabling proxy

; Enables/disabled proxy support
;memcache.proxy_enabled=false
; Proxy host/ip. For unix domain sockets, use unix://<abs path to socket>
;memcache.proxy_host=localhost
; Proxy port. For unix domain sockets, give 0 
;memcache.proxy_port=0

; Compression level - ignored unless compression threshold is set on the memcache pool
; 0: use LZO compression
; 1 - 9: use Zlib compression
;memcache.compression_level=0

; Options to use the memcache session handler

; Use memcache as a session handler
;session.save_handler=memcache
; Defines a comma separated of server urls to use for session storage
;session.save_path="tcp://localhost:11211?persistent=1&weight=1&timeout=1&retry_interval=15"
; Option to enable the number of retries on a persistent connection
;memcache.connection_retry_count=0
EOF

# Install XML package description
# use 'name' rather than 'pecl_name' to avoid conflict with pear extensions
%{__mkdir_p} %{buildroot}%{pecl_xmldir}
#%{__install} -m 644 ../package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml
%{__install} -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%clean
%{__rm} -rf %{buildroot}


%if 0%{?pecl_install:1}
%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
%endif


%if 0%{?pecl_uninstall:1}
%postun
if [ $1 -eq 0 -a -x %{__pecl} ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%files
%defattr(-, root, root, -)
%doc CHANGELOG %{pecl_name}-%{version}/CREDITS %{pecl_name}-%{version}/README 
%doc %{pecl_name}-%{version}/example.php %{pecl_name}-%{version}/memcache.php
%config(noreplace) %{_sysconfdir}/php.d/%{module_name}.ini
%{php_extdir}/%{module_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Wed Mar 10 2010 Jayesh Jose <jjose@zynga.com> 2.2.6.0-1
- Adding LZO compression support

* Thu Feb 25 2010 Prashun Purkayastha <ppurkayastha@zynga.com> 2.2.5.5-1
- Added a display message for the NOT_FOUND error

* Tue Feb 16 2010 Prashun Purkayastha <ppurkayastha@zynga.com> 2.2.5.4-1
- Added INI_SET option to retry with "memcache.connection_retry_count" on a 
- failed set or get operation on a persistent connection

* Wed Nov 18 2009 Jayesh Jose <jjose@zynga.com> 2.2.5.3-1
- Disabled fall back to direct mc connection 

* Thu Oct 29 2009 Jayesh Jose <jjose@zynga.com> 2.2.5-1
- Zynga version with proxy support

* Sat Feb 28 2009 Remi Collet <Fedora@FamilleCollet.com> 2.2.5-1
- new version 2.2.5 (bug fixes)

* Fri Sep 11 2008 Remi Collet <Fedora@FamilleCollet.com> 2.2.4-1
- new version 2.2.4 (bug fixes)

* Sat Feb  9 2008 Remi Collet <Fedora@FamilleCollet.com> 2.2.3-1
- new version

* Thu Jan 10 2008 Remi Collet <Fedora@FamilleCollet.com> 2.2.2-1
- new version

* Thu Nov 01 2007 Remi Collet <Fedora@FamilleCollet.com> 2.2.1-1
- new version

* Sat Sep 22 2007 Remi Collet <Fedora@FamilleCollet.com> 2.2.0-1
- new version
- add new INI directives (hash_strategy + hash_function) to config
- add BR on php-devel >= 4.3.11 

* Mon Aug 20 2007 Remi Collet <Fedora@FamilleCollet.com> 2.1.2-1
- initial RPM

