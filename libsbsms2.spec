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
Version:	2.3.0
Release:	1
License:	GPL v2
Group:		Libraries
#Source0Download: https://github.com/claytonotey/releases
Source0:	https://github.com/claytonotey/libsbsms/archive/%{version}/libsbsms-%{version}.tar.gz
# Source0-md5:	06df56b8c360af07ed57436fb02ec5dc
Patch0:		libsbsms-opts.patch
Patch1:		libsbsms-gcc.patch
Patch2:		libsbsms-link.patch
Patch3:		libsbsms-pthread.patch
URL:		https://github.com/claytonotey/libsbsms
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1.5
BuildRequires:	libmad-devel
BuildRequires:	libsndfile-devel >= 1.0.2
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
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

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md TODO
%attr(755,root,root) %{_libdir}/libsbsms.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsbsms.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsbsms.so
%{_libdir}/libsbsms.la
%{_includedir}/sbsms.h
%{_pkgconfigdir}/sbsms.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libsbsms.a
