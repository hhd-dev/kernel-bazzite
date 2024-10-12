FROM fedora

RUN dnf install -y fedpkg fedora-packager rpmdevtools ncurses-devel pesign \
    asciidoc audit-libs-devel bc bindgen binutils-devel bison clang dwarves \
    elfutils-devel flex fuse-devel gcc gcc-c++ gettext glibc-static hostname \
    java-devel kernel-rpm-macros libbabeltrace-devel libbpf-devel \
    libcap-devel libcap-ng-devel libmnl-devel libnl3-devel libtraceevent-devel \
    libtracefs-devel lld llvm-devel lvm2 m4 make net-tools newt-devel \
    numactl-devel openssl openssl-devel pciutils-devel perl perl-devel \
    perl-generators python3-devel python3-docutils rsync rust rust-src \
    systemd-boot-unsigned systemd-ukify which xmlto xz-devel zlib-devel \
    && dnf clean all

RUN useradd -m -s /bin/bash builder

USER builder

WORKDIR /workspace

ENTRYPOINT [ "env" ]