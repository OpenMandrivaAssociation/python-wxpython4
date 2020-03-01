%define pkgname      wxpython4
%define srcname      wxPython
%define sip_ver      1:4.19.1

%bcond_with tests

Name:           python-wxpython4
Version:        4.0.7
Release:        %mkrel 2
Summary:        New implementation of wxPython, a GUI toolkit for Python
# wxPython is licensed under the wxWidgets license.  The only exception is
# the pubsub code in wx/lib/pubsub which is BSD licensed.  Note: wxPython
# includes a bundled copy of wxWidgets in ext/wxWidgets which has a few
# bits of code that use other licenses.  This source is not used in the
# Fedora build, except for the interface headers in ext/wxWidgets/interface
# and the doxygen build scripts.
License:        wxWidgets and BSD
Group:          Development/Python
URL:            https://www.wxpython.org/
Source0:        https://files.pythonhosted.org/packages/source/w/%{srcname}/%{srcname}-%{version}.tar.gz
# wxPython upstream uses a private sip module, wx.siplib, and bundles the
# siplib code.  It's not possible to build this siplib because the source code
# for sipgen is not included.  Thus we unbundle sip and the sip package builds
# a wx.siplib for us in Fedora.
Patch0:         unbundle-sip.patch

BuildRequires:  gcc-c++
BuildRequires:  doxygen
BuildRequires:  waf >= 2.0.18-2
BuildRequires:  wxgtk3.0-devel
# For tests
%if %{with tests}
BuildRequires:  locales-en
BuildRequires:  x11-server-xvfb
BuildRequires:  python3-numpy
BuildRequires:  python3-pypdf2
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-timeout
BuildRequires:  python3-pytest-xdist
BuildRequires:  python3-wx-siplib
%endif

%description
wxPython4 is a is a new implementation of wxPython focused on improving speed,
maintainability and extensibility. Just like "Classic" wxPython it wraps the
wxWidgets C++ toolkit and provides access to the user interface portions of the
wx API, enabling Python applications to have a GUI on Windows, Macs or Unix
systems with a native look and feel and requiring very little (if any) platform
specific code.
#----------------------------------------------

### Python 3

%package -n     python3-%{pkgname}
Summary:        New implementation of wxPython, a GUI toolkit for Python3
Group:          Development/Python
%{?python_provide:%python_provide python3-%{pkgname}}
BuildRequires:  python3-devel
BuildRequires:  python3-numpy-devel
BuildRequires:  python3-pathlib2
BuildRequires:  python3-pillow
BuildRequires:  python3-setuptools
BuildRequires:  python3-sip-devel >= %{sip_ver}
BuildRequires:  python3-six
Requires:       python3-pillow
Requires:       python3-wx-siplib-api(%{_sip_api_major}) >= %{_sip_api}
Requires:       python3-six

%description -n python3-%{pkgname}
wxPython4 is a is a new implementation of wxPython focused on improving speed,
maintainability and extensibility. Just like "Classic" wxPython it wraps the
wxWidgets C++ toolkit and provides access to the user interface portions of the
wx API, enabling Python applications to have a GUI on Windows, Macs or Unix
systems with a native look and feel and requiring very little (if any) platform
specific code.

#----------------------------------------------

%package -n     python3-%{pkgname}-media
Summary:        New implementation of wxPython, a GUI toolkit for Python3 (media module)
Group:          Development/Python
%{?python_provide:%python_provide python3-%{pkgname}-media}
Requires:       python3-%{pkgname} = %{version}-%{release}

%description -n python3-%{pkgname}-media
wxPython4 is a is a new implementation of wxPython focused on improving speed,
maintainability and extensibility. Just like "Classic" wxPython it wraps the
wxWidgets C++ toolkit and provides access to the user interface portions of the
wx API, enabling Python applications to have a GUI on Windows, Macs or Unix
systems with a native look and feel and requiring very little (if any) platform
specific code.

This package provides the wx.media module.

%package -n     python3-%{pkgname}-webview
Summary:        New implementation of wxPython, a GUI toolkit for Python3 (webview module)
Group:          Development/Python
%{?python_provide:%python_provide python3-%{pkgname}-webview}
Requires:       python3-%{pkgname} = %{version}-%{release}

%description -n python3-%{pkgname}-webview
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
DOXYGEN=%{_bindir}/doxygen SIP=%{_bindir}/sip-wx WAF=%{_bindir}/waf \
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

%files -n python3-%{pkgname}
%license license/*
%{python3_sitearch}/*
%exclude %{python3_sitearch}/wx/*html2*
%exclude %{python3_sitearch}/wx/__pycache__/*html2*
%exclude %{python3_sitearch}/wx/*media*
%exclude %{python3_sitearch}/wx/__pycache__/*media*

%files -n python3-%{pkgname}-media
%{python3_sitearch}/wx/*media*
%{python3_sitearch}/wx/__pycache__/*media*

%files -n python3-%{pkgname}-webview
%{python3_sitearch}/wx/*html2*
%{python3_sitearch}/wx/__pycache__/*html2*

%files doc
%doc docs demo samples
%license license/*
