bcond_without check

%global crate swww
%global cargo_install_lib 0

Name:           swww
Version:        0.9.5
Release:        1%{?dist}
Summary:        Efficient animated wallpaper daemon for wayland, controlled at runtime
License:        GPL-3

URL:            https://github.com/LGFae/swww
Source:         %{url}/archive/v%{version}.tar.gz

BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  scdoc

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
%autosetup -n %{crate} -p1
cargo vendor
%cargo_prep -v vendor

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%{cargo_vendor_manifest}

%install
%cargo_install
for src in doc/*.scd; do
    out=$(basename "$src" .scd)
    scdoc < "$src" > man/${out}.1
    install -Dpm644 man/${out}.1 %{buildroot}%{_mandir}/man1/${out}.1
done

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
%doc docs/README.md README.md
%{_bindir}/swww
%{_mandir}/man1/*.1*

%files bash-completion
%{bash_completions_dir}/swww

%files zsh-completion
%{zsh_completions_dir}/_swww

%files fish-completion
%{fish_completions_dir}/swww.fish

%changelog
%autochangelog
