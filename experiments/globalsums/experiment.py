
from benchpark.directives import variant, maintainers
from benchpark.experiment import Experiment
from benchpark.openmp import OpenMPExperiment

class Globalsums(
    Experiment,
    OpenMPExperiment,
):
    variant(
        "workload",
        default="globalsums",
        description="Workload to run",
    )
    variant(
        "version",
        default="master",
        description="app version",
    )

    maintainers("sba")

    def compute_applications_section(self):
        self.add_experiment_variable("n_nodes", ["1"], True)
        self.add_experiment_variable("processes_per_node", ["1"])
        self.add_experiment_variable("n_ranks", "{processes_per_node} * {n_nodes}")

        if self.spec.satisfies("+openmp"):
            self.add_experiment_variable("omp_num_threads", ["48"])
            self.add_experiment_variable("arch", "OpenMP")
        
        self.set_required_variables(
            n_resources="{n_ranks}",
            process_problem_size="",
            total_problem_size="",
        )

    def compute_package_section(self):
        # get package version
        app_version = self.spec.variants["version"][0]
        self.add_package_spec(self.name, [f"globalsums@{app_version}"])
