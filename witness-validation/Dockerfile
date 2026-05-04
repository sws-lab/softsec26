FROM ghcr.io/goblint/analyzer:2.7.1

RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y git wget nano

RUN wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add -
ADD llvm.list /etc/apt/sources.list.d
RUN apt update
RUN apt install -y clang-23 libclang-23-dev libclang-cpp23 llvm-23 llvm-23-dev
RUN ln -s /usr/lib/llvm-23/lib/libclang-cpp.so.23.0 /usr/lib/llvm-23/lib/libclang-cpp.so

RUN git clone https://github.com/jprotopopov-ut/clang-witness-inject
RUN cd clang-witness-inject && make CXX=clang-23 -j$(nproc)

ADD . witness-validation

RUN echo "export GOBLINT_DIR=/opt/goblint/analyzer" >> /etc/bash.bashrc
RUN echo "export WITNESS_INJECT=/clang-witness-inject/witness_inject" >> /etc/bash.bashrc

WORKDIR witness-validation
ENTRYPOINT ["/bin/bash"]