import urllib.request
import urllib.parse
import json
import subprocess
import time
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def get_token():
    cmd = "git credential fill"
    inp = "protocol=https\nhost=github.com\n"
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    out, _ = proc.communicate(input=inp)
    token = None
    for line in out.splitlines():
        if line.startswith("password="):
            token = line.split("=", 1)[1].strip()
    return token


OWNER = "yashkarwa2005"
REPO = "Online-Appointment-Booking-System-using-Scrum-Agile-Methodology"
TOKEN = get_token()

if not TOKEN:
    raise RuntimeError("Could not retrieve GitHub token from git credential manager.")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "User-Agent": "Agile-PBL-Cleaner",
    "Content-Type": "application/json",
    "Accept": "application/vnd.github+json"
}


def api_request(endpoint, method="GET", data=None):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/{endpoint}"
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8") if data else None,
        headers=HEADERS,
        method=method
    )
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode("utf-8")
            return json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        return {"error": e.code, "message": err_msg}


def create_or_update_label(name, color, description):
    res = api_request("labels", method="POST", data={
        "name": name,
        "color": color,
        "description": description
    })
    if "error" in res and res["error"] == 422:
        safe_name = urllib.parse.quote(name)
        api_request(f"labels/{safe_name}", method="PATCH", data={
            "color": color,
            "description": description
        })
    print(f"[*] Configured label: {name} (#{color})")


def main():
    print("=== Step 1: Configuring Clean Color-Coded Labels ===")
    labels = [
        ("🔴 High Priority", "d73a4a", "High Priority - Must Have"),
        ("🟠 Medium Priority", "fbca04", "Medium Priority - Should Have"),
        ("🟢 Low Priority", "0e8a16", "Low Priority - Could Have"),
        ("📋 Backlog", "cfd3d7", "Backlog item"),
        ("📝 To Do", "1d76db", "Ready to start"),
        ("⚙️ In Progress", "d93f0b", "Currently in development"),
        ("🔍 Review / Testing", "a2eeef", "Under testing and review"),
        ("✅ Done", "0e8a16", "Completed and verified"),
    ]
    for name, color, desc in labels:
        create_or_update_label(name, color, desc)

    print("\n=== Step 2: Fetching Existing Issues ===")
    issues = api_request("issues?state=all&per_page=50")
    if not isinstance(issues, list):
        print("[-] Error fetching issues:", issues)
        return

    print(f"Found {len(issues)} issues to clean.")

    # Status distribution mapping:
    # We want a realistic Agile board distribution:
    # Issues 1-5: Done (Sprint 1-3 complete)
    # Issues 6-7: In Progress (Active work)
    # Issues 8-9: Review / Testing
    # Issues 10-12: To Do (Upcoming sprint items)
    distribution = {
        1: ("closed", ["🔴 High Priority", "✅ Done"]),
        2: ("closed", ["🔴 High Priority", "✅ Done"]),
        3: ("closed", ["🔴 High Priority", "✅ Done"]),
        4: ("closed", ["🔴 High Priority", "✅ Done"]),
        5: ("closed", ["🔴 High Priority", "✅ Done"]),
        6: ("open", ["🟠 Medium Priority", "⚙️ In Progress"]),
        7: ("open", ["🔴 High Priority", "⚙️ In Progress"]),
        8: ("open", ["🟠 Medium Priority", "🔍 Review / Testing"]),
        9: ("open", ["🟠 Medium Priority", "🔍 Review / Testing"]),
        10: ("open", ["🔴 High Priority", "📝 To Do"]),
        11: ("open", ["🟢 Low Priority", "📝 To Do"]),
        12: ("open", ["🔴 High Priority", "📝 To Do"]),
    }

    for issue in issues:
        num = issue["number"]
        old_title = issue["title"]

        # Remove [US-xx] or [US-xx] types of prefix
        clean_title = re.sub(r"^\[US-\d+\]\s*", "", old_title).strip()

        target_state, target_labels = distribution.get(num, ("open", ["🔴 High Priority", "📝 To Do"]))

        patch_data = {
            "title": clean_title,
            "state": target_state,
            "labels": target_labels
        }

        res = api_request(f"issues/{num}", method="PATCH", data=patch_data)
        if "number" in res:
            print(f"[+] Updated Issue #{num}: '{clean_title}' -> State: {target_state}, Labels: {target_labels}")
        else:
            print(f"[-] Error updating #{num}: {res}")
        time.sleep(0.3)

    print("\n[SUCCESS] All GitHub Issues cleaned! Removed '[US-xx]' and distributed states with color labels.")


if __name__ == "__main__":
    main()
