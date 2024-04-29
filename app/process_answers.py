import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from advice import get_personality_traits, get_advice, save_img

def process_answers(answers):
    name = answers.get('0', '')
    chunks = [
        answers.get('3', ''),
        answers.get('4', ''),
        answers.get('5', ''),
        answers.get('6', ''),
        answers.get('7', ''),
        answers.get('8', ''),
        answers.get('9', '')
    ]

    if name:
        print(f"Hello, {name}!")

        i = answers.get('id', 0)
        personality_scores = get_personality_traits(chunks)
        print(f"Personality scores: {personality_scores}")

        advice = get_advice(personality_scores)
        save_img(i, personality_scores)

        # Save content of advice to markdown file
        with open(f'output/advice{i}.md', 'w') as f:
            f.write(advice)

        # Add the image at the end of the markdown file
        with open(f'output/advice{i}.md', 'a') as f:
            f.write(f'\n\n![alt text](imgs/img{i}.png)')

        # Send the file in an email
        email = answers.get('2', '')
        send_email(email, f'output/advice{i}.md')

def send_email(recipient, file_path):
    # Email configuration
    sender_email = "marouane.dev.debug@gmail.com"
    sender_password = "MarouaneDevDebug101"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create message
    msg = MIMEMultipart()
    msg['Subject'] = "Your Personalized Advice"
    msg['From'] = sender_email
    msg['To'] = recipient

    # Attach file
    with open(file_path, 'r') as f:
        body = f.read()
    msg.attach(MIMEText(body, 'plain'))

    # Send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        print(f"Email sent to {recipient}")

if __name__ == "__main__":
    answers = {
        '0': 'John Doe',
        '1': '24',
        '2': 'marouanetalaa101@gmail.com',
        '3': 'I hate rainy days.',
        '4': 'I love sunny weather.'
    }
    process_answers(answers)