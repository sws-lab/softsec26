FROM ubuntu:24.04

RUN apt-get update
RUN apt-get install -y build-essential python3-dev automake cmake git flex bison libglib2.0-dev libpixman-1-dev python3-setuptools cargo libgtk-3-dev unzip
RUN apt-get install -y lld-18 llvm-18 llvm-18-dev clang-18 python3-clang \
                       gcc-$(gcc --version|head -n1|sed 's/\..*//'|sed 's/.* //')-plugin-dev libstdc++-$(gcc --version|head -n1|sed 's/\..*//'|sed 's/.* //')-dev \
                       meson ninja-build \
                       cpio libcapstone-dev \
                       wget curl xxd

RUN wget -O /tmp/v4.35c.tar.gz "https://github.com/AFLplusplus/AFLplusplus/archive/refs/tags/v4.35c.tar.gz"
RUN cd /tmp && tar xvf v4.35c.tar.gz
RUN cd /tmp/AFLplusplus-4.35c && make distrib PERFORMANCE=1 NO_QEMU=1 NO_NYX=1 NO_UNICORN=1 NO_FRIDA=1 LLVM_CONFIG=llvm-config-18 -j$(nproc)
RUN cd /tmp/AFLplusplus-4.35c && make install

RUN wget -O /tmp/symbiotic.zip "https://zenodo.org/records/17698724/files/symbiotic.zip?download=1"
RUN cd /opt && unzip /tmp/symbiotic.zip

RUN echo "export AFL_SKIP_CPUFREQ=1" >> /etc/bash.bashrc
RUN echo "export AFL_USE_UBSAN=1" >> /etc/bash.bashrc
RUN echo "export AFL_USE_ASAN=1" >> /etc/bash.bashrc
RUN echo "export PATH=/opt/symbiotic/bin:$PATH" >> /etc/bash.bashrc

ADD . /buffer_overflows
WORKDIR /buffer_overflows