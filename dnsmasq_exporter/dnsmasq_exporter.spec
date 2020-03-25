%define debug_package %{nil}

Name:    dnsmasq_exporter
Version: 0.2.0
Release: 1%{?dist}
Summary: Prometheus dnsmasq exporter.
License: ASL 2.0
URL:     https://github.com/google/%{name}

Source0: https://github.com/google/%{name}/archive/v%{version}.tar.gz
Source1: %{name}.service
Source2: %{name}.default

BuildRequires: golang >= 1.12

%{?systemd_requires}
Requires(pre): shadow-utils
Requires: dnsmasq >= 2.69

%description

Export dnsmasq metrics to Prometheus.

%prep
%setup -q

%build
GOPROXY=https://proxy.golang.org go build -o %{name} .

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %attr(755, prometheus, prometheus)%{_sharedstatedir}/prometheus
