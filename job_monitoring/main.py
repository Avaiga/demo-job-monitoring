from runtime import App
from pages import root, monitoring
import taipy
from taipy.config.config import Config
from taipy.gui import Gui
import os

# Variables for bindings
all_jobs = []
show_dialog_run_pipeline = False
selected_pipeline = None
show_details_pane = False
selected_job = None


if __name__ == "__main__":
    # Initialize Taipy objects
    Config.configure_job_executions(mode="standalone", nb_of_workers=4)
    Config.load("app.config.toml")
    App().core = taipy.Core()
    App().gui = Gui(pages={"/": root.page, "monitoring": monitoring.page})

    # Start the app
    App().start(
        title="Job Monitoring Demo",
        port=os.environ.get("PORT", "8080"),
        dark_mode=False,
        css_file="app",
    )
