%global commit 0b58eb0a3a45de6fdfaa3f868d7dfa2d14f33db1

Name:           odroid-xu-exynos5-hwcomposer
Version:        2013.10.03
Release:        1%{?dist}
Summary:        Exynos5 HW Composer

Group:          System Environment/Daemons
License:        GPLv3
URL:            https://github.com/hardkernel/linux/tree/odroidxu-3.4.y/tools/hardkernel/exynos5-hwcomposer
Source0:        https://github.com/hardkernel/linux/archive/%{commit}/linux-%{commit}.tar.gz
Source1:        60-exynos5-hwcomposer.conf
Source2:        60-exynos5-hwcomposer.rules
Source3:        exynos5-hwcomposer.service
Patch0:         %{name}-2013.10.03-link-libhwcomposer-statically.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
This is the Exynos5 HW Composer that Copies from the framebuffer to HDMI.

This piece of software is needed to use the HDMI on newer Exynos5 processors.

Its original author is Samsung LSI. Kindly modified by Dongjin Kim to work
on Linux.

%prep
%setup -qn linux-%{commit}/tools/hardkernel/exynos5-hwcomposer
%patch0 -p1
chmod 644 src/hardware/samsung_slsi/exynos/include/exynos_format.h src/hardware/samsung_slsi/exynos5410/include/gralloc_priv.h

%build
sh autogen.sh
%configure
make %{?_smp_mflags}

%install
install -p -m0644 -D %{SOURCE1} %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d/60-exynos5-hwcomposer.conf
install -p -m0644 -D %{SOURCE2} %{buildroot}%{_udevrulesdir}/60-exynos5-hwcomposer.rules
install -p -m0644 -D %{SOURCE3} %{buildroot}%{_unitdir}/exynos5-hwcomposer.service
install -p -m0755 -D tools/exynos5-hwcomposer %{buildroot}%{_sbindir}/exynos5-hwcomposer

%post
%systemd_post exynos5-hwcomposer.service

%preun
%systemd_preun exynos5-hwcomposer.service

%postun
%systemd_postun_with_restart exynos5-hwcomposer.service 

%files
%doc COPYING README
%{_prefix}/lib/dracut/dracut.conf.d/60-exynos5-hwcomposer.conf
%{_unitdir}/exynos5-hwcomposer.service
%{_udevrulesdir}/60-exynos5-hwcomposer.rules
%{_sbindir}/exynos5-hwcomposer

%changelog
* Sun Apr 05 2015 Scott K Logan <logans@cottsay.net> - 2013.10.03-1
- Initial package
