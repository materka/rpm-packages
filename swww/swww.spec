%bcond_without check

%global crate swww
%global cargo_install_lib 0
%global debug_package %{nil}

Name:           swww
Version:        0.9.5.3e2e2ba
Release:        1%{?dist}
Summary:        Efficient animated wallpaper daemon for wayland, controlled at runtime
License:        GPL-3

URL:            https://github.com/materka/swww
Source:         %{url}/archive/v%{version}.tar.gz
BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  scdoc
BuildRequires: 	git
BuildRequires:	lz4-devel

%global _description %{expand:
Efficient animated wallpaper daemon for wayland, controlled at runtime.}

%description %{_description}

%package bash-completion
BuildArch:      noarch
Summary:        Bash completion files for %{name}
Provides:       %{name}-bash-completion = %{version}-%{release}

Requires:       bash-completion
Requires:       %{name} = %{version}-%{release}

%description bash-completion
This package installs Bash completion files for %{name}

%package fish-completion
BuildArch:      noarch
Summary:        Fish completion files for %{name}
Provides:       %{name}-fish-completion = %{version}-%{release}

Requires:       fish
Requires:       %{name} = %{version}-%{release}

%description fish-completion
This package installs Fish completion files for %{name}

%package zsh-completion
BuildArch:      noarch
Summary:        Zsh completion files for %{name}
Provides:       %{name}-zsh-completion = %{version}-%{release}

Requires:       zsh
Requires:       %{name} = %{version}-%{release}

%description zsh-completion
This package installs Zsh completion files for %{name}

%prep
%autosetup -n %{crate}-%{version} -p1
cargo vendor
%cargo_prep -v vendor

%_buildshell doc/gen.sh

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%{cargo_vendor_manifest}

%install
cargo install --no-track --path client
cargo install --no-track --path daemon

install -Dpm644 doc/generated/swww.1 %{buildroot}%{_mandir}/man1/swww.1
install -Dpm644 doc/generated/swww-clear.1 %{buildroot}%{_mandir}/man1/swww-clear.1
install -Dpm644 doc/generated/swww-clear-cache.1 %{buildroot}%{_mandir}/man1/swww-clear-cache.1
install -Dpm644 doc/generated/swww-daemon.1 %{buildroot}%{_mandir}/man1/swww-daemon.1
install -Dpm644 doc/generated/swww-img.1 %{buildroot}%{_mandir}/man1/swww-img.1
install -Dpm644 doc/generated/swww-kill.1 %{buildroot}%{_mandir}/man1/swww-kill.1
install -Dpm644 doc/generated/swww-query.1 %{buildroot}%{_mandir}/man1/swww-query.1
install -Dpm644 doc/generated/swww-restore.1 %{buildroot}%{_mandir}/man1/swww-restore.1

install -Dpm644 completions/swww.bash %{buildroot}%{bash_completions_dir}/swww
install -Dpm644 completions/swww.fish %{buildroot}%{fish_completions_dir}/swww.fish
install -Dpm644 completions/_swww %{buildroot}%{zsh_completions_dir}/_swww

%if %{with check}
%check
%cargo_test
%endif

%files
%license LICENSE
%license LICENSE.dependencies
%license cargo-vendor.txt
%doc README.md
%{_bindir}/swww
%{_bindir}/swww-daemon
%{_mandir}/man1/swww.1*
%{_mandir}/man1/swww-clear.1*
%{_mandir}/man1/swww-clear-cache.1*
%{_mandir}/man1/swww-daemon.1*
%{_mandir}/man1/swww-img.1*
%{_mandir}/man1/swww-kill.1*
%{_mandir}/man1/swww-query.1*
%{_mandir}/man1/swww-restore.1*

%files bash-completion
%{bash_completions_dir}/swww

%files zsh-completion
%{zsh_completions_dir}/_swww

%files fish-completion
%{fish_completions_dir}/swww.fish

%changelog
%autochangelog
