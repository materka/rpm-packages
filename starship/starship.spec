%bcond_without check

%global crate starship
%global cargo_install_lib 0

Name:           starship
Version:        1.22.1
Release:        1%{?dist}
Summary:        The minimal, blazing-fast, and infinitely customizable prompt for any shell!
License:        ISC

URL:            https://github.com/starship/starship
Source:         %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  zlib-devel

%global _description %{expand:
The minimal, blazing-fast, and infinitely customizable prompt for any shell!}

%description %{_description}
%prep
%autosetup -n %{crate}-%{version} -p1
cargo vendor
%cargo_prep -v vendor

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%{cargo_vendor_manifest}

%install
%cargo_install

%if %{with check}
%check
%cargo_test
%endif

%files
%license LICENSE
%license LICENSE.dependencies
%license cargo-vendor.txt
%doc docs/README.md docs/v3.md
%{_bindir}/starship

%changelog
%autochangelog
