from competition.models import Competition


# this function will returns a list containing:
# Rank / Student ID / Name / Solved / Time / <List of questions' Attempts / Solved> / Total Attempt / Solved
def generate_competition_table(pk):
    competition = Competition.objects.get(pk=pk)
    student_list = competition.student_set.all()
    question_list = competition.question_set.all()
    table = []
    result = []

    # prepare header for table
    header = ['Rank', 'Name', 'Solved', 'Time']
    for index, question in enumerate(question_list, start=1):
        if index == 1:
            header.append('{} (Attempts / Solved Time)'.format(index))
        else:
            header.append(index)
    header.append('Total Attempt / Solved')

    # prepare student's result
    for student in student_list:
        student_id = student.id
        student_name = student.user.username
        total_attempt = 0
        total_solved = 0
        total_time = 0
        question_attempt_result = []
        # for each question, get the latest student_answer and check if it's correct
        for question in question_list:
            student_answer_list = student.studentanswer_set.filter(question=question).order_by('-submission_time')
            num_of_attempts = student_answer_list.count()
            total_attempt += num_of_attempts
            time_taken = None
            if student_answer_list.count() > 0:
                latest_student_answer = student_answer_list[0]
                # if correct, +1 to total_solved and calculate time_difference
                if latest_student_answer.solved:
                    total_solved += 1
                    time_difference = latest_student_answer.submission_time - competition.start_time
                    time_taken = int(time_difference.seconds)  # divide 60 for minutes, etc
                    total_time += time_taken
            # if the student hasn't submitted an answer, put '--' as placeholder
            if time_taken is None:
                time_taken = '--'
            question_attempt_result.append('{}/{}'.format(num_of_attempts, time_taken))
        student_data = [student_id, student_name, total_solved, total_time]
        student_data += question_attempt_result
        student_data.append('{}/{}'.format(total_attempt, total_solved))
        result.append(student_data)

    result = sorted(result, key=lambda x: (-x[2], x[3]))  # sort by descending # of solved, then ascending time

    # formatting the actual table that is returned
    table.append(header)
    for index, student_data in enumerate(result, start=1):
        formatted_table = [index]  # enumerate index is used to display ranking
        formatted_table += student_data
        table.append(formatted_table)

    # if no student, add filler
    if len(result) == 0:
        filler = ['--', '--', '--', '--']
        for i in range(question_list.count()):
            filler.append('--')
        filler.append('--/--')
        table.append(filler)

    return table
