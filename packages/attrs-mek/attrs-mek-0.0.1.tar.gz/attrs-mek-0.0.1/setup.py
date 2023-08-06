import os
import re
from setuptools import setup

def fill_in_md_template():
    end_of_file_regex = re.compile(r"(# END README.*$|^.*# START README)", re.DOTALL)

    base_path = "tests/examples"
    paths = [path for path in os.listdir(base_path) if path[:7] == "section"]

    with open("README_template.md", "r") as template_file:
        md_contents = template_file.read()

        for path in paths:
            section_name = path.split("_")[0]

            with open(base_path + "/" + path, "r") as test_file:
                test_contents = test_file.read()
                parsed_content = re.sub(end_of_file_regex, "", test_contents).strip()

                replace_pattern = re.compile(fr"# {section_name}.*\n")
                md_contents = re.sub(
                    replace_pattern, f"```python\n{parsed_content}\n```\n", md_contents
                )

        with open("README.md", "w") as md_file:
            md_file.write(md_contents)

with open("attrs_mek/__init__.py", "r") as file:
    contents = file.read()

def meta(name):
    pattern = re.compile(fr"__{name}__ = \"(.*)\"")
    val = re.findall(pattern, contents)
    return val[0]

if __name__ == "__main__":
    # fill_in_md_template()

    setup(
        name=meta("title"),
        version=meta("version"),
        author=meta("author"),
        packages=['attrs_mek'],
        url=meta("url"),
        license=meta("license"),
        description=meta("description"),
        long_description=open('README.md').read(),
        long_description_content_type="text/markdown",
        install_requires=[
            "attrs",
            "pytest",
        ],
    )
