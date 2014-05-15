%define upstream_name pycairo
%define package_name py3cairo
%define source_subtree %{upstream_name}-%{version}
%define python_version python3

Name:		%{python_version}-cairo
Version:	1.10.0
Release:	1
Summary:	Python 3 bindings for Cairo

Group:		System Environment/Libraries
License:	MIT
URL:		http://cairographics.org/releases/
Source0:	%{name}-%{version}.tar.gz
Source1:        fake-config

BuildRequires:	%{python_version}-devel
BuildRequires:	pkgconfig(cairo)
Requires:	%{python_version}-base

%description
%{summary}.

%package devel
Summary:        Python3 bindings for Cairo (development headers)
Requires:       %{name} = %{version}

%description devel
%{summary}.

%prep
%setup -q

%build
cd %{source_subtree}
# Make sure it builds against the right Python version
export PYTHON=python3
# We need to create a fake config script that will redirect
# the call to using the shell, as waf for some stupid reason
# always executes python-config with the Python interpreter
export PYTHON_CONFIG=fake-config
cp %{SOURCE1} $PYTHON_CONFIG
$PYTHON ./waf configure --prefix=%{_prefix}
./waf build

%install
rm -rf $RPM_BUILD_ROOT
cd %{source_subtree}
./waf install --destdir=$RPM_BUILD_ROOT

# Remove files that were byte-compiled by waf
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{python_version}.*/site-packages/cairo/__init__.py{c,o}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/%{python_version}.*/site-packages/cairo

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{upstream_name}/%{package_name}.h
%{_libdir}/pkgconfig/%{package_name}.pc
