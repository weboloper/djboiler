from django.template.loader import render_to_string

def test_email():
    subject = 'Test E-Postası'
    recipient_list = ['weboloper@gmail.com']

    # E-posta şablonunu render et
    message = render_to_string('core/emails/test_email.html', {
        'username': 'Core Test Kullanıcısı',
    })

    return subject, message, recipient_list

