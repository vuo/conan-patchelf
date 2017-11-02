from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os

class PatchelfConan(ConanFile):
    name = 'patchelf'
    version = '0.9'
    settings = 'os', 'compiler', 'build_type', 'arch'
    url = 'https://github.com/vuo/conan-patchelf'
    license = 'https://github.com/NixOS/patchelf/blob/master/COPYING'
    description = 'A small utility to modify the dynamic linker and RPATH of ELF executables'
    source_dir = 'patchelf-%s' % version
    build_dir = '_build'

    def source(self):
        self.output.info(self.package_folder)
        tools.get('https://nixos.org/releases/patchelf/patchelf-%s/patchelf-%s.tar.bz2' % (self.version, self.version),
                  sha256='a0f65c1ba148890e9f2f7823f4bedf7ecad5417772f64f994004f59a39014f83')

    def build(self):
        tools.mkdir(self.build_dir)
        with tools.chdir(self.build_dir):
            autotools = AutoToolsBuildEnvironment(self)
            autotools.cxx_flags.append('-Oz')
            env_vars = {
                'CC' : '/opt/llvm-3.8.0/bin/clang',
                'CXX': '/opt/llvm-3.8.0/bin/clang++',
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
