import pytest
from airflow.models import DagBag


@pytest.fixture()
def dagbag():
    return DagBag()


def test_dag_import_errors(dagbag):
    assert dagbag.import_errors == {}


def test_dag_is_not_none(dagbag):
    for dag_id in dagbag.dag_ids:
        dag = dagbag.get_dag(dag_id=dag_id)
        assert dag is not None


@pytest.mark.parametrize('current_dag_id', ['twitter_operations'])
@pytest.mark.parametrize('tasks_count', [3])
def test_dag_tasks_count(dagbag, current_dag_id, tasks_count):
    for dag_id in dagbag.dag_ids:
        if dag_id == current_dag_id:
            dag = dagbag.get_dag(dag_id=dag_id)
            assert len(dag.tasks) == tasks_count

