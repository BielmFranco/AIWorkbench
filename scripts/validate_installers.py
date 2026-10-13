#!/usr/bin/env python3
from pathlib import Path
import shutil, subprocess, sys, tempfile
from zipfile import ZipFile

import package_skills

root = Path(__file__).resolve().parents[1]
errors = []
expected = {path.name for path in package_skills.available()}
bash = shutil.which("bash")
if not bash and sys.platform == "win32":
    for candidate in (Path("C:/Program Files/Git/bin/bash.exe"), Path("C:/Program Files/Git/usr/bin/bash.exe")):
        if candidate.is_file():
            bash = str(candidate); break
if not bash:
    errors.append("Bash executable not found")
else:
    run = subprocess.run([bash, "-n", str(root / "scripts" / "install.sh")], text=True, capture_output=True)
    if run.returncode: errors.append("install.sh: " + (run.stderr or run.stdout).strip())

powershell = shutil.which("pwsh") or shutil.which("powershell")
if not powershell:
    errors.append("PowerShell executable not found")
else:
    script = str(root / "scripts" / "install.ps1").replace("'", "''")
    command = "$tokens=$null;$errors=$null;[System.Management.Automation.Language.Parser]::ParseFile('" + script + "',[ref]$tokens,[ref]$errors)|Out-Null;if($errors.Count){$errors|ForEach-Object{Write-Error $_};exit 1}"
    run = subprocess.run([powershell, "-NoProfile", "-Command", command], text=True, capture_output=True)
    if run.returncode: errors.append("install.ps1: " + (run.stderr or run.stdout).strip())
if not errors:
    with tempfile.TemporaryDirectory(prefix="aiworkbench-install-") as temporary:
        temporary_root = Path(temporary)
        ps_target = temporary_root / "powershell"
        run = subprocess.run([powershell, "-NoProfile", "-File", str(root / "scripts" / "install.ps1"), "-Target", "codex", "-InstallPath", str(ps_target)], text=True, capture_output=True)
        ps_count = len([path for path in ps_target.iterdir() if path.is_dir()]) if ps_target.is_dir() else 0
        if run.returncode or ps_count != len(expected) or {p.name for p in ps_target.iterdir() if p.is_dir()} != expected:
            errors.append("install.ps1 copy test failed: " + (run.stderr or run.stdout).strip())
        bash_target = temporary_root / "bash"
        if sys.platform == "win32":
            command = 'export PATH=/usr/bin:/bin:$PATH; script=$(cygpath -u "$1"); destination=$(cygpath -u "$2"); "$script" codex all "$destination"'
            run = subprocess.run([bash, "-lc", command, "aiworkbench", str(root / "scripts" / "install.sh"), str(bash_target)], text=True, capture_output=True)
        else:
            run = subprocess.run([bash, str(root / "scripts" / "install.sh"), "codex", "all", str(bash_target)], text=True, capture_output=True)
        bash_count = len([path for path in bash_target.iterdir() if path.is_dir()]) if bash_target.is_dir() else 0
        if run.returncode or bash_count != len(expected) or {p.name for p in bash_target.iterdir() if p.is_dir()} != expected:
            errors.append("install.sh copy test failed: " + (run.stderr or run.stdout).strip())
        package_skills.DIST = temporary_root / "zips"
        for skill in package_skills.available():
            archive_path = package_skills.package(skill)
            with ZipFile(archive_path) as archive:
                names = archive.namelist()
                if f"{skill.name}/SKILL.md" not in names or any(not name.startswith(skill.name + "/") for name in names):
                    errors.append(skill.name + ": ZIP must contain one top-level skill folder")
if errors:
    print("\n".join("ERROR " + error for error in errors)); sys.exit(1)
print(f"OK: installers and portable ZIPs ({len(expected)}/{len(expected)})")
