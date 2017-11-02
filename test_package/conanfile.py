from conans import ConanFile

class PatchelfTestConan(ConanFile):
    def imports(self):
        self.copy('patchelf', src='bin', dst='bin')

    def test(self):
        self.run('bin/patchelf --version')
