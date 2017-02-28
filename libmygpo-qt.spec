#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	Qt Library that wraps the gpodder.net Web API
Name:		libmygpo-qt
Version:	1.0.8
Release:	3
License:	LGPL v2+
Source0:	http://stefan.derkits.at/files/libmygpo-qt/%{name}.%{version}.tar.gz
# Source0-md5:	cb67c86919171d6d2356dfb59c3b9571
Patch0:		https://github.com/gpodder/libmygpo-qt/compare/1.0.8...master.patch
# Patch0-md5:	cf716711e999823c9941861a18c19fc2
Patch1:		fix-test.patch
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
<http://gpoddernet.readthedocs.io/>.

%package devel
Summary:	Development files for %{name}
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
libmygpo-qt is a Qt Library that wraps the gpodder.net Web API,
<http://gpoddernet.readthedocs.io/>.

%prep
%setup -q -n %{name}.%{version}
%patch0 -p1
%patch1 -p1

grep '^From ' %{PATCH0}

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
