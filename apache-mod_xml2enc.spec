#Module-Specific definitions
%define mod_name mod_xml2enc
%define mod_conf A29_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Extended internationalisation support
Name:		apache-%{mod_name}
Version:	1.0.3
Release:	14
Group:		System/Servers
License:	Apache License
URL:		http://apache.webthing.com/mod_xml2enc/
Source0:	http://apache.webthing.com/svn/apache/filters/mod_xml2enc.c
Source1:	http://apache.webthing.com/svn/apache/filters/mod_xml2enc.h
Source2:	README.mod_xml2enc
Source3:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	libxml2-devel
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_xml2enc is a transcoding module that can be used to extend the
internationalisation support of libxml2-based filter modules by converting
encoding before and/or after the filter has run. Thus an unsupported input
charset can be converted to UTF-8, and output can also be converted to another
charset if required.

%package	devel
Summary:	Development API for the mod_xml2enc apache module
Group:		Development/C

%description	devel
mod_xml2enc is a transcoding module that can be used to extend the
internationalisation support of libxml2-based filter modules by converting
encoding before and/or after the filter has run. Thus an unsupported input
charset can be converted to UTF-8, and output can also be converted to another
charset if required.

This package contains the development API for the mod_xml2enc apache module.

%prep

%setup -q -c -T -n %{mod_name}-%{version}

cp %{SOURCE0} .
cp %{SOURCE1} .
cp %{SOURCE2} README.mod_xml2enc
cp %{SOURCE3} %{mod_conf}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

head -40 %{mod_name}.c > LICENCE

%build
%{_bindir}/apxs `xml2-config --cflags` `xml2-config --libs` %{ldflags} -c %{mod_name}.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_includedir}
install -m0644 mod_xml2enc.h %{buildroot}%{_includedir}/

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
 %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
 if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
 fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.mod_xml2enc LICENCE
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}

%files devel
%defattr(-,root,root)
%attr(0644,root,root) %{_includedir}/mod_xml2enc.h


%changelog
* Sat May 14 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-5mdv2011.0
+ Revision: 674432
- rebuild

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-4
+ Revision: 662781
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-3mdv2011.0
+ Revision: 588286
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-2mdv2010.1
+ Revision: 515841
- rebuilt for apache-2.2.15

* Sun Dec 27 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-1mdv2010.1
+ Revision: 482832
- 1.0.3

* Sun Oct 25 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-1mdv2010.0
+ Revision: 459195
- import apache-mod_xml2enc


* Sun Oct 25 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-1mdv2010.0
- initial Mandriva package
