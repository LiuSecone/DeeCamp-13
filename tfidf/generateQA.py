# encoding=utf-8

sensitive_words = []
def load_sensitive_word():
    global sensitive_words
    with open('dataset/sensitive.txt', 'r', encoding='utf-8') as rf:
        sensitive_words = rf.readlines()
        sensitive_words = [word.strip() for word in sensitive_words]
        print(sensitive_words)


def handleDataset(inputName,outputQuestion,outputAnswer):
    global sensitive_words
    # 处理数据
    questions = open(outputQuestion, 'w', encoding='utf-8')
    answers = open(outputAnswer, 'w', encoding='utf-8')
    i =  0
    with open(inputName, 'r', encoding='utf-8') as rf:
        line = rf.readline()
        while line:
            qa = line.split(',')
            if len(qa) == 2:
                i += 1
                questions.write(qa[0].strip()+'\n')
                answers.write(qa[1].strip()+'\n')
                if i >300000:
                    break
            line = rf.readline()
    questions.close()
    answers.close()

if __name__ == '__main__':
    load_sensitive_word()
    inputName = 'dataset/zhihu.csv'
    outputQuestion = 'dataset/question.txt'
    outputAnswer = 'dataset/answer.txt'
    handleDataset(inputName,outputQuestion,outputAnswer)