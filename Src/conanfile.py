from conan import ConanFile
from conan.tools.cmake import cmake_layout, CMakeToolchain, CMakeDeps


class QVLConan(ConanFile):
    name = "qvl"
    version = "1.0.0"
    
    # Package metadata
    license = "BSD-3-Clause"
    author = "Intel Corporation"
    url = "https://github.com/intel/confidential-computing.tee.dcap.qvl"
    description = "SGX and TDX DCAP Quote Verification Library"
    topics = ("sgx", "tdx", "attestation", "quote-verification")
    
    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    
    # Build options
    options = {
        "build_tests": [True, False],
        "build_docs": [True, False],
        "build_attestation_app": [True, False],
    }
    
    default_options = {
        "build_tests": False,
        "build_docs": False,
        "build_attestation_app": False,
        # Dependency options
        "openssl/*:shared": False,
        "openssl/*:no_tests": True,
        "gtest/*:shared": False,
        "spdlog/*:shared": False,
        "fmt/*:shared": False,
    }
    
    def requirements(self):
        """Declare dependencies"""
        self.requires("openssl/3.0.12")
        self.requires("spdlog/1.14.1")
        self.requires("fmt/10.2.1")
        
        if self.options.build_tests:
            self.requires("gtest/1.14.0")
    
    def build_requirements(self):
        """Build-time dependencies (optional)"""
        # Add build-only dependencies here if needed
        # Example: self.tool_requires("cmake/3.27.0")
        pass
    
    def layout(self):
        """Define the layout of the project"""
        cmake_layout(self)
    
    def generate(self):
        """Generate the necessary files for the build system"""
        # Generate CMake toolchain
        tc = CMakeToolchain(self)
        tc.user_presets_path = "ConanPresets.json"
        tc.generate()
        
        # Generate CMake dependencies
        deps = CMakeDeps(self)
        deps.generate()
    
    def configure(self):
        """Configure options and settings"""
        # Disable shared libraries for static builds
        if self.settings.os == "Emscripten":
            # Force static libraries for WebAssembly
            self.options["openssl"].shared = False
            self.options["spdlog"].shared = False
            self.options["fmt"].shared = False
            if self.options.build_tests:
                self.options["gtest"].shared = False
