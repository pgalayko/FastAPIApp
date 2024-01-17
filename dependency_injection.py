import abc


class EmailSender(abc.ABC):
    @abc.abstractmethod
    def send(self, email: str, message: str):
        pass


class SendGridSender(EmailSender):
    def send(self, email: str, message: str):
        print(f'Sending {message} to {email} using SendGrid')


class MailchimpSender(EmailSender):
    def send(self, email: str, message: str):
        print(f'Sending {message} to {email} using Mailchimp')


# def send_email(email: str, message: str):  # Используется конкретный Sender, подменить нет возможности
#     sender = SendGridSender()
#     sender.send(email, message)

def send_email(email: str, message: str, sender: EmailSender):  # Добавили возможность использовать требуемый sender
    sender.send(email, message)


mail_chimp_sender = MailchimpSender()
send_grid_sender = SendGridSender()

send_email('', '', mail_chimp_sender)
