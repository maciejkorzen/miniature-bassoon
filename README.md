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

# Limitations
Remeber that this test generator is not a ultimate solution for testing candidates!
It only helps in efficient way to do basic technical screening process.

# Structure of questions database
The "database" of questions is set of directories and files.
Each database has to be in specified directory. Let's assume that we have a directory named `test-questions-1`.
In this directory you have to create subdirectories for each question.
In the question subdirectory you create file named `question`. In this file you have to put question content.
In the question subdirectory you have to create directory named `answers`.
In `answers` directory you have to create directory named `1`.
In `answers/1` directory you have to create one file. This file's name is irrelevant. It can be anything. Inside this file you have to put correct answer.
In `answers` directory you have to create directory named `0`.
In `ansers/0` directory you have to create four files. Names of files are irrelevant. Name them whatever you want. Inside this files you have to put incorrect answers.
In files with question and answers you can use HTML. Files' content will be included in HTML document.

You can find example of questions database in `test2-real-questions` directory.

Directory structure example:
```
% tree test2-real-questions
test2-real-questions
├── linux-process-list
│   ├── answers
│   │   ├── 0
│   │   │   ├── ans1
│   │   │   ├── ans2
│   │   │   ├── ans3
│   │   │   └── ans4
│   │   └── 1
│   │       └── ans1
│   └── question
├── which-command-will-disable-network-access
│   ├── answers
│   │   ├── 0
│   │   │   ├── ans1
│   │   │   ├── ans2
│   │   │   ├── ans3
│   │   │   └── ans4
│   │   └── 1
│   │       └── ans1
│   └── question
└── which-one-is-nosql-database
    ├── answers
    │   ├── 0
    │   │   ├── ans1
    │   │   ├── ans2
    │   │   ├── ans3
    │   │   └── ans4
    │   └── 1
    │       └── ans1
    └── question

12 directories, 18 files
```

# Examples
Generated test examples with fake questions.
* [Version for candidate](https://maciejkorzen.github.io/miniature-bassoon-example/test-candidate.html).
* [Version with answers](https://maciejkorzen.github.io/miniature-bassoon-example/test-hr.html).
