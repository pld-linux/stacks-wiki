Summary:	Stack's Wiki - a lightweight wiki system
Summary(pl):	Stack's Wiki - lekki system wiki
Name:		stacks-wiki
Version:	0.5.1
Release:	0.3
License:	GPL
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/stacks-wiki/%{name}-%{version}.tar.bz2
# Source0-md5:	3027b0286d47742f6782c0ead784a138
Patch0:		%{name}.patch
URL:		http://www.shortround.net/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	php
Requires:	php-mysql
Requires:	webapps
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
Stack's Wiki is a light weight wiki system. It uses PHP and MySQL like
most sites, but also uses AJAX for content management. It also uses
Markdown for the raw content.

%description -l pl
Stack's Wiki to lekki system wiki. U¿ywa PHP i MySQL podobnie jak
wiêkszo¶æ serwisów, ale u¿ywa tak¿e technologii AJAX do zarz±dzania
tre¶ci±. U¿ywa tak¿e Markdown do surowej tre¶ci.

%prep
%setup -q
%patch0 -p1

cat >apache.conf <<'EOF'
Alias /%{name} %{_datadir}/%{name}
<Directory %{_datadir}/%{name}>
	Allow from all
</Directory>
EOF

cat >README.PLD <<'EOF'
To create database invoke:
mysqladmin create stacks-wiki
mysql> GRANT SELECT,INSERT,UPDATE,DELETE ON `stacks-wiki`.* TO 'wiki'@localhost IDENTIFIED BY 'wiki';
zcat %{_docdir}/%{name}-%{version}/schema.sql.gz | mysql stacks-wiki
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}
cp -a www/* $RPM_BUILD_ROOT%{_appdir}
cp -a db.php $RPM_BUILD_ROOT%{_sysconfdir}/db.php

install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1
%webapp_register apache %{_webapp}

%triggerun -- apache1
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc CHANGELOG README README.PLD schema.sql
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%{_appdir}
