#
# Conditional build:
%bcond_without	apidocs		# valadoc/devhelp based API documentation
%bcond_without	static_libs	# static library
%bcond_without	fep		# fep client

Summary:	Library to deal with Japanese kana-to-kanji conversion method
Summary(pl.UTF-8):	Biblioteka obsługi metody konwersji tekstu japońskiego kana do kanji
Name:		libskk
Version:	1.0.5
Release:	2
License:	GPL v3+
Group:		Libraries
#Source0Download: https://github.com/ueno/libskk/releases
Source0:	https://github.com/ueno/libskk/releases/download/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	683c5a2dd23171297132453afd62e3c4
Patch0:		%{name}-valadoc.patch
URL:		https://github.com/ueno/libskk/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11.1
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.36
BuildRequires:	gobject-introspection-devel >= 0.9.0
BuildRequires:	json-glib-devel
BuildRequires:	libgee-devel >= 0.8
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
# not needed for releases
#BuildRequires:	vala >= 2:0.14.0
%{?with_apidocs:BuildRequires:	valadoc >= 2:0.52}
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libxkbcommon-devel
BuildRequires:	xz
%if %{with fep}
BuildRequires:	libfep-devel >= 0.0.7
BuildRequires:	vala-libfep >= 0.0.7
%endif
BuildRequires:	vala-libgee >= 0.8
Requires:	glib2 >= 1:2.36
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libskk is a library to deal with Japanese kana-to-kanji conversion
method.

%description -l pl.UTF-8
libskk to biblioteka do obsługi metody konwersji tekstu japońśkiego
kana do kanji.

%package fep
Summary:	skkfep - Japanese SKK input method on text terminal
Summary(pl.UTF-8):	skkfep - metoda wprowadzania znaków japońskich SKK z terminala tekstowego
Group:		Applications/Text
Requires:	%{name} = %{version}-%{release}
Requires:	libfep >= 0.0.7

%description fep
skkfep is a tool that allows to use Japanese input method called SKK
(Simple Kana to Kanji conversion program) on ANSI compliant text
terminals.

%description fep -l pl.UTF-8
skkfep to narzędzie pozwalające na używanie metody wprowadzania znaków
japońskich SKK (Simple Kana to Kanji - konwersja uproszczonego kana do
kanji) na terminalach tekstowych zgodnych z ANSI.

%package devel
Summary:	Header files for libskk library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libskk
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.36
Requires:	json-glib-devel
Requires:	libgee-devel >= 0.8

%description devel
Header files for libskk library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libskk.

%package static
Summary:	Static libskk library
Summary(pl.UTF-8):	Statyczna biblioteka libskk
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libskk library.

%description static -l pl.UTF-8
Statyczna biblioteka libskk.

%package -n vala-libskk
Summary:	Vala API for libskk library
Summary(pl.UTF-8):	API języka Vala do biblioteki libskk
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.14.0
Requires:	vala-libgee >= 0.8
BuildArch:	noarch

%description -n vala-libskk
Vala API for libskk library.

%description -n vala-libskk -l pl.UTF-8
API języka Vala do biblioteki libskk.

%package apidocs
Summary:	libskk API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libskk
Group:		Documentation
BuildArch:	noarch

%description apidocs
API and internal documentation for libskk library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libskk.

%prep
%setup -q
%patch0 -p1

%build
# pass fake VALADOC_* args to avoid requiring valadoc-devel
# (only utility is needed here, but configure checks for development package)
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	VALADOC_CFLAGS=fake \
	VALADOC_LIBS=fake \
	%{?with_apidocs:--enable-docs} \
	%{?with_fep:--enable-fep} \
	%{?with_static_libs:--enable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	libskkgtkdocdir=%{_gtkdocdir}/libskk

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libskk.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/skk
%attr(755,root,root) %{_libdir}/libskk.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libskk.so.0
%{_libdir}/girepository-1.0/Skk-1.0.typelib
%{_datadir}/libskk
%{_mandir}/man1/skk.1*

%if %{with fep}
%files fep
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/skkfep
%attr(755,root,root) %{_libexecdir}/skkfep-client
%{_mandir}/man1/skkfep.1*
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libskk.so
%{_datadir}/gir-1.0/Skk-1.0.gir
%{_includedir}/libskk
%{_pkgconfigdir}/libskk.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libskk.a
%endif

%files -n vala-libskk
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/skk-1.0.deps
%{_datadir}/vala/vapi/skk-1.0.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libskk
# should it be here?
%{_datadir}/devhelp/references/libskk
%endif
