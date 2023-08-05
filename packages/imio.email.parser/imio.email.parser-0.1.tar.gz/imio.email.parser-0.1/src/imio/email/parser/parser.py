# -*- coding: utf-8 -*-

from email.mime.text import MIMEText
from mailparser import MailParser

import base64
import email
import email2pdf
import logging
import re

logger = logging.getLogger('imio.email.parser')

# RFC 2822 local-part: dot-atom or quoted-string
# characters allowed in atom: A-Za-z0-9!#$%&'*+-/=?^_`{|}~
# RFC 2821 domain: max 255 characters
_LOCAL_RE = re.compile(r'([A-Za-z0-9!#$%&\'*+\-/=?^_`{|}~]+'
                     r'(\.[A-Za-z0-9!#$%&\'*+\-/=?^_`{|}~]+)*|'
                     r'"[^(\|")]*")@[^@]{3,255}$')

# RFC 2821 local-part: max 64 characters
# RFC 2821 domain: sequence of dot-separated labels
# characters allowed in label: A-Za-z0-9-, first is a letter
# Even though the RFC does not allow it all-numeric domains do exist
_DOMAIN_RE = re.compile(r'[^@]{1,64}@[A-Za-z0-9][A-Za-z0-9-]*'
                                r'(\.[A-Za-z0-9][A-Za-z0-9-]*)+$')


def is_email_address(address):
    if _LOCAL_RE.match(address) or _DOMAIN_RE.match(address):
        return True
    return False


def correct_addresses(lst):
    """Correct badly handled email. See test_parser..."""
    if len(lst) == 1:
        return lst
    new_lst = []
    new_parts = []
    for tup in lst:
        # not a correct address
        if is_email_address(tup[1]):
            if new_parts:
                if tup[0]:
                    new_parts.append(tup[0])
                else:
                    logger.warning("part 0 not in tup {} for addresses {}".format(tup, lst))
                new_lst.append((', '.join(new_parts), tup[1]))
                new_parts = []
            else:
                new_lst.append(tup)
        else:
            if tup[0]:
                logger.warning("part 0 in tup {} for addresses {}".format(tup, lst))
            new_parts.append(tup[1])
    return new_lst


class Parser:
    def __init__(self, message):
        """
        :type message: email.message.Message
        """
        self.initial_message = message
        self.message = self._extract_relevant_message(message)
        self.parsed_message = MailParser(self.message)

    def _extract_relevant_message(self, message):
        """
        Take the first found EML attachment,
        or use the original message.

        :type message: email.message.Message
        """
        payload = message.get_payload()
        if message.get("X-Forwarded-For") or message.get("X-Forwarded-To"):
            self.origin = "Server forward"
            return message
        if type(payload) is list:
            for part in payload:
                if (
                    part.get_content_type() == "message/rfc822"
                ):  # maybe also check for attachment filename ?
                    self.origin = "Agent forward"
                    return part.get_payload()[0]
        self.origin = "Generic inbox"
        return message

    @property
    def headers(self):
        headers = {
            "From": correct_addresses(self.parsed_message.from_),
            "To": correct_addresses(self.parsed_message.to),
            "Cc": correct_addresses(self.parsed_message.cc),
            "Subject": self.parsed_message.subject,
            "Origin": self.origin,
        }
        if self.origin == 'Agent forward':
            headers['Agent'] = correct_addresses(MailParser(self.initial_message).from_)
        return headers

    @property
    def attachments(self):
        files = []
        for attachment in self.parsed_message.attachments:
            # skip attachment declared as inline (part of message)
            if attachment.get('content-disposition') and attachment['content-disposition'] == 'inline':
                continue
            if attachment["binary"]:
                raw_file = base64.b64decode(attachment["payload"])
            else:
                raw_file = attachment["payload"].encode("utf-8")
            files.append({"filename": attachment["filename"], "content": raw_file})
        return files

    def generate_pdf(self, output_path):
        proceed, args = email2pdf.handle_args([__file__, "--no-attachments", '--headers'])
        try:
            payload, parts_already_used = email2pdf.handle_message_body(args, self.message)
        except email2pdf.FatalException as fe:
            if fe.value == 'No body parts found; aborting.':
                self.message.attach(MIMEText('<html><body><p></p></body></html>', 'html'))
                payload, parts_already_used = email2pdf.handle_message_body(args, self.message)
            else:
                raise fe
        payload = email2pdf.remove_invalid_urls(payload)
        if args.headers:
            header_info = email2pdf.get_formatted_header_info(self.message)
            payload = header_info + payload
        payload = payload.encode("UTF-8")
        email2pdf.output_body_pdf(self.message, payload, output_path)
