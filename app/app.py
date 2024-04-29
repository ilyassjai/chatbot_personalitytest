from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# List of questions
questions = [
    "What is your name?",
    "How old are you?",
    "What is your email?",
    "Have you experienced a week or longer of lower-than-usual interest in activities that you usually enjoy? Examples might include work, exercise, or hobbies.",
    "Could you tell me about any times over the past few months that you’ve been bothered by low feelings, stress, or sadness?",
    "Tell me about how confident you have been feeling in your capabilities recently.",
    "Can you tell me about your hopes and dreams for the future? What feelings have you had recently about working toward those goals?",
    "Describe how ‘supported’ you feel by others around you – your friends, family, or otherwise.",
    "Tell me about any important activities or projects that you’ve been involved with recently. How much enjoyment do you get from these?",
    "Do feelings of anxiety or discomfort around others bother you?"
]

# Dictionary to store answers
answers = {}

# Counter for answer IDs
answer_id_counter = 1

@app.route('/')
def index():
    return render_template('index.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    global answers, answer_id_counter
    new_answers = request.get_json()
    # Assign a unique ID to each submission
    new_answers['id'] = answer_id_counter
    # Update answer ID counter
    answer_id_counter += 1
    # Insert new answers at the beginning of the dictionary
    answers = {str(new_answers['id']): new_answers, **answers}
    # Save answers to a JSON file
    with open('answers.json', 'w') as f:
        f.write(jsonify(answers).get_data(as_text=True))
    return 'Answers submitted successfully'

if __name__ == '__main__':
    app.run(debug=True)
