# Mandrill works best in Python 3.6

import mandrill, requests, json, config, re, datetime

from flask import Flask, request, render_template, Markup



mandrill_client = mandrill.Mandrill(mandrill_api_key)

app = Flask(__name__)


def mandrill_template(body, preview, from_email, from_name, to_email, \
                      to_name, subject):
    '''
    Constructs a MailChimp Mandrill email API call
    '''
    template_content = [{
            "name"   : "main",
            "content":  body
        },
        {
            "name"   : "prev_text",
            "content":  preview
        }]

    message = {
            'from_email': from_email,
            'from_name' : from_name,

            'to': [{
                    'email':  to_email,
                    'name' :  to_name,
                    'type' : 'to'
                }],

            'subject': subject,
        }

    # Set the time when Mandrill will send the emails.
    send_time = \
        str(datetime.datetime.now() + datetime.timedelta(minutes = 1))[:19]

    # Sends email using MailChimp Mandrill API:
    result = mandrill_client.messages.send_template(
             template_name    = 'mar_committee_automated',
             template_content = template_content,
             message          = message, async = False,
             ip_pool          = 'Main Pool',
             send_at          = send_time)

    return result



@app.route('/compose/', methods=['GET', 'POST'])
def compose():
    '''
    Send emails through MailChimp Mandrill API.
    '''

    # Create blank list to hold MailChimp Results:
    result_list = []

    # When email data forms are filled out and the submit button it clicked:
    if request.method == 'POST':

        # Get text entered in forms:
        body_text    = request.form.get('body_text')
        from_email   = request.form.get('from_email')
        from_name    = request.form.get('from_name')
        subject_text = request.form.get('subject_text')
        prev_text    = request.form.get('prev_text')

        # Check if email address is valid:
        regx_email = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+' + \
                     '(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'

        match = re.match(regx_email, from_email)

        # If email address is not valid, assign the default email:
        if match == None or from_email == '':
            from_email = 'test@default.com'

        # If no body text return error and go back:
        if len(body_text) < 6:
            return render_template('error.html')

        # Add additional test to the end of the email body:
        body_text_link = body_text + \
            '<br /> <br />' + \
            'TEXT AT END OF BODY HERE'

        body_text_markup = Markup(body_text_link)

        # MailChimp Mandrill email API call:
        mandrill_result = mandrill_template(body_text_markup, prev_text, \
                from_email, from_name, mem_email, mem_name, subject_text)

        # Log results from MailChimp Mandrill API:
        result_list.append(mandrill_result)

        # Return successful email send page which redirects to blank
        #   compose page:
        return render_template('submit.html', result_list = result_list)

    return render_template('compose.html')



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)