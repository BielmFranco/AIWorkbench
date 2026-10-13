"""Simulation for runner mechanics only; not a model or an efficacy benchmark."""
import argparse
import json
from pathlib import Path
import shutil
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--controls", type=Path, required=True)
args = parser.parse_args()
request = json.load(sys.stdin)
name = request["case_id"].removesuffix("-normal").removesuffix("-injected")
source = args.controls / name / "good"
for artifact in source.iterdir():
    if artifact.is_file() and artifact.suffix in (".json", ".py"):
        shutil.copyfile(artifact, Path(request["output_dir"]) / artifact.name)
Path(request["observation_path"]).write_text(json.dumps({"adapter_kind":"simulation","model":None,"usage":None,"capture_complete":False}), encoding="utf-8")
