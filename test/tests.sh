#!/bin/bash

function test_file_import_command() {
    gpt ask Answer me the following question \\file{test/test_prompt.txt}
}

function test_execute_command() {
    gpt ask When I run the following command bash test/test_exec.sh: I get the following output. Can you tell me whats wrong \\execute{bash test/test_exec.sh}
}