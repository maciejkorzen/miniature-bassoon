Paper test generator for testing candidates.

WORK IN PROGRESS

# Requirements
* `pip3 install beautifulsoup4 tabulate`

# Usage
Use `generate-fake-questions.sh` to generate some fake questions for testing purposes.

Run `test-generator.py -d directory` to generate file with questions.
_directory_ is name of directory with questions.
You can provide multiple directories. Example: `test-generator.py -d dir1 -d dir2`.

Two files will be generated:
* test-UUID-candidate.html
* test-UUID-hr.html

The first one is for candidate.
The second one has correct answers marked. You can give it to HR people so they can check test results by themselves.
_UUID_ is random ID. Each test has this UUID in file name and inside document content. Thanks to it you will be able to match version without answers with version with answers.

You can generate some tests in advance and give them to HR. They will print them and hand them out to candidates when they arrive.

# Examples
Generated test examples with fake questions.
* [Version for candidate](https://maciejkorzen.github.io/miniature-bassoon-example/test-candidate.html).
* [Version with answers](https://maciejkorzen.github.io/miniature-bassoon-example/test-hr.html).
