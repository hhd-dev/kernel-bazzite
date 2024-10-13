URL = "https://api.github.com/repos/hhd-dev/linux-bazzite/releases"

import requests
import sys
import datetime

contributors = {"antheas": "Antheas Kapenekakis <git@antheas.dev>"}

# * Wed Aug 28 2024 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.11.0-0.rc5.86987d84b968.45]
# - redhat: include resolve_btfids in kernel-devel (Jan Stancek)
# - redhat: workaround CKI cross compilation for scripts (Jan Stancek)
# - spec: fix "unexpected argument to non-parametric macro" warnings (Jan Stancek)
# - Linux v6.11.0-0.rc5.86987d84b968


def main():
    res = requests.get(URL)
    data = res.json()

    out = ""

    for release in data:
        # Wed Aug 28 2024
        date = datetime.datetime.strptime(
            release["published_at"], "%Y-%m-%dT%H:%M:%SZ"
        ).strftime("%a %b %d %Y")
        author = release["author"]["login"]
        rel = release["tag_name"]

        out += f"* {date} {contributors.get(author, author)} [{rel}]\n"
        out += f"- {release['name'].replace(rel + ": ", '')}\n"

        body_lines = release["body"].split("\n")
        for line in body_lines:
            parts = line.split(" ")
            buf = ""
            for part in parts:
                if len(buf) + len(part) + 1 > 80 and not part.startswith("http"):
                    out += f" {buf}\n"
                    buf = part
                else:
                    buf += f" {part}"
            if buf:
                out += f" {buf}\n"
        out += "\n"

    with open("kernel.spec", "r") as f:
        spec = f.read()

    spec = spec.replace("%changelog", "%changelog\n" + out)

    with open("kernel.spec", "w") as f:
        f.write(spec)

    print(f"Wrote changelog:\n{out}")


if __name__ == "__main__":
    for i in range(3):
        try:
            main()
            break
        except Exception as e:
            print(f"Error:\n{e}. Retrying...", file=sys.stderr)
