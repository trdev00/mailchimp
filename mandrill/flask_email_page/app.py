import mandrill

from flask import Flask, render_template, request


mandrill_client = mandrill.Mandrill('YOUR MANDRILL API KEY')

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    '''
    This will create a webpage that will have text boxes to enter in email
        to and from fields and a rich text editor to create the body of the
        email.
    Once the submit button is clicked the data entered will be used to send
        an email through Mailchimp's Mandrill API.
    '''
    if request.method == 'POST':
        body_text    = request.form.get('editordata')
        from_email   = request.form.get('from_email')
        from_name    = request.form.get('from_name')
        to_email     = request.form.get('to_email')
        to_name      = request.form.get('to_name')
        subject_text = request.form.get('subject_text')

        # This is what Mandrill needs to send an email out.
        message = {
            'from_email': from_email,
            'from_name': from_name,
            'to': [{
                    'email': to_email,
                    'name': to_name,
                    'type': 'to'
                  }],
            'subject': subject_text,
            'html': body_text
        }

        # This uses the API key for Mandrill to send the email:
        # Returns a response from Mandrill.
        result = mandrill_client.messages.send(message = message)

        return render_template('submit.html', body_text = body_text, \
                from_email = from_email, subject_text = subject_text, \
                from_name = from_name, result = result)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)