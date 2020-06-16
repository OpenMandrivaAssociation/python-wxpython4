%define pkgname      wxpython4
%define srcname      wxPython
%define sip_ver      1:4.19.1

%bcond_with tests

Name:           python-wxpython4
Version:        4.1.0
Release:        1
Summary:        New implementation of wxPython, a GUI toolkit for Python
License:        wxWidgets and BSD
Group:          Development/Python
URL:            https://www.wxpython.org/
Source0:        https://files.pythonhosted.org/packages/source/w/%{srcname}/%{srcname}-%{version}.tar.gz
# wxPython upstream uses a private sip module, wx.siplib, and bundles the
# siplib code.  It's not possible to build this siplib because the source code
# for sipgen is not included.  Thus we unbundle sip and the sip package builds
# a wx.siplib for us in Fedora.
Patch0:         unbundle-sip.patch

BuildRequires:  doxygen
BuildRequires:  waf
#BuildRequires:  wxgtku3.0-devel
BuildRequires:  wxgtk3.1-devel
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gdk-3.0)
BuildRequires:  python3dist(requests)

%{?python_provide:%python_provide python-%{pkgname}}
BuildRequires:  pkgconfig(python)
BuildRequires:  python-numpy-devel
# Available in unsupported, so disable for now.
#BuildRequires:  python3dist(pathlib2)
BuildRequires:  python3dist(pillow)
BuildRequires:  python3dist(setuptools)
# Devel not available here, so disable it and try python-sip
#BuildRequires:  python-sip-devel >= %{sip_ver}
BuildRequires:  python-sip4
BuildRequires:  python-sip4-wx
BuildRequires:  python3dist(six)
Requires:       python3dist(pillow)
#Requires:       python-wx-siplib-api(%{_sip_api_major}) >= %{_sip_api}
Requires:       python3dist(six)

# For tests
%if %{with tests}
BuildRequires:  locales-en
BuildRequires:  x11-server-xvfb
BuildRequires:  python3dist(numpy)
# Available in Cooker but in unsupported repo. Disable for now.
#BuildRequires:  python3dist(pypdf2)
BuildRequires:  python3dist(pytest)
# Not imported yet
#BuildRequires:  python-pytest-timeout
#BuildRequires:  python-pytest-xdist
#BuildRequires:  python-wx-siplib
%endif

%description
wxPython4 is a is a new implementation of wxPython focused on improving speed,
maintainability and extensibility. Just like "Classic" wxPython it wraps the
wxWidgets C++ toolkit and provides access to the user interface portions of the
wx API, enabling Python applications to have a GUI on Windows, Macs or Unix
systems with a native look and feel and requiring very little (if any) platform
specific code.
#----------------------------------------------

%package -n     python-%{pkgname}-media
Summary:        New implementation of wxPython, a GUI toolkit for Python3 (media module)
Group:          Development/Python
%{?python_provide:%python_provide python-%{pkgname}-media}
Requires:       python-%{pkgname} = %{version}-%{release}

%description -n python-%{pkgname}-media
wxPython4 is a is a new implementation of wxPython focused on improving speed,
maintainability and extensibility. Just like "Classic" wxPython it wraps the
wxWidgets C++ toolkit and provides access to the user interface portions of the
wx API, enabling Python applications to have a GUI on Windows, Macs or Unix
systems with a native look and feel and requiring very little (if any) platform
specific code.

This package provides the wx.media module.

%package -n     python-%{pkgname}-webview
Summary:        New implementation of wxPython, a GUI toolkit for Python3 (webview module)
Group:          Development/Python
%{?python_provide:%python_provide python-%{pkgname}-webview}
Requires:       python-%{pkgname} = %{version}-%{release}

%description -n python-%{pkgname}-webview
wxPython4 is a is a new implementation of wxPython focused on improving speed,
maintainability and extensibility. Just like "Classic" wxPython it wraps the
wxWidgets C++ toolkit and provides access to the user interface portions of the
wx API, enabling Python applications to have a GUI on Windows, Macs or Unix
systems with a native look and feel and requiring very little (if any) platform
specific code.

This package provides the wx.html2 module.

%package        doc
Summary:        Documentation and samples for wxPython
Group:          Development/Python
BuildArch:      noarch

%description doc
Documentation, samples and demo application for wxPython.

#----------------------------------------------

%prep
%autosetup -n %{srcname}-%{version} -p1

rm -rf sip/siplib
rm -rf wx/py/tests
rm -f docs/sphinx/_downloads/i18nwxapp/i18nwxapp.zip
cp -a wx/lib/pubsub/LICENSE_BSD_Simple.txt license
# Remove env shebangs from various files
sed -i -e '/^#!\//, 1d' demo/*.py{,w}
sed -i -e '/^#!\//, 1d' demo/agw/*.py
sed -i -e '/^#!\//, 1d' docs/sphinx/_downloads/i18nwxapp/*.py
sed -i -e '/^#!\//, 1d' samples/floatcanvas/*.py
sed -i -e '/^#!\//, 1d' samples/mainloop/*.py
sed -i -e '/^#!\//, 1d' samples/ribbon/*.py
sed -i -e '/^#!\//, 1d' wx/py/*.py
sed -i -e '/^#!\//, 1d' wx/tools/*.py
# Fix end of line encodings
sed -i 's/\r$//' docs/sphinx/_downloads/*.py
sed -i 's/\r$//' docs/sphinx/rest_substitutions/snippets/python/contrib/*.py
sed -i 's/\r$//' docs/sphinx/rest_substitutions/snippets/python/converted/*.py
sed -i 's/\r$//' docs/sphinx/_downloads/i18nwxapp/locale/I18Nwxapp.pot
sed -i 's/\r$//' docs/sphinx/make.bat
sed -i 's/\r$//' docs/sphinx/phoenix_theme/theme.conf
sed -i 's/\r$//' samples/floatcanvas/BouncingBall.py
# Remove spurious executable perms
chmod -x demo/*.py
chmod -x samples/mainloop/mainloop.py
chmod -x samples/printing/sample-text.txt
# Remove empty files
find demo -size 0 -delete
find docs/sphinx/rest_substitutions/snippets/python/converted -size 0 -delete
# Convert files to UTF-8
for file in demo/TestTable.txt docs/sphinx/_downloads/i18nwxapp/locale/I18Nwxapp.pot docs/sphinx/class_summary.pkl docs/sphinx/wx.1moduleindex.pkl; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done

%build
#export CC=gcc
#export CXX=g++
#DOXYGEN=%{_bindir}/doxygen SIP=%{_bindir}/sip-wx WAF=%{_bindir}/waf \
%{__python3} -u build.py dox touch etg --nodoc sip build_py --use_syswx --gtk3

%install
%{__python3} build.py install_py --destdir=%{buildroot}
rm -f %{buildroot}%{_bindir}/*
# Remove locale files (they are provided by wxWidgets)
rm -rf %{buildroot}%{python3_sitearch}/wx/locale

%check
%if %{with tests}
SKIP_TESTS="'not (display_Tests or glcanvas_Tests or mousemanager_Tests or numdlg_Tests or uiaction_MouseTests or uiaction_KeyboardTests or unichar_Tests or valtext_Tests or test_frameRestore or test_grid_pi)'"
ln -sf %{python3_sitearch}/wx/siplib.so wx/siplib.so
xvfb-run -a %{__python3} build.py test --pytest_timeout=60 --extra_pytest="-k $SKIP_TESTS" --verbose || true
%endif

%files
%license license/*
%{python_sitearch}/*
%exclude %{python3_sitearch}/wx/*html2*
%exclude %{python3_sitearch}/wx/__pycache__/*html2*
%exclude %{python3_sitearch}/wx/*media*
%exclude %{python3_sitearch}/wx/__pycache__/*media*

%files -n python-%{pkgname}-media
%{python_sitearch}/wx/*media*
%{python_sitearch}/wx/__pycache__/*media*

%files -n python-%{pkgname}-webview
%{python_sitearch}/wx/*html2*
%{python_sitearch}/wx/__pycache__/*html2*

%files doc
%doc docs demo samples
%license license/*
