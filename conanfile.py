from conans import ConanFile, CMake, tools


class Md5Conan(ConanFile):
    name = "md5"
    version = "1.1"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports_sources = "./*"


    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="md5")
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src=".")
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["md5app"]

