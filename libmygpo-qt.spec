#
# Conditional build:
%bcond_without	qt4	# Qt4 based library
%bcond_without	qt5	# Qt5 based library
%bcond_without	tests	# build without tests

Summary:	Qt4 library that wraps the gpodder.net Web API
Summary(pl.UTF-8):	Biblioteka Qt4 obudowująca API WWW gpodder.net
Name:		libmygpo-qt
Version:	1.0.9
Release:	2
License:	LGPL v2+
Source0:	http://stefan.derkits.at/files/libmygpo-qt/%{name}.%{version}.tar.gz
# Source0-md5:	aead5b0c6707f3e2bd2259cb1db2b7cd
Patch1:		fix-test.patch
Group:		Libraries
URL:		http://wiki.gpodder.org/wiki/Libmygpo-qt
BuildRequires:	cmake >= 2.8.9
BuildRequires:	doxygen
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
%if %{with qt4}
BuildRequires:	QtCore-devel >= 4.6
BuildRequires:	QtNetwork-devel >= 4.6
BuildRequires:	QtTest-devel >= 4.6
BuildRequires:	qjson-devel
BuildRequires:	qt4-build >= 4.6
%endif
%if %{with qt5}
BuildRequires:	Qt5Core-devel >= 5.2
BuildRequires:	Qt5Network-devel >= 5.2
BuildRequires:	Qt5Test-devel >= 5.2
BuildRequires:	qt5-build >= 5.2
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libmygpo-qt is a Qt Library that wraps the gpodder.net Web API,
<http://gpoddernet.readthedocs.io/>.

%description -l pl.UTF-8
libmygpo-qt to biblioteka Qt obudowująca API WWW gpodder.net:
<http://gpoddernet.readthedocs.io/>.

%package devel
Summary:	Development files for Qt4 %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Qt4 %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	QtCore-devel >= 4.6
Requires:	QtNetwork-devel >= 4.6
Requires:	libstdc++-devel
Requires:	qjson-devel

%description devel
Development files for Qt4 %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt4 %{name}.

%package -n libmygpo-qt5
Summary:	Qt5 library that wraps the gpodder.net Web API
Summary(pl.UTF-8):	Biblioteka Qt5 obudowująca API WWW gpodder.net
Group:		Libraries

%description -n libmygpo-qt5
libmygpo-qt is a Qt Library that wraps the gpodder.net Web API,
<http://gpoddernet.readthedocs.io/>.

%description -n libmygpo-qt5 -l pl.UTF-8
libmygpo-qt to biblioteka Qt obudowująca API WWW gpodder.net:
<http://gpoddernet.readthedocs.io/>.

%package -n libmygpo-qt5-devel
Summary:	Development files for Qt5 %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Qt5 %{name}
Group:		Development/Libraries
Requires:	Qt5Core-devel >= 5.2
Requires:	Qt5Network-devel >= 5.2
Requires:	libmygpo-qt5 = %{version}-%{release}
Requires:	libstdc++-devel

%description -n libmygpo-qt5-devel
Development files for Qt5 %{name} library.

%description -n libmygpo-qt5-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt5 %{name}.

%prep
%setup -q -n %{name}.%{version}
%patch -P1 -p1

%build
%if %{with qt4}
install -d build-qt4
cd build-qt4
%cmake .. \
	-DBUILD_WITH_QT4=ON
%{__make}

%if %{with tests}
export CTEST_OUTPUT_ON_FAILURE=1
%{__make} test
%endif
cd ..
%endif

%if %{with qt5}
install -d build-qt5
cd build-qt5
%cmake .. \
	-DBUILD_WITH_QT4=OFF
%{__make}

%if %{with tests}
export CTEST_OUTPUT_ON_FAILURE=1
%{__make} test
%endif
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with qt4}
%{__make} -C build-qt4 install/fast \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%if %{with qt5}
%{__make} -C build-qt5 install/fast \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n libmygpo-qt5 -p /sbin/ldconfig
%postun	-n libmygpo-qt5 -p /sbin/ldconfig

%if %{with qt4}
%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/libmygpo-qt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmygpo-qt.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmygpo-qt.so
%{_includedir}/mygpo-qt
%{_pkgconfigdir}/libmygpo-qt.pc
%dir %{_libdir}/cmake/mygpo-qt
%{_libdir}/cmake/mygpo-qt/Mygpo-qtConfig*.cmake
%{_libdir}/cmake/mygpo-qt/Mygpo-qtTargets*.cmake
%endif

%if %{with qt5}
%files -n libmygpo-qt5
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/libmygpo-qt5.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmygpo-qt5.so.1

%files -n libmygpo-qt5-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmygpo-qt5.so
%{_includedir}/mygpo-qt5
%{_pkgconfigdir}/libmygpo-qt5.pc
%dir %{_libdir}/cmake/mygpo-qt
%{_libdir}/cmake/mygpo-qt/Mygpo-qt5Config*.cmake
%{_libdir}/cmake/mygpo-qt/Mygpo-qt5Targets*.cmake
%endif
