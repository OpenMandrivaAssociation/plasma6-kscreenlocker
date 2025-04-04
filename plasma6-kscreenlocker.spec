%define stable %([ "$(echo %{version} |cut -d. -f2)" -ge 80 -o "$(echo %{version} |cut -d. -f3)" -ge 80 ] && echo -n un; echo -n stable)
#define git 20240222
%define gitbranch Plasma/6.0
%define gitbranchd %(echo %{gitbranch} |sed -e "s,/,-,g")

Summary:	Library and components for secure lock screen architecture
Name:		plasma6-kscreenlocker
Version:	6.3.4
Release:	%{?git:0.%{git}.}2
License:	GPLv2+
Group:		Graphical desktop/KDE
URL:		https://kde.org/
%if 0%{?git:1}
Source0:	https://invent.kde.org/plasma/kscreenlocker/-/archive/%{gitbranch}/kscreenlocker-%{gitbranchd}.tar.bz2#/kscreenlocker-%{git}.tar.bz2
%else
Source0:	http://download.kde.org//%{stable}/plasma/%(echo %{version} |cut -d. -f1-3)/kscreenlocker-%{version}.tar.xz
%endif
Patch0:		kscreenlocker-5.5.3-use-fallback-wallpaper-from-omv.patch
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(Qt6)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Quick)
BuildRequires:	cmake(Qt6QuickWidgets)
BuildRequires:	cmake(Qt6Test)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xcb-keysyms)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(libseccomp)
BuildRequires:	pkgconfig(libevent)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	cmake(KF6I18n)
BuildRequires:	cmake(Wayland) >= 5.90.0
BuildRequires:	cmake(Plasma) >= 5.90.0
BuildRequires:	cmake(PlasmaQuick) >= 5.90.0
BuildRequires:	cmake(KF6KCMUtils)
BuildRequires:	cmake(KF6Declarative)
BuildRequires:	cmake(KF6IdleTime)
BuildRequires:	cmake(KF6Crash)
BuildRequires:	cmake(KF6GlobalAccel)
BuildRequires:	cmake(LayerShellQt) >= 5.27.80
BuildRequires:	cmake(KF6Screen)
BuildRequires:	cmake(KF6Notifications)
BuildRequires:	cmake(KF6Svg)
BuildRequires:	cmake(KF6KIO)
BuildRequires:	cmake(KF6Solid)
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(wayland-server)
BuildRequires:	pkgconfig(wayland-cursor)
BuildRequires:	pkgconfig(wayland-egl)
BuildRequires:	pkgconfig(wayland-scanner)
BuildRequires:	wayland-tools
BuildRequires:	pam-devel
Conflicts:      plasma-workspace < 5.5.0

%description
Library and components for secure lock screen architecture.

%triggerin -- %{name} < %{EVRD}
%{_bindir}/killall kscreenlocker_greet > /dev/null 2>&1 ||:

%files -f kscreenlocker.lang -f kscreenlocker_greet.lang -f kcm_screenlocker.lang
%{_libdir}/libexec/kscreenlocker_greet
%{_datadir}/dbus-1/interfaces/kf6_org.freedesktop.ScreenSaver.xml
%{_datadir}/knotifications6/ksmserver.notifyrc
%{_datadir}/ksmserver/screenlocker/org.kde.passworddialog
%{_datadir}/dbus-1/interfaces/org.kde.screensaver.xml
%{_qtdir}/plugins/plasma/kcms/systemsettings/kcm_screenlocker.so
%{_datadir}/applications/kcm_screenlocker.desktop
%{_datadir}/qlogging-categories6/kscreenlocker.categories

#--------------------------------------------------------------------

%define kscreenlocker_major 6
%define libkscreenlocker plasma6-%{mklibname kscreenlocker}

%package -n %{libkscreenlocker}
Summary:	Library and components for secure lock screen architecture 
Group:		System/Libraries

%description -n %{libkscreenlocker}
Library and components for secure lock screen architecture.

%files -n %{libkscreenlocker}
%{_libdir}/libKScreenLocker.so.*

#--------------------------------------------------------------------

%define kscreenlocker_devel plasma6-%{mklibname kscreenlocker -d}

%package -n %{kscreenlocker_devel}
Summary:        Devel stuff for %{name}
Group:          Development/KDE and Qt
Requires:       %{name} = %{EVRD}
Requires:       %{libkscreenlocker} = %{EVRD}
Requires:       cmake(Qt6DBus)
Provides:       %{name}-devel = %{EVRD}

%description -n %{kscreenlocker_devel}
This package contains header files needed if you wish to build applications
based on %{name}.

%files -n %{kscreenlocker_devel}
%{_libdir}/libKScreenLocker.so
%{_includedir}/KScreenLocker
%{_libdir}/cmake/KScreenLocker
%{_libdir}/cmake/ScreenSaverDBusInterface

#--------------------------------------------------------------------

%prep
%autosetup -p1 -n kscreenlocker-%{?git:%{gitbranchd}}%{?!git:%{version}}
%cmake \
	-DBUILD_QCH:BOOL=ON \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

%find_lang kscreenlocker || touch kscreenlocker.lang
%find_lang kscreenlocker_greet || touch kscreenlocker_greet.lang
%find_lang kcm_screenlocker || touch kcm_screenlocker.lang
