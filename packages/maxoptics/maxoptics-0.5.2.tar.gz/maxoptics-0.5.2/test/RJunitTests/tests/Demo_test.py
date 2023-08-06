from base import *


class DemoTestCase(unittest.TestCase):
    def test_version(self):
        # self.assertEqual(True, False)  # add assertion here
        self.assertEqual(maxoptics.__VERSION__, "0.5.2")  # add assertion here

    def test_load_config(self):
        self.assertEqual(Path(__file__).parent / "maxoptics.conf", maxoptics.__CONFIGPATH__)

    def test_00_init(self):
        global cl
        cl = maxoptics.MosLibrary()

    def test_01_initProject(self):
        global pr
        pr = cl.create_project_as("Unittest")

    def test_warehouse(self):
        self.assertTrue(cl, "Initialization Failed")
        self.assertTrue(cl.user_materials)
        self.assertTrue(cl.user_waveforms)
        self.assertTrue(cl.public_materials)

    def test_overrideMeshOrder(self):
        for i in polygons:
            pprint(i)
            j = pr.add(i)
            self.assertEqual(0, j["overrideMeshOrder"])
            j["meshOrder"] = 2
            self.assertEqual(1, j["overrideMeshOrder"])


if __name__ == '__main__':
    unittest.main()
