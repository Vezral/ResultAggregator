import subprocess
import os
import time
import filecmp
from student_answer.models import StudentAnswer, StudentAnswerResult


# source_code_name = with .java
# source_code_path = absolute path with .java
# program_name = without .java
# program_name_path = absolute path without .java
# django_ = java file name and path that is saved on django server

# remove package name and change java class name if django renamed the uploaded file
def modify_java_file(django_source_code_path, source_code_name):
    is_duplicate = False
    django_program_name = os.path.splitext(os.path.basename(django_source_code_path))[0]
    program_name = os.path.splitext(os.path.basename(source_code_name))[0]
    if django_program_name != program_name:
        is_duplicate = True

    with open(django_source_code_path, "r+") as fd:
        code = fd.readlines()
        fd.seek(0)
        fd.truncate()
        for line in code:
            if not line.startswith("package"):
                # if django renamed the program, rename the public class
                if is_duplicate:
                    if 'public class ' + program_name in line:
                        line = line.replace(program_name, django_program_name)
                fd.write(line)


# compile the .java file in MEDIA_ROOT/competition/question and return the compiled program
def compile_java(django_source_code_path, source_code_name):
    modify_java_file(django_source_code_path, source_code_name)
    cmd = "javac " + django_source_code_path
    subprocess.run(cmd, shell=True)

    program_path = os.path.splitext(django_source_code_path)[0]
    return program_path


# execute the compiled java in MEDIA_ROOT/competition/question
def execute_java(program_path, input_file_path, input_file_name):
    working_directory = os.path.dirname(program_path)
    program_name = os.path.basename(program_path)
    cmd = "java " + program_name + " " + input_file_path
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=working_directory)
    input_file_no_extension = os.path.splitext(os.path.basename(input_file_name))[0]
    result_file_path = program_path + '__' + input_file_no_extension + '__result.txt'
    if os.path.exists(result_file_path):
        result_file_path = result_file_path[:-4] + str(int(time.time())) + '.txt'
    with open(result_file_path, 'w+') as fd:
        fd.write(result.stdout.decode("ascii").strip())  # decode byte to ascii
        fd.write(result.stderr.decode("ascii").strip())  # decode byte to ascii
    return result_file_path


# runs the above compile & execute functions + remove compiled program after executing
def run_java_program(student_answer_pk, source_code_name):
    student_answer = StudentAnswer.objects.get(pk=student_answer_pk)
    program_path = compile_java(student_answer.answer_file.path, source_code_name)
    input_file_list = student_answer.question.questionfile_set.all()
    correct_count = 0
    # run the program for each input_file in question and check if it's correct by comparing answer file
    for input_file in input_file_list:
        result_file_path = execute_java(program_path, input_file.question_file.path, input_file.question_file.name)
        is_correct = filecmp.cmp(result_file_path, input_file.answer_file.path)
        if is_correct:
            correct_count += 1
        student_answer_result = StudentAnswerResult(student_answer=student_answer, result_file=result_file_path, is_correct=is_correct)
        student_answer_result.save()

    # remove compiled program after execution
    java_exec_path = program_path + '.class'
    if os.path.exists(java_exec_path):
        os.remove(java_exec_path)

    return correct_count
