"""
Implementation of the CMEPS FUNIT test.

This "system" test runs the pFUnit unit tests for the CMEPS atm/ocn bulk flux schemes
(components/cmeps/cesm/flux_atmocn). We're abusing the system test infrastructure to run
these, so that a run of the test suite can result in the unit tests being run as well.

Grid and compset are irrelevant for this test type.
"""

import os
from CIME.SystemTests.funit import FUNIT
from CIME.XML.standard_module_setup import *

logger = logging.getLogger(__name__)


class FUNITCMEPS(FUNIT):
    def __init__(self, case):
        FUNIT.__init__(self, case)

    def get_test_spec_dir(self):
        return os.path.join(
            self._case.get_value("SRCROOT"),
            "components",
            "cmeps",
            "cesm",
            "flux_atmocn",
            "test",
        )

    def get_extra_run_tests_args(self):
        # Build against the CESM_share checked out with this CESM tag, rather than
        # fetching CESM_share from GitHub (the default in the tests' CMakeLists.txt).
        share_dir = os.path.join(self._case.get_value("SRCROOT"), "share")
        return '--cmake-args " -DFETCHCONTENT_SOURCE_DIR_CESM_SHARE={}"'.format(
            share_dir
        )

    def run_phase(self):
        test_spec_dir = self.get_test_spec_dir()
        expect(
            os.path.isfile(os.path.join(test_spec_dir, "CMakeLists.txt")),
            "RUN FAIL for FUNITCMEPS: CMEPS unit test directory not found: {}\n"
            "(The CMEPS version used by this CESM checkout may predate the "
            "flux_atmocn unit tests.)".format(test_spec_dir),
        )
        FUNIT.run_phase(self)
