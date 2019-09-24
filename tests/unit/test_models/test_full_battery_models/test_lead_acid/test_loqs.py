#
# Tests for the lead-acid LOQS model
#
import pybamm
import unittest


class TestLeadAcidLOQS(unittest.TestCase):
    def test_well_posed(self):
        options = {"thermal": "isothermal"}
        model = pybamm.lead_acid.LOQS(options)
        model.check_well_posedness()

    def test_default_geometry(self):
        options = {"thermal": "isothermal"}
        model = pybamm.lead_acid.LOQS(options)
        self.assertIsInstance(model.default_geometry, pybamm.Geometry)
        self.assertNotIn("negative particle", model.default_geometry)
        self.assertIsInstance(model.default_spatial_methods, dict)
        self.assertNotIn("negative particle", model.default_geometry)
        self.assertTrue(
            issubclass(
                model.default_spatial_methods["current collector"],
                pybamm.ZeroDimensionalMethod,
            )
        )
        self.assertTrue(
            issubclass(
                model.default_submesh_types["current collector"], pybamm.SubMesh0D
            )
        )

    def test_well_posed_with_convection(self):
        options = {"convection": {"transverse": "uniform"}}
        model = pybamm.lead_acid.LOQS(options)
        model.check_well_posedness()

        options = {"dimensionality": 1, "convection": {"transverse": "full"}}
        model = pybamm.lead_acid.LOQS(options)
        model.check_well_posedness()

    def test_well_posed_1plus1D(self):
        options = {
            "surface form": "differential",
            "current collector": "potential pair",
            "dimensionality": 1,
        }
        model = pybamm.lead_acid.LOQS(options)
        model.check_well_posedness()
        self.assertTrue(
            issubclass(
                model.default_spatial_methods["current collector"], pybamm.FiniteVolume
            )
        )
        self.assertTrue(
            issubclass(
                model.default_submesh_types["current collector"],
                pybamm.Uniform1DSubMesh,
            )
        )

    def test_well_posed_2plus1D(self):
        options = {
            "surface form": "differential",
            "current collector": "potential pair",
            "dimensionality": 2,
        }
        model = pybamm.lead_acid.LOQS(options)
        model.check_well_posedness()
        self.assertTrue(
            issubclass(
                model.default_spatial_methods["current collector"],
                pybamm.ScikitFiniteElement,
            )
        )
        self.assertTrue(
            issubclass(
                model.default_submesh_types["current collector"], pybamm.Scikit2DSubMesh
            )
        )


class TestLeadAcidLOQSWithSideReactions(unittest.TestCase):
    def test_well_posed_differential(self):
        options = {"surface form": "differential", "side reactions": ["oxygen"]}
        model = pybamm.lead_acid.LOQS(options)
        model.check_well_posedness()

    def test_well_posed_algebraic(self):
        options = {"surface form": "algebraic", "side reactions": ["oxygen"]}
        model = pybamm.lead_acid.LOQS(options)
        model.check_well_posedness()

    def test_incompatible_options(self):
        options = {"side reactions": ["something"]}
        with self.assertRaises(pybamm.OptionError):
            pybamm.lead_acid.LOQS(options)


class TestLeadAcidLOQSSurfaceForm(unittest.TestCase):
    def test_well_posed_differential(self):
        options = {"surface form": "differential"}
        model = pybamm.lead_acid.LOQS(options)
        model.check_well_posedness()

    def test_well_posed_algebraic(self):
        options = {"surface form": "algebraic"}
        model = pybamm.lead_acid.LOQS(options)
        model.check_well_posedness()

    def test_well_posed_1plus1D(self):
        options = {
            "surface form": "differential",
            "current collector": "potential pair",
            "dimensionality": 1,
        }
        model = pybamm.lead_acid.LOQS(options)
        model.check_well_posedness()


if __name__ == "__main__":
    print("Add -v for more debug output")
    import sys

    if "-v" in sys.argv:
        debug = True
    pybamm.settings.debug_mode = True
    unittest.main()
