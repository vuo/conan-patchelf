from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os

class PatchelfConan(ConanFile):
    name = 'patchelf'

    source_version = '0.10pre'
    package_version = '1'
    version = '%s-%s' % (source_version, package_version)

    settings = 'os', 'compiler', 'build_type', 'arch'
    url = 'https://github.com/vuo/conan-patchelf'
    license = 'https://github.com/NixOS/patchelf/blob/master/COPYING'
    description = 'A small utility to modify the dynamic linker and RPATH of ELF executables'
    source_dir = 'patchelf'
    build_dir = '_build'

    def source(self):
        self.run("git clone https://github.com/NixOS/patchelf.git")
        with tools.chdir(self.source_dir):
            # This commit includes https://github.com/NixOS/patchelf/pull/85
            # and https://github.com/NixOS/patchelf/pull/86 (which aren't yet in a tagged release).
            self.run("git checkout 927b332")
            self.run("./bootstrap.sh")

        self.run('mv %s/COPYING %s/%s.txt' % (self.source_dir, self.source_dir, self.name))

    def build(self):
        tools.mkdir(self.build_dir)
        with tools.chdir(self.build_dir):
            autotools = AutoToolsBuildEnvironment(self)
            autotools.flags.append('-Oz')
            env_vars = {
                'CC' : '/usr/bin/clang-5.0',
                'CXX': '/usr/bin/clang++-5.0',
            }
            with tools.environment_append(env_vars):
                autotools.configure(configure_dir='../%s' % self.source_dir,
                                    build=False,
                                    host=False,
                                    args=['--quiet',
                                          '--prefix=%s' % os.getcwd()])
                autotools.make(args=['--quiet'])

    def package(self):
        self.copy('patchelf', src='%s/src' % self.build_dir, dst='bin')
        self.copy('%s.txt' % self.name, src=self.source_dir, dst='license')
