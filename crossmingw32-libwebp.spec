Summary:	WebP image codec libraries - cross MinGW32 version
Summary(pl.UTF-8):	Biblioteki do kodeka obrazów WebP - wersja skrośna MinGW32
Name:		crossmingw32-libwebp
Version:	0.3.1
Release:	1
License:	BSD
Group:		Development/Libraries
#Source0Download: http://code.google.com/p/webp/downloads/list
Source0:	http://webp.googlecode.com/files/libwebp-%{version}.tar.gz
# Source0-md5:	dc862bb4006d819b7587767a9e83d31f
URL:		https://developers.google.com/speed/webp/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	crossmingw32-gcc
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++
%define		__pkgconfig_provides	%{nil}
%define		__pkgconfig_requires	%{nil}

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker, most of -f options are Linux-specific
%define		filterout_ld	-Wl,-z,.*
%define		filterout_c	-f[-a-z0-9=]*

%description
WebP image codec libraries.

This package contains the cross version for Win32.

%description -l pl.UTF-8
Biblioteki kodeka obrazów WebP.

Ten pakiet zawiera wersję skrośną dla Win32.

%package static
Summary:	Static WebP libraries (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczne biblioteki WebP (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static WebP libraries (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczne biblioteki WebP (wersja skrośna MinGW32).

%package dll
Summary:	DLL WebP libraries for Windows
Summary(pl.UTF-8):	Biblioteki DLL WebP dla Windows
Group:		Applications/Emulators
Requires:	wine

%description dll
DLL WebP libraries for Windows.

%description dll -l pl.UTF-8
Biblioteki DLL WebP dla Windows.

%prep
%setup -q -n libwebp-%{version}

sed -i -e 's/libwebp_la_LDFLAGS.*/& -no-undefined/' src/Makefile.am

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--target=%{target} \
	--host=%{target} \
	--disable-silent-rules \
	--enable-libwebpdemux \
	--enable-libwebpmux

# -C src to get just the library, no utils
%{__make} -C src

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C src install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS PATENTS README
%{_libdir}/libwebp.dll.a
%{_libdir}/libwebp.la
%{_libdir}/libwebpdemux.dll.a
%{_libdir}/libwebpdemux.la
%{_libdir}/libwebpmux.dll.a
%{_libdir}/libwebpmux.la
%{_includedir}/webp
%{_pkgconfigdir}/libwebp.pc
%{_pkgconfigdir}/libwebpdemux.pc
%{_pkgconfigdir}/libwebpmux.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libwebp.a
%{_libdir}/libwebpdemux.a
%{_libdir}/libwebpmux.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libwebp-4.dll
%{_dlldir}/libwebpmux-0.dll
%{_dlldir}/libwebpdemux-0.dll
