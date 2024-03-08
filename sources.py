import os
import re
import sys
import json
import argparse
import requests

parser = argparse.ArgumentParser(
    prog = "Ubuntu Sourcer",
    description = "Lists valid deb and deb-src URLs for current Stable and LTS versions of Ubuntu",
    epilog = "If piping the output of this program, --output will be ignored and --ignore will be set"
)
parser.add_argument("--version", "-v", help = "Ubuntu release version, eg '18.04' or 'eoan'", type = str)
parser.add_argument("--ignore", "-q", help = "Ignore warnings", action = "store_true", default = False)
parser.add_argument("--output", "-o", help = "Output file", type = str)
args = parser.parse_args()

PIPING_OUT = sys.stdout
if not sys.stdout.isatty():
    args.ignore = True
    args.output = None
    if sys.stderr.isatty():
        PIPING_OUT = sys.stderr
    else:
        PIPING_OUT = None


if args.output is None and not args.ignore:
    print("\x1b[91;1mWARNING:\x1b[0m No output file specified. Output will be printed to stdout.")
    input("Press enter to continue:")
    print("\x1b[2A\x1b[0J", end = "")
elif args.output is None:
    pass
elif not os.path.isfile(args.output):
    try:
        open(args.output, "w+").write("")
    except PermissionError:
        if not args.ignore:
            print("\x1b[91;1mWARNING:\x1b[0m Directory is read-only. Output will be printed to stdout.")
            input("Press enter to continue:")
            print("\x1b[2A\x1b[0J", end = "")
elif not os.access(args.output, os.W_OK) and not args.ignore:
    print("\x1b[91;1mWARNING:\x1b[0m File is read-only. Output will be printed to stdout.")
    input("Press enter to continue:")
    print("\x1b[2A\x1b[0J", end = "")

resp = requests.get("https://raw.githubusercontent.com/VoxelPrismatic/ubuntu-sources/main/releases.json")
RELEASES = resp.json()

current_st = open("/etc/os-release").read()
current_data = {}

for line in current_st.strip().split("\n"):
    key = line.split("=", 1)[0]
    val = line.split("=", 1)[1]
    if val.startswith("\"") and val.endswith("\""):
        val = val[1:-1]
    current_data[key] = val

if current_data["ID"] != "ubuntu" and not args.ignore:
    print("\x1b[91;1mWARNING:\x1b[0m This OS does not appear to be Ubuntu.")
    print("Please be cautious when using sources outside of your distribution, things will break.")
    input("Press enter to continue:")
    print("\x1b[3A\x1b[0J", end = "")

if args.version in RELEASES:
    current_data["VERSION_ID"] = args.version
elif args.version:
    for ver in RELEASES:
        valid = RELEASES[ver].lower().split() + [RELEASES[ver].lower()]
        if args.version.lower() in valid:
            current_data["VERSION_ID"] = ver
            break
    else:
        print("\x1b[91;1mERROR:\x1b[0m That version or code name does not exist.")
        exit()

current_ver = current_data["VERSION_ID"]
current_year = int(current_ver.split(".")[0])
current_month = int(current_ver.split(".")[1])

lts_year = current_year - (current_year % 2)
lts_month = 4
lts_ver = f"{lts_year}.{lts_month:02}"

dist_years = {current_ver, lts_ver}

ARCHIVE_PATHS = [
    "",         # base
    "-updates",
    "-backports",
    "-proposed",
    "-security"
]

ARCHIVE_DOMAINS = [
    "us.archive.",
    "archive.",
    "security."
]

ARCHIVE_COMPONENTS = [
    "main",
    "partner",
    "restricted",
    "universe",
    "multiverse"
]

def validate_uri(name, path, domain, component):
    uri = f"http://{domain}ubuntu.com/ubuntu/dists/{name}/{component}/"
    breakdown = f"\x1b[93;1m{domain[:-1]} \x1b[94;1m{name}{path} \x1b[95;1m{component}\x1b[0m"
    if PIPING_OUT:
        print(f"\x1b[K~ | " + breakdown + "\r", end = "", file = PIPING_OUT)

    attempts = 0
    resp = None
    
    while resp is None:
        try:
            resp = requests.get(uri, timeout = 5)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
            attempts += 1
            if PIPING_OUT:
                print(f"\x1b[K\x1b[91;1m{attempts}\x1b[0m | {breakdown}\r", end = "", file = PIPING_OUT)

    if resp.status_code == 200:
        if PIPING_OUT:
            print("\x1b[K\x1b[92;1m\u221a\x1b[0m | " + breakdown, file = PIPING_OUT)
        return True
    
    if PIPING_OUT:
        print("\x1b[K\x1b[91;1mX\x1b[0m | " + breakdown, file = PIPING_OUT)
    return False

sources = ""
if PIPING_OUT:
    print("\n" * len(ARCHIVE_COMPONENTS), file = PIPING_OUT)

steps = len(dist_years) * len(ARCHIVE_PATHS) * len(ARCHIVE_DOMAINS)
completed = 0
depth = str(len(ARCHIVE_COMPONENTS) + 1)

for version in dist_years:
    code_name = RELEASES[version]
    build_name = code_name.split()[0].lower()
    ver_urls = []
    for path in ARCHIVE_PATHS:
        path_urls = []
        for domain in ARCHIVE_DOMAINS:
            completed += 1
            if PIPING_OUT:
                print(f"\x1b[{depth}A\x1b[0J{completed / steps:.2%}", file = PIPING_OUT)
            components = []
            for component in ARCHIVE_COMPONENTS:
                if validate_uri(build_name, path, domain, component):
                    components.append(component)
            if components:
                path_urls.append(f"http://{domain}ubuntu.com/ubuntu/ {build_name}{path} {' '.join(components)}")
        ver_urls.append(path_urls)
    if sum(len(q) for q in ver_urls):
        sources += f"# {version} - {code_name}"
        for path_urls in ver_urls:
            sources += "\ndeb " + "\ndeb ".join(path_urls)
            sources += "\ndeb-src " + "\ndeb-src ".join(path_urls)
            sources += "\n"
        sources += "\n\n\n\n"

if args.output and os.access(args.output, os.W_OK):
    open(args.output, "w+").write(sources)
    print("\x1b[93;1mDone!\x1b[0m")
    exit()

if not sys.stdout.isatty():
    print(sources)
    exit()

print(f"\x1b[{depth}A\x1b[0J", end = "")

for line in sources.split("\n"):
    if line == "":
        print()
        continue
    if line.startswith("#"):
        print("\x1b[97;2m" + line + "\x1b[0m")
        continue
    groups = re.match(r"(deb(-src)?) (http[^\s]+) ([\w-]+)(( \w+)+)", line)
    print(
        "\x1b[33m" + groups.group(1) + " "
        "\x1b[93;1m" + groups.group(3) + " "
        "\x1b[94;1m" + groups.group(4) + ""
        "\x1b[95;1m" + groups.group(5) + "\x1b[0m"
    )
