# Dynamic-Email-Sender
Dynamic Email Sender: Sends personalized emails using multiple SMTP servers &amp; randomizes sender names, subjects, HTML bodies. Supports proxies &amp; dynamic placeholders. Easy setup &amp; customization.
Dynamic Email Sender Script

This Python script, ksMail.py, enables the sending of personalized emails using multiple SMTP servers with random selection, as well as selecting random sender names, subjects, and HTML bodies from provided lists in text files. Additionally, it supports the use of proxies for sending emails and provides placeholders for dynamic content generation within HTML templates.
Key Features:

    Versatile Email Configuration: The script dynamically selects sender names, subjects, and HTML bodies from provided lists in from_names.txt, subjects.txt, and html_bodies.txt, respectively. Users can easily customize these lists by adding or removing entries.

    Random SMTP Selection: Multiple SMTP servers can be specified in smtp_credentials.txt, and the script randomly chooses one for each email sending attempt. This enhances reliability and load distribution.

    Proxy Support: Users have the option to use proxies for SMTP connections by adding their proxy details to proxies.txt.

    Dynamic Content Generation: Placeholders within HTML templates, such as ##email##, ##date##, ##random_email##, ##random_ip##, ##random_country##, and ##random_os##, are replaced with dynamically generated data. Additionally, ##otp## can be used to generate random numbers of specified lengths for one-time passwords.

    HTML Body Separation: Multiple HTML bodies can be used by adding ##end## at the end of each HTML template, facilitating separation and customization.

Usage:

    Configure SMTP Credentials: Populate smtp_credentials.txt with SMTP server credentials in the format: host:port:username:password:from_address.

    Customize Email Data: Edit from_names.txt, subjects.txt, and html_bodies.txt to customize sender names, subjects, and HTML body templates, respectively.

    Optional: Add proxy details to proxies.txt if using proxies for SMTP connections.

    Run the Script: Execute ksMail.py. Emails will be sent to recipients listed in recipients.txt.

Placeholders:

    ##otp##<n>: Generates a random <n>-digit one-time password.
    ##email##: Replaces with the recipient's email address.
    ##date##: Replaces with the current date.
    ##random_email##: Generates a fake email address.
    ##random_ip##: Generates a random IPv4 address.
    ##random_country##: Generates a random country name.
    ##random_os##: Generates a random operating system name.
    ##end##: Indicates the end of an HTML body template.

Dependencies:

    Faker: pip install faker
    Pytz: pip install pytz

Notes:

    Ensure all required data files (subjects.txt, from_names.txt, html_bodies.txt, recipients.txt, smtp_credentials.txt) are provided in the script directory.
    For advanced usage and customization, refer to the script documentation and comments.
