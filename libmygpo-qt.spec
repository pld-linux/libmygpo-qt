#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	Qt Library that wraps the gpodder.net Web API
Name:		libmygpo-qt
Version:	1.0.7
Release:	2
License:	LGPL v2+
Source0:	http://stefan.derkits.at/files/libmygpo-qt/%{name}.%{version}.tar.gz
# Source0-md5:	447e60c8c695b4280a0e20c71abacf49
Group:		Libraries
URL:		http://wiki.gpodder.org/wiki/Libmygpo-qt
BuildRequires:	QtCore-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	QtTest-devel
BuildRequires:	automoc4
BuildRequires:	cmake >= 2.6.2
BuildRequires:	doxygen
BuildRequires:	pkgconfig
BuildRequires:	qjson-devel
BuildRequires:	qt4-build
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libmygpo-qt is a Qt Library that wraps the gpodder.net Web API,
<http://wiki.gpodder.org/wiki/Web_Services/API_2>.

%package devel
Summary:	Development files for %{name}
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
libmygpo-qt is a Qt Library that wraps the gpodder.net Web API,
<http://wiki.gpodder.org/wiki/Web_Services/API_2>.

%prep
%setup -q -n %{name}.%{version}

%build
install -d build
cd build
%cmake ..
%{__make}

%if %{with tests}
export CTEST_OUTPUT_ON_FAILURE=1
%{__make} test
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install/fast -C build \
	DESTDIR=$RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/libmygpo-qt.so.*.*.*
%ghost %{_libdir}/libmygpo-qt.so.1

%files devel
%defattr(644,root,root,755)
%{_includedir}/mygpo-qt
%{_libdir}/libmygpo-qt.so
%{_pkgconfigdir}/libmygpo-qt.pc
%{_libdir}/cmake/mygpo-qt
