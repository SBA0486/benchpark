
from spack.package import *

class Globalsums(CMakePackage):
    """ Test example Globalsums """

    homepage = "https://github.com/lanl/GlobalSums/tree/b4b71b8cd1492aafeddfea97410e1147b96d789d"
#    git = "https://github.com/lanl/GlobalSums.git"
    git = "https://github.com/SBA0486/GlobalSums.git"

    version("master", branch="master", submodules=False)

    variant("openmp", default=True, description="Build with OpenMP enabled.")
    variant("mpi", default=True, description="Build with MPI.")
    
    depends_on("mpi", when="+mpi")
    depends_on("cmake")

    @run_before("cmake")
    def edit(self):
        cmakefile = join_path(self.stage.source_path, "CMakeLists.txt")
        filter_file(r"^\# Cleanup", f"install(TARGETS globalsums \n\t\tDESTINATION bin \n) \n\n# Cleanup", cmakefile)
      #  filter_file(r"COMPILE_FLAGS \$\{VECTOR_C_FLAGS\}", "COMPILE_FLAGS \"${VECTOR_C_FLAGS}\"", cmakefile)
      #  filter_file(r"COMPILE_FLAGS \$\{VECTOR_CXX_FLAGS\}", "COMPILE_FLAGS \"${VECTOR_CXX_FLAGS}\"", cmakefile)
      #  filter_file(r"COMPILE_FLAGS \$\{VECTOR_NOVEC_C_FLAGS\}", "COMPILE_FLAGS \"${VECTOR_NOVEC_C_FLAGS}\"", cmakefile)
      #  filter_file(r"COMPILE_FLAGS \$\{OpenMP_C_FLAGS\}", "COMPILE_FLAGS \"${OpenMP_C_FLAGS}\"", cmakefile)
      #  filter_file(r"COMPILE_FLAGS \$\{OpenMP_CXX_FLAGS\}", "COMPILE_FLAGS \"${OpenMP_CXX_FLAGS}\"", cmakefile)
                
    def cmake_args(self):
        define_from_variant = self.define_from_variant
        spec = self.spec
        define = self.define
        args = [
            define_from_variant("USE_MPI", "mpi"),
            define_from_variant("USE_OPENMP", "openmp"),
        ]
        if spec.satisfies("+mpi"):
            args.extend(
                [
                    define("CMAKE_C_COMPILER", spec["mpi"].mpicc),
                ]
            )
        if spec.satisfies("^fujitsu-mpi"):
            args.append(define("USE_FJMPI", True))
        else:
            args.append(define("USE_FJMPI", False))
        if spec.satisfies("%fj"):
            args.append(self.define("CMAKE_Fortran_MODDIR_FLAG", "-M"))
        return args

    def flag_handler(self, name, flags):
        flags = list(flags)
        if name == "fflags":
            if self.spec.satisfies("%gcc"):
                flags.append("-ffree-line-length-none")
            if self.spec.satisfies("%gcc@10:"):
                flags.append("-fallow-argument-mismatch")
        return (None, None, flags)
        
#    def cmake_args(self):
#        spec = self.spec
#        args = []
#
#        args.append('-DCMAKE_CXX_COMPILER={0}'.format(spec["mpi"].mpicc))
#
#        args.append(self.define_from_variant("USE_OPENMP", "openmp"))
#       
#        args.append(self.define_from_variant("USE_CALIPER", "caliper"))
#        args.append("-DMPI_CXX_LINK_FLAGS={0}".format(spec["mpi"].libs.ld_flags))
#
#        return args
