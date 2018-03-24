from conans import ConanFile

class PatchelfTestConan(ConanFile):
    def imports(self):
        self.copy('patchelf', src='bin', dst='bin')

    def test(self):
        self.run('bin/patchelf --version')
        self.run('! (ldd bin/patchelf | grep -v "^lib/" | grep "/" | egrep -v "\s/lib64/")')
