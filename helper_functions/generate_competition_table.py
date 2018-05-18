from competition.models import Competition


def generate_competition_table(pk):
    competition = Competition.objects.get(pk=pk)
    student_list = competition.student_set.all()
    question_list = competition.question_set.all()
    table = []
    result = []

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
        for question in question_list:
            student_answer_list = student.studentanswer_set.filter(question=question).order_by('-submission_time')
            num_of_attempts = student_answer_list.count()
            total_attempt += num_of_attempts
            time_taken = None
            if student_answer_list.count() > 0:
                latest_student_answer = student_answer_list[0]
                if latest_student_answer.solved:
                    total_solved += 1
                    time_difference = latest_student_answer.submission_time - competition.start_time
                    time_taken = time_difference.seconds
                    total_time += time_taken
            if time_taken is None:
                time_taken = '--'
            question_attempt_result.append('{}/{}'.format(num_of_attempts, time_taken))
        student_data = [student_id, student_name, total_solved, total_time]
        student_data += question_attempt_result
        student_data.append('{}/{}'.format(total_attempt, total_solved))
        result.append(student_data)

    result = sorted(result, key=lambda x: (-x[2], x[3])) # sort by descending # of solved, then ascending time

    table.append(header)
    for index, student_data in enumerate(result, start=1):
        formatted_table = [index]
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
