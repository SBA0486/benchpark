# Copyright 2023 Lawrence Livermore National Security, LLC and other
# Benchpark Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: Apache-2.0

import pathlib

from benchpark.directives import variant
from benchpark.system import System


class Tioga(System):
    variant(
        "rocm",
        default="551",
        values=("543", "551"),
        description="ROCm version",
    )

    variant(
        "compiler",
        default="cce",
        values=("gcc", "cce"),
        description="Which compiler to use",
    )

    variant(
        "gtl",
        default=False,
        values=(True, False),
        description="Use GTL-enabled MPI",
    )

    def initialize(self):
        super().initialize()

        self.scheduler = "flux"
        self.sys_cores_per_node = "64"
        self.sys_gpus_per_node = "4"

    def generate_description(self, output_dir):
        super().generate_description(output_dir)

        sw_description = pathlib.Path(output_dir) / "software.yaml"

        with open(sw_description, "w") as f:
            f.write(self.sw_description())

    def external_pkg_configs(self):
        externals = Tioga.resource_location / "externals"

        rocm = self.spec.variants["rocm"][0]
        gtl = self.spec.variants["gtl"][0]
        compiler = self.spec.variants["compiler"][0]

        selections = [externals / "base" / "00-packages.yaml"]
        if rocm == "543":
            selections.append(externals / "rocm" / "00-version-543-packages.yaml")
        elif rocm == "551":
            selections.append(externals / "rocm" / "01-version-551-packages.yaml")

        if compiler == "cce":
            if gtl == "true":
                selections.append(externals / "mpi" / "02-cce-ygtl-packages.yaml")
            else:
                selections.append(externals / "mpi" / "01-cce-ngtl-packages.yaml")
            selections.append(externals / "libsci" / "01-cce-packages.yaml")
        elif compiler == "gcc":
            selections.append(externals / "mpi" / "00-gcc-ngtl-packages.yaml")
            selections.append(externals / "libsci" / "00-gcc-packages.yaml")

        return selections

    def compiler_configs(self):
        compilers = Tioga.resource_location / "compilers"

        compiler = self.spec.variants["compiler"][0]
        # rocm = self.spec.variants["rocm"][0]

        selections = []
        # TODO: I'm not actually sure what compiler mixing is desired, if any
        # so I don't think the choices here make much sense, but this
        # demonstrate how system spec variants can be used to choose what
        # configuration to construct
        if compiler == "cce":
            selections.append(compilers / "rocm" / "00-rocm-551-compilers.yaml")
        elif compiler == "gcc":
            selections.append(compilers / "gcc" / "00-gcc-12-compilers.yaml")

        return selections

    def system_specific_variables(self):
        return {"rocm_arch": "gfx90a"}

    def sw_description(self):
        """This is somewhat vestigial: for the Tioga config that is committed
        to the repo, multiple instances of mpi/compilers are stored and
        and these variables were used to choose consistent dependencies.
        The configs generated by this class should only ever have one
        instance of MPI etc., so there is no need for that. The experiments
        will fail if these variables are not defined though, so for now
        they are still generated (but with more-generic values).
        """
        return """\
software:
  packages:
    default-compiler:
      pkg_spec: cce
    default-mpi:
      pkg_spec: cray-mpich
    compiler-rocm:
      pkg_spec: cce
    compiler-amdclang:
      pkg_spec: clang
    compiler-gcc:
      pkg_spec: gcc
    blas-rocm:
      pkg_spec: rocblas
    blas:
      pkg_spec: rocblas
    lapack-rocm:
      pkg_spec: rocsolver
    lapack:
      pkg_spec: cray-libsci
    mpi-rocm-gtl:
      pkg_spec: cray-mpich+gtl
    mpi-rocm-no-gtl:
      pkg_spec: cray-mpich~gtl
    mpi-gcc:
      pkg_spec: cray-mpich~gtl
    fftw:
      pkg_spec: intel-oneapi-mkl
"""
