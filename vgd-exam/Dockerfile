# A self-contained, cross-platform environment for the exam. It builds for the
# host CPU and runs natively on Apple Silicon, Intel macOS, and x86_64/arm64
# Linux (and on Windows via WSL2 or Docker Desktop) -- no emulation.
#
#   docker build -t vgd-exam .          # or: podman build -t vgd-exam .
#   docker run --rm -it -v "$PWD":/exam vgd-exam
#
# The -v mount makes the container work on your own copy of the files, so your
# edits and the generated answers.json stay on your machine.
FROM ubuntu:24.04

# Non-interactive apt so tzdata (pulled in by the JDK) does not prompt.
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Provided automatically by the builder: "arm64" or "amd64".
ARG TARGETARCH

# The Gradle wrapper (./gradlew, shipped in the repo) builds the Java and runs
# Jazzer (the fuzzer); Jazzer is pulled in as a Gradle dependency and ships a
# native driver for every platform here. python3 runs exam.py. The .NET SDK
# installs Dafny as an architecture-independent tool; z3 is its solver.
# (The JDK comes from Adoptium below, so we don't install one from apt.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        make \
        python3 \
        dotnet-sdk-8.0 \
        ca-certificates \
        wget \
        unzip \
        libicu74 && \
    rm -rf /var/lib/apt/lists/*

# JDK 25 (Eclipse Temurin) so the container matches the JDK the exam is
# developed and graded against. Installed under /opt/jdk and put first on PATH,
# ahead of any JRE that apt may have pulled in as a dependency.
RUN case "${TARGETARCH}" in \
        arm64) JARCH=aarch64 ;; \
        amd64) JARCH=x64 ;; \
        *) echo "unsupported TARGETARCH=${TARGETARCH}" >&2; exit 1 ;; \
    esac && \
    wget -q -O /tmp/jdk.tar.gz \
        "https://api.adoptium.net/v3/binary/latest/25/ga/linux/${JARCH}/jdk/hotspot/normal/eclipse" && \
    mkdir -p /opt/jdk && \
    tar -xzf /tmp/jdk.tar.gz -C /opt/jdk --strip-components=1 && \
    rm /tmp/jdk.tar.gz
ENV JAVA_HOME=/opt/jdk
ENV PATH="/opt/jdk/bin:${PATH}"

# Dafny 4.11.0 (matches lib/DafnyRuntime.jar) as a .NET global tool.
ENV PATH="/root/.dotnet/tools:${PATH}"
RUN dotnet tool install --global dafny --version 4.11.0

# z3 4.14.1 for the host architecture, on PATH as `z3` so Dafny finds it.
RUN case "${TARGETARCH}" in \
        arm64) Z3="z3-4.14.1-arm64-glibc-2.34" ;; \
        amd64) Z3="z3-4.14.1-x64-glibc-2.35" ;; \
        *) echo "unsupported TARGETARCH=${TARGETARCH}" >&2; exit 1 ;; \
    esac && \
    wget -q -O /tmp/z3.zip \
        "https://github.com/Z3Prover/z3/releases/download/z3-4.14.1/${Z3}.zip" && \
    unzip -q /tmp/z3.zip -d /opt && \
    rm /tmp/z3.zip && \
    ln -s "/opt/${Z3}/bin/z3" /usr/local/bin/z3

ENV GRADLE_OPTS=-Xmx2g

WORKDIR /exam
COPY . /exam

# Pre-warm the Gradle wrapper: download the pinned distribution and resolve the
# Jazzer/JUnit dependencies into GRADLE_USER_HOME (/root/.gradle) at build time,
# so the exam runs without network even though the runtime volume mount shadows
# /exam (the cache under /root/.gradle is not shadowed). --no-daemon keeps no
# background JVM in the image layer.
RUN ./gradlew --no-daemon testClasses

CMD ["/bin/bash"]
