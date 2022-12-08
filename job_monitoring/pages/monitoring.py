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
        ]

    return [_job_to_fields(job) for job in taipy.get_jobs()]


def get_job_by_id(id):
    found = [job for job in taipy.get_jobs() if job.id == id]
    if found:
        return found[0]
    return None


def get_job_by_index(index):
    all_jobs = taipy.get_jobs()
    if len(all_jobs) > index:
        return all_jobs[index]
    return None


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
    job_to_delete = get_job_by_index(job_index)
    taipy.delete_job(job_to_delete, force=True)

    refresh_job_list(state)


def on_table_click(state, table, action, payload):
    job_index = payload["index"]
    selected_job = get_job_by_index(job_index)
    state.selected_job = selected_job
    state.show_details_pane = True


def refresh_job_list(state):
    state.all_jobs = get_all_jobs()


columns = {
    "0": {"title": "Submit ID"},
    "1": {"title": "Job ID"},
    "2": {"title": "Creation Date"},
    "3": {"title": "Status"},
}


def get_status(job: Job):
    if not job:
        return None
    return job.status.name.lower()


def cancel_selected_job(state):
    job_id = state.selected_job.id
    taipy.cancel_job(state.selected_job)
    state.show_details_pane = False
    refresh_job_list(state)
    state.selected_job = get_job_by_id(job_id)


def delete_selected_job(state):
    taipy.delete_job(state.selected_job, force=True)
    state.show_details_pane = False
    refresh_job_list(state)


page = Markdown("job_monitoring/pages/monitoring.md")
