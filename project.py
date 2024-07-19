import openai
import random
import re
import sys
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


class Topics():
    def __init__(self):
        self.countst = {"history": 0,
                        "geography": 0,
                        "worldwide literature": 0,
                        "math": 0,
                        "english": 0,
                        "space": 0,
                        "psychology": 0,
                        "biology": 0,
                        "programming": 0,
                        'chemistry': 0}
        self.questions = {"history": [],
                          "geography": [],
                          "worldwide literature": [],
                          "math": [],
                          "english": [],
                          "space": [],
                          "psychology": [],
                          "biology": [],
                          "programming": [],
                          'chemistry': []}


class Player:
    def __init__(self):
        self.name = input("What is your name? ")
        self.scores = {"history": 0,
                       "geography": 0,
                       "worldwide literature": 0,
                       "math": 0,
                       "english": 0,
                       "space": 0,
                       "psychology": 0,
                       "biology": 0,
                       "programming": 0,
                       'chemistry': 0}

    def __str__(self):
        print(f"Player {self.name} with {self.score}")

    def get_best_score(self):
        return max(self.scores.values())


def create_message(topic, topics):

    message = f"""Give me 5 trivia questions and their answers on the topic of {topic}. Each question should have A, B, C and D choices. A random letter needs to be correct for each question.
    Your response should be in this format:
    Question 1: <question>
    Choice A:
    Choice B:
    Choice C:
    Choice D:
    Answer 1: <A/B/C/D>
    Question 2: <question>
    Choice A:
    Choice B:
    Choice C:
    Choice D:
    Answer 2: <A/B/C/D>
    ...
    """

    if topics.countst[topic] > 0:
        message = f"""Give me 5 trivia questions and their answers on the topic of {topic}. Each question should have A, B, C and D choices. A random letter needs to be correct for each question.
        Don't use the following questions:
        {'\n'.join(topics.questions[topic])}

        Your response should be in this format:
        Question 1: <question>
        Choice A:
        Choice B:
        Choice C:
        Choice D:
        Answer 1: <A/B/C/D>
        Question 2: <question>
        Choice A
        Choice B:
        Choice C:
        Choice D:
        Answer 2: <A/B/C/D>
        ...
        """
    return message


def extract_everything(outputf):
    questionRegex = re.compile(r"Question \d:.*")
    matchQuestion = re.findall(questionRegex, outputf)

    aRegex = re.compile(r"Choice A: .*")
    matchA = re.findall(aRegex, outputf)

    bRegex = re.compile(r"Choice B: .*")
    matchB = re.findall(bRegex, outputf)

    cRegex = re.compile(r"Choice C: .*")
    matchC = re.findall(cRegex, outputf)

    dRegex = re.compile(r"Choice D: .*")
    matchD = re.findall(dRegex, outputf)

    answerRegex = re.compile(r"Answer \d: (A|B|C|D)")
    matchAnswer = re.findall(answerRegex, outputf)

    output_dict = {
        "question": matchQuestion,
        "A": matchA,
        "B": matchB,
        "C": matchC,
        "D": matchD,
        "Answer": matchAnswer,
    }

    return output_dict


def loop(output_dict, player, topic):
    current_score = 0
    for i in range(5):

        print(output_dict["question"][i])
        print(output_dict['A'][i])
        print(output_dict['B'][i])
        print(output_dict['C'][i])
        print(output_dict['D'][i])

        us_in = input("Choose one (A|B|C|D) :")

        if us_in.upper() == output_dict["Answer"][i].upper():
            print("Correct")
            current_score += 1
        else:
            print(f"Wrong. The right answer is {output_dict['Answer'][i]}")

    print(f"You got {current_score}/5")

    if current_score > player.scores[topic]:
        player.scores[topic] = current_score
    print(f"This topic's score is {player.scores[topic]}")


def choose_topic():
    topics = [
        "history",
        "geography",
        "worldwide literature",
        "math",
        "english",
        "space",
        "psychology",
        "biology",
        "programming",
        'chemistry'
    ]

    selected_topics = random.sample(topics, 3)
    print(f"Choose one of those topics: {', '.join(selected_topics)}.")

    user_input = input("Your choice: ")
    while user_input.lower() not in selected_topics:
        print(f"Choose only one of these topics: {
              ', '.join(selected_topics)}.")
        user_input = input("Your choice: ")
    return user_input


def ask_chatgpt(message):
    max_tries = 3
    tried = 0
    try:
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}],
            temperature=1,
        )
    except Exception as e:
        print(e)
        tried += 1

        if tried == max_tries:
            sys.exit()

    return completion.choices[0].message.content


def main():
    player1 = Player()
    topics = Topics()
    print("Hello", player1.name)

    while True:
        topic = choose_topic()

        print("please wait a sec...")
        message = create_message(topic, topics)
        outputf = ask_chatgpt(message)
        output_data = extract_everything(outputf)

        topics.questions[topic] += (output_data['question'])
        topics.countst[topic] += 1

        loop(output_data, player1, topic)
        print("Do you want to continue? (Yes/No)")
        your_final = input().lower()
        if your_final.lower() == "no":
            best_score = player1.get_best_score()
            print(f"Your current heighest score is {best_score}")
            sys.exit("See you soon , bye!")


if __name__ == '__main__':
    main()

