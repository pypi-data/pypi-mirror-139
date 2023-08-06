from base import *


class MyTestCase(unittest.TestCase):
    def test_01_CreateProject(self):
        global project
        project = Base.cl.create_project_as("UTEME")
        self.assertTrue(project)

        project.add("Rectangle").update(materialId = "P34")
        project.add("EME").update(backgroundMaterial = Base.cl.user_material["Air"]["id"])
        project.save()
        global task
        task = project.run("EME_FDE").asEME()
        global task_
        task_ = project.run("EME_EME").asEME()

    def test_06_Result(self):
        pass


if __name__ == '__main__':
    unittest.main()
