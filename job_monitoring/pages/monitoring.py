import taipy as tp
from taipy.gui import get_state_id, invoke_callback, Markdown
from taipy.config.config import Config
from taipy.core.job.job import Job
from runtime import App


def get_all_jobs():
    """Returns all the known jobs (as a array of fields)."""

    def _job_to_fields(job: Job) -> list[str]:
        return [
            job.submit_id,
            job.id,
            job.creation_date.strftime("%b %d %Y %H:%M:%S"),
            str(job.status),
        ]

    return [_job_to_fields(job) for job in tp.get_jobs()]


def get_all_pipelines():
    """Returns all pipelines (as an array of ids)"""
    return [
        pipeline.id
        for pipeline in Config.pipelines.values()
        if pipeline.id != "default"  # we explicitely get rid of the "default" pipeline
    ]


def get_job_by_id(id):
    """Return a job from its id"""
    found = [job for job in tp.get_jobs() if job.id == id]
    if found:
        return found[0]
    return None


def get_job_by_index(index):
    """Return a job from its index"""
    all_jobs = tp.get_jobs()
    if len(all_jobs) > index:
        return all_jobs[index]
    return None


def get_status(job: Job):
    """Get the status of the given job as string."""
    if not job:
        return None
    return job.status.name.lower()


# -----------------------------------------------------------------------------
# Callbacks / UI function

def on_style(state, index, row):
    status_index = 3
    if 'RUNNING' in row[status_index]:
        return 'blue'
    if 'COMPLETED' in row[status_index]:
        return 'green'
    if 'BLOCKED' in row[status_index]:
        return 'orange'
    if 'FAILED' in row[status_index]:
        return 'red'

def refresh_job_list(state):
    """Refresh the job list"""
    state.all_jobs = get_all_jobs()


def job_updated(state_id, pipeline, job):
    """Callback called when a job has been updated."""

    # invoke_callback allows to run a function with a GUI _state_.
    invoke_callback(App().gui, state_id, refresh_job_list, args=[])


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

    pipeline = tp.create_pipeline(pipeline_config)
    tp.subscribe_pipeline(pipeline=pipeline, callback=job_updated, params=[state_id])
    tp.submit(pipeline)


def on_table_click(state, table, action, payload):
    job_index = payload["index"]
    selected_job = get_job_by_index(job_index)
    state.selected_job = selected_job
    state.show_details_pane = True


def cancel_selected_job(state):
    job_id = state.selected_job.id
    tp.cancel_job(state.selected_job)
    state.show_details_pane = False
    refresh_job_list(state)
    state.selected_job = get_job_by_id(job_id)


def delete_selected_job(state):
    tp.delete_job(state.selected_job, force=True)
    state.show_details_pane = False
    refresh_job_list(state)


# -----------------------------------------------------------------------------
# UI Configuration

columns = {
    "0": {"title": "Submit ID"},
    "1": {"title": "Job ID"},
    "2": {"title": "Creation Date"},
    "3": {"title": "Status"},
}


# -----------------------------------------------------------------------------
# Page


page = Markdown("job_monitoring/pages/monitoring.md")
