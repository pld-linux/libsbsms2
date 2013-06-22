#
# Conditional build:
%bcond_with	sse	# use SSE optimizations
#
%ifarch pentium3 pentium4 %{x8664}
%define	with_sse	1
%endif
Summary:	C++ library for high quality time stretching and pitch scaling
Summary(pl.UTF-8):	Biblioteka C++ do wysokiej jakości zmiany szybkości i wysokości dźwięku
Name:		libsbsms2
Version:	2.0.1
Release:	1
License:	GPL v2
Group:		Libraries
Source0:	http://downloads.sourceforge.net/sbsms/libsbsms-%{version}.tar.gz
# Source0-md5:	409fb6f4f64e48ff1a7bc18621b952fb
Patch0:		libsbsms-opts.patch
Patch1:		libsbsms-gcc.patch
Patch2:		libsbsms-link.patch
Patch3:		libsbsms-am.patch
URL:		http://sbsms.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake >= 1.5
BuildRequires:	libmad-devel
BuildRequires:	libsndfile-devel >= 1.0.2
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
# because of sbsms tool
Conflicts:	libsbsms < 2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libsbsms is a library for high quality time and pitch scale
modification. It uses octave subband sinusoidal modeling.

%description -l pl.UTF-8
libsbsms to biblioteka do wysokiej jakości modyfikowania szybkości i
wysokości dźwięku. Wykorzystuje modelowanie sinusoidalne.

%package devel
Summary:	Header files for libsbsms 2 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libsbsms 2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel
Conflicts:	libsbsms-devel < 2

%description devel
Header files for libsbsms 2 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libsbsms 2.

%package static
Summary:	Static libsbsms 2 library
Summary(pl.UTF-8):	Statyczna biblioteka libsbsms 2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Conflicts:	libsbsms-static < 2

%description static
Static libsbsms 2 library.

%description static -l pl.UTF-8
Statyczna biblioteka libsbsms 2.

%prep
%setup -q -n libsbsms-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-multithreaded \
	--enable-shared \
	%{!?with-sse:--disable-sse}
%{__make}

cd test
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	SBSMS_CFLAGS="-I$(pwd)/../include" \
	SBSMS_LIBS="-L$(pwd)/../src/.libs -lsbsms" \
	--enable-shared
	
%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C test install \
	DESTDIR=$RPM_BUILD_ROOT

%{__sed} -i -e 's,-L[^ "]*/\.libs *,,g' $RPM_BUILD_ROOT%{_libdir}/libsbsmsx.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README TODO
%attr(755,root,root) %{_bindir}/sbsms
%attr(755,root,root) %{_libdir}/libsbsms.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsbsms.so.0
%attr(755,root,root) %{_libdir}/libsbsmsx.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsbsmsx.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsbsms.so
%attr(755,root,root) %{_libdir}/libsbsmsx.so
%{_libdir}/libsbsms.la
%{_libdir}/libsbsmsx.la
%{_includedir}/sbsms.h
%{_pkgconfigdir}/sbsms.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libsbsms.a
%{_libdir}/libsbsmsx.a
