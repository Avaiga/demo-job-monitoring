<|{all_jobs}|table|columns={columns}|width='100%'|on_action={on_table_click}|>
<|Refresh List|button|on_action={refresh_job_list}|>
<|Run Pipeline...|button|on_action={open_run_pipeline_dialog}|>

<|{show_dialog_run_pipeline}|dialog|title=Run pipeline...|
<|{selected_pipeline}|selector|lov={get_all_pipelines()}|>
<|Run|button|on_action={run_pipeline}|>
<|Cancel|button|on_action={close_run_pipeline_dialog}|>
|>
<|{show_details_pane}|pane|

# Job Details <|Delete|button|on_action=delete_selected_job|> <|Cancel|button|on_action=cancel_selected_job|>

<|layout|columns=1 1|
<|part|class_name=card|
## Task
<|{selected_job.task.config_id}|>
|>

<|part|class_name=card|
## Status
<|{get_status(selected_job)}|>
|>
|>

<|part|class_name=card|
## ID
<|{selected_job.id}|>
|>

<|part|class_name=card|
## Submission ID
<|{selected_job.submit_id}|>
|>

<|part|class_name=card|
## Creation Date
<|{selected_job.creation_date.strftime("%b %d %y %H:%M:%S")}|>
|>

<|part|class_name=card|
## Stacktrace
<|{"\n".join(selected_job.stacktrace)}|class_name=code|>
|>

----


|>
