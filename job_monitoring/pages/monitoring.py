import taipy
from taipy.gui import get_state_id, invoke_callback, Markdown
from taipy.config.config import Config
from taipy.core.job.job import Job
from runtime import App


def get_all_jobs():
    """Returns all the known jobs as a array of fields."""

    def _job_to_fields(job: Job) -> list[str]:
        return [
            job.submit_id,
            job.id,
            job.creation_date.strftime("%b %d %Y %H:%M:%S"),
            str(job.status),
            False,
        ]

    return [_job_to_fields(job) for job in taipy.get_jobs()]


# -----------------------------------------------------------------------------
# Dialog "Run pipeline"


def job_updated(state_id, pipeline, job):
    """Callback called when a job has been updated."""

    # If job is already in the list
    def _update_job(state, new_job):
        # Refresh the table
        state.all_jobs = get_all_jobs()

    # invoke_callback allows to run a function with a GUI _state_.
    invoke_callback(App().gui, state_id, _update_job, args=[job.id])


def open_run_pipeline_dialog(state):
    """Opens the 'Run pipeline...' dialog."""
    state.show_dialog_run_pipeline = True


def close_run_pipeline_dialog(state):
    """Closes the 'Run pipeline...' dialog."""
    state.show_dialog_run_pipeline = False


def run_pipeline(state):
    """Runs a pipeline action."""

    # We need to pass the state ID so that it can be restored in the job_updated listener:
    state_id = get_state_id(state)

    # Get selected pipeline config:
    selected = state.selected_pipeline
    pipeline_config = Config.pipelines[selected]
    if not pipeline_config:
        raise Exception(f"unknown pipeline config: {selected}")

    # Close the dialog
    close_run_pipeline_dialog(state)

    pipeline = taipy.create_pipeline(pipeline_config)
    taipy.subscribe_pipeline(pipeline=pipeline, callback=job_updated, params=[state_id])
    taipy.submit(pipeline)


def all_pipelines():
    return [
        pipeline.id
        for pipeline in Config.pipelines.values()
        if pipeline.id != "default"
    ]


def on_table_edit(state, var_name, action, payload):
    job_index = payload["index"]
    column_index = payload["col"]

    # Marker for cancellation
    if column_index == "4":
        if payload["user_value"]:
            job_to_cancel = taipy.get_jobs()[job_index]
            taipy.cancel_job(job_to_cancel.id)

    # Refresh the table
    refresh_job_list(state)


def on_table_delete(state, var_name, action, payload):
    job_index = payload["index"]
    job_to_delete = taipy.get_jobs()[job_index]
    taipy.delete_job(job_to_delete, force=True)
    # Refresh the table
    refresh_job_list(state)


def refresh_job_list(state):
    state.all_jobs = get_all_jobs()


columns = {
    "0": {"title": "Submit ID"},
    "1": {"title": "Job ID"},
    "2": {"title": "Creation Date"},
    "3": {"title": "Status"},
    "4": {"title": "Cancel"},
}

page_md = """
<|{all_jobs}|table|columns={columns}|width='100%'|editable=columns[4]|on_edit={on_table_edit}|on_delete={on_table_delete}|>

<|Refresh List|button|on_action={refresh_job_list}|>
<|Run Pipeline...|button|on_action={open_run_pipeline_dialog}|>
<|{show_dialog_run_pipeline}|dialog|title=Run pipeline...|

<|{selected_pipeline}|selector|lov={all_pipelines()}|>

<|Run|button|on_action={run_pipeline}|>
<|Cancel|button|on_action={close_run_pipeline_dialog}|>
|>
"""

page = Markdown(page_md)
