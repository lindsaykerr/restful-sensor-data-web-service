import re


class Sanitize:

    @staticmethod
    def scrub_form_input(str: str):
        if re.match(r'^[0-9A-Za-z. _@]+$', str):
            return str.strip()
        else:
            return None
