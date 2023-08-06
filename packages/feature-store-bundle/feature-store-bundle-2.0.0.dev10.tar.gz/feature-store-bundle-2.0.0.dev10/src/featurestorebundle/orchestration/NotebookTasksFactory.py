from typing import List
from pyspark.dbutils import DBUtils
from featurestorebundle.orchestration.NotebookTask import NotebookTask


class NotebookTasksFactory:
    def __init__(self, dbutils: DBUtils):
        self.__dbutils = dbutils

    def create(self, notebooks: List[str]) -> List[NotebookTask]:
        parameters = dict(self.__dbutils.notebook.entry_point.getCurrentBindings())

        notebook_paths = [
            notebook_path.replace("/Workspace", "", 1) if notebook_path.startswith("/Workspace/Repos") else notebook_path
            for notebook_path in notebooks
        ]

        return [NotebookTask(notebook_path, parameters=parameters) for notebook_path in notebook_paths]
