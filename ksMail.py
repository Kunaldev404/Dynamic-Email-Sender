import random
import logging
import smtplib
from email.message import EmailMessage
from datetime import datetime
import faker
import pytz
import ssl
import sys
import threading
import time

# Initialize faker to generate fake data
fake = faker.Faker()

# Configure logging
logging.basicConfig(filename='email_sender.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to read proxies from file
def read_proxies(file_name):
    proxies = []

    try:
        with open(file_name, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split('@')
                    if len(parts) == 2:
                        username_password = parts[0].split(':')
                        host_port = parts[1].split(':')
                        if len(username_password) == 2 and len(host_port) == 2:
                            proxy = {
                                'username': username_password[0],
                                'password': username_password[1],
                                'host': host_port[0],
                                'port': host_port[1]
                            }
                            proxies.append(proxy)
                        else:
                            logging.error(f"Invalid proxy format: {line}")
                    else:
                        logging.error(f"Invalid proxy format: {line}")
    except FileNotFoundError:
        logging.error(f"File '{file_name}' not found.")

    return proxies

# Function to read data from file
def read_file(file_name):
    try:
        with open(file_name, 'r') as file:
            return file.read().strip().splitlines()
    except FileNotFoundError:
        logging.error(f"File '{file_name}' not found.")
        return []

# Function to read email data from separate files
def read_email_data():
    subjects = read_file('subjects.txt')
    from_names = read_file('from_names.txt')
    html_bodies = read_file('html_bodies.txt')
    recipients = read_file('recipients.txt')
    proxies = read_proxies('proxies.txt')

    return subjects, from_names, html_bodies, recipients, proxies

# Function to replace placeholders in HTML body
def replace_placeholders(html_body, recipient):
    # Replace ##email## with recipient's email
    html_body = html_body.replace('##email##', recipient)
    
    # Replace ##date## with current date in UTC format (mm,day,year)
    current_date = datetime.now(pytz.utc).strftime('%m,%d,%Y')
    html_body = html_body.replace('##date##', current_date)
    
    # Replace ##random_email## with a random email address
    html_body = html_body.replace('##random_email##', fake.email())

    # Replace ##random_ip## with a random IPv4 address
    html_body = html_body.replace('##random_ip##', fake.ipv4())

    # Replace ##random_country## with a random country
    html_body = html_body.replace('##random_country##', fake.country())

    # Replace ##random_os## with a random operating system
    os_list = ['Windows', 'macOS', 'Linux']
    html_body = html_body.replace('##random_os##', random.choice(os_list))

    # Replace ##random_browser## with a random browser
    browser_list = ['Chrome', 'Firefox', 'Safari', 'Edge', 'Opera']
    html_body = html_body.replace('##random_browser##', random.choice(browser_list))

    # Replace ##otp## with a random number of specified length
    def replace_otp(match):
        length = int(match.group(1))
        return str(random.randint(10 ** (length - 1), (10 ** length) - 1))

    import re
    html_body = re.sub(r'##otp##(\d+)', replace_otp, html_body)

    return html_body

# Function to send email with retry logic
def send_email_with_retry(subjects, from_names, html_bodies, recipients, proxies, smtp_credentials, retry=5):
    success_count = 0
    fail_count = 0

    smtp_index = 0

    for recipient in recipients:
        try:
            subject = random.choice(subjects)  # Randomly choose a subject
            from_name = random.choice(from_names)  # Randomly choose a from_name
            html_body = random.choice(html_bodies)  # Randomly choose an html_body
            proxy = random.choice(proxies) if proxies else None

            smtp_host, smtp_port, smtp_username, smtp_password, smtp_frommail = smtp_credentials[smtp_index]

            with smtplib.SMTP(smtp_host, smtp_port) as smtp:
                smtp.ehlo()
                smtp.starttls(context=ssl.create_default_context())
                smtp.login(smtp_username, smtp_password)

                # Sanitize header values
                subject = subject.replace('\n', '').replace('\r', '')
                from_addr = f"{from_name} <{smtp_frommail}>".replace('\n', '').replace('\r', '')
                recipient = recipient.replace('\n', '').replace('\r', '')

                msg = EmailMessage()
                msg.set_content('')  # Clear any existing content
                msg.add_alternative(replace_placeholders(html_body, recipient), subtype='html')  # Set HTML content

                msg['Subject'] = subject
                msg['From'] = from_addr
                msg['To'] = recipient

                smtp.send_message(msg)

                logging.info(f"Email sent to {recipient}")
                success_count += 1

            # Move to the next SMTP credentials
            smtp_index = (smtp_index + 1) % len(smtp_credentials)
        except Exception as e:
            logging.error(f"Failed to send email to {recipient}: {e}")
            fail_count += 1

    logging.info(f"Total emails sent: {success_count}")
    logging.info(f"Total emails failed: {fail_count}")

# Main function
def main():
    start_time = time.time()

    smtp_credentials = read_file('smtp_credentials.txt')
    smtp_credentials = [cred.split(':') for cred in smtp_credentials]

    subjects, from_names, html_bodies, recipients, proxies = read_email_data()

    if not subjects or not from_names or not html_bodies or not recipients:
        logging.error("Please make sure all necessary data files are provided.")
        return

    send_email_with_retry(subjects, from_names, html_bodies, recipients, proxies, smtp_credentials)

    end_time = time.time()
    total_time = end_time - start_time
    logging.info(f"Total time taken: {total_time:.2f} seconds")

# Run the main function
if __name__ == "__main__":
    main()