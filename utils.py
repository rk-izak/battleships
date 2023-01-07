def is_ans_in_list(answer, ans_list, message):
    if answer not in ans_list:
        while True:
                print("\n"+message)
                answer = str(input("Please, try again." + "\n")).lower()
                if answer not in ans_list:
                        continue
                else:
                        break

    return answer