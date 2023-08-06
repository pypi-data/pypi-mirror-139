
import logging
import mailjet_rest
from . import emailer, mailjet_models

logger = logging.getLogger(__name__)

class MailjetEmailer(emailer.Emailer):
    def __init__(self,
            from_address: str,
            from_name: str,
            api_key: str,
            api_secret: str,
            version: str = "v3.1"):
        super().__init__(from_address, from_name)
        self._client = mailjet_rest.Client(auth = (api_key, api_secret), version = version)

    def send(self, subject:  str, to_email: str, text_content:  str, html_content: str, to_name:  str = "user"):
        data = mailjet_models.SendData(Messages = [
            mailjet_models.Message(
                    From = mailjet_models.Contact(
                            Email = self._from_address,
                            Name = self._from_name
                        ),
                    To = [mailjet_models.Contact(
                            Email = to_email,
                            Name = to_name
                        )],
                    Subject = subject,
                    TextPart = text_content,
                    HTMLPart = html_content,
                )
            ])

        result = self._client.send.create(data = data.dict())
        logger.info(result.json())
