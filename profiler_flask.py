import os
import sqlite3 as sql
import datetime
from flask import Flask, request, render_template
import profiler_main as fpm

CWD = os.getcwd()

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('index_p.html')

@app.route('/profile_upload', methods = ['POST'])
def success():
    if request.method == 'POST':
        # Save file to temp drive
        f = request.files['file']
        fname = os.path.join(CWD, '01_profiler', 'temp', f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{f.filename}")
        f.save(fname)
        print(f"temp file {fname}")

        json_profile = fpm.load_profile(fname)
        wf_id = fpm.write_profile_to_profiler_inputs(json_profile)

        try:
            os.remove(fname)
            print(f"deleted {fname}")
        except Exception as e:
            print(f"ERR: {e} for {fname}")

        return render_template("profile_upload_success.html", fname = f.filename, workflow_id = wf_id)


@app.route('/features/<int:workflow_id>', methods = ['POST', 'GET']) #/<int:workflow_id>')
#def profile_dataset(workflow_id):
def profile_dataset(workflow_id):
    wf = workflow_id
    fpm.write_to_profiler_features(wf)
    # TODO: Run python functions required to populate profiler_features and profiler_output tables &
    #  display the profiler.html page
    return render_template("profiler.html")# , workflow_id=workflow_id)


if __name__ == '__main__':
    app.run(debug=True)