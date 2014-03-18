Summary:	Provide online accounts information
Name:		gnome-online-accounts
Version:	3.10.3
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-online-accounts/3.10/%{name}-%{version}.tar.xz
# Source0-md5:	37627e71bf5098b59947b8e1529b3991
URL:		http://www.gnome.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gobject-introspection-devel >= 1.38.0
BuildRequires:	gtk-doc
BuildRequires:	gtk+3-webkit-devel >= 2.2.0
BuildRequires:	intltool
BuildRequires:	json-glib-devel
BuildRequires:	libgnome-keyring-devel
BuildRequires:	libnotify-devel
BuildRequires:	libsoup-gnome-devel
BuildRequires:	rest-devel >= 0.7.90
Requires:	%{name}-libs = %{version}-%{release}
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir		%{_libdir}/%{name}
%define		skip_post_check_so	libgoa-backend-1.0.so.*

%description
gnome-online-accounts provides interfaces so applications and
libraries in GNOME can access the user's online accounts.

%package libs
Summary:	GOA libraries
Group:		Libraries

%description libs
GOA libraries.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
The gnome-online-accounts-devel package contains libraries and header
files for developing applications that use gnome-online-accounts.

%package apidocs
Summary:	GOA API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
GOA API documentation.

%prep
%setup -q

# kill gnome common deps
%{__sed} -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.ac

%build
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules	\
	--disable-static	\
	--enable-facebook	\
	--enable-google		\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang gnome-online-accounts --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%post   libs -p /usr/sbin/ldconfig
%postun libs -p /usr/sbin/ldconfig

%files -f gnome-online-accounts.lang
%defattr(644,root,root,755)
%doc NEWS COPYING
%dir %{_libexecdir}
%attr(755,root,root) %{_libexecdir}/goa-daemon
%{_datadir}/dbus-1/services/org.gnome.OnlineAccounts.service
%{_datadir}/gnome-online-accounts
%{_iconsdir}/hicolor/*/apps/*.png
%{_iconsdir}/hicolor/*/apps/*.svg
%{_mandir}/man8/goa-daemon.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libgoa-1.0.so.?
%attr(755,root,root) %ghost %{_libdir}/libgoa-backend-1.0.so.?
%attr(755,root,root) %{_libdir}/libgoa-1.0.so.*.*.*
%attr(755,root,root) %{_libdir}/libgoa-backend-1.0.so.*.*.*
%{_libdir}/girepository-1.0/Goa-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgoa-1.0.so
%attr(755,root,root) %{_libdir}/libgoa-backend-1.0.so
%dir %{_libdir}/goa-1.0
%dir %{_libdir}/goa-1.0/include
%{_libdir}/goa-1.0/include/goaconfig.h
%{_includedir}/goa-1.0
%{_datadir}/gir-1.0/Goa-1.0.gir
%{_pkgconfigdir}/goa-1.0.pc
%{_pkgconfigdir}/goa-backend-1.0.pc

%if 0
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/goa
%endif

