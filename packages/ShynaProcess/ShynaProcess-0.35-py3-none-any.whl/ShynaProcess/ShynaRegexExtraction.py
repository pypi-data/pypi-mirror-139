import re


class ShynaRegexExtraction:
    """"
    Define string first and then run the needed method(s):
    re_for_cr_db_from_email_body
    get_link_and_data_from_summary
    clean_apostrophe
    """
    input_str = ""

    def re_for_cr_db_from_email_body(self):
        """Extract the Credit and Debit amount from the email's body"""
        regex = r"(.(r).(n))"
        subst = ''
        result = re.sub(regex, subst, self.input_str, 0, re.MULTILINE)
        if result:
            final = str(str(result).split('Dear Customer,')[-1]).split('\n \n Warm')
            if str(final[0]).__contains__('credited to A/c'):
                final_stmt = str(final[0]).split('credited to A/c')[0]
                return "+" + final_stmt.strip('\n \n')
            elif str(final[0]).__contains__('debited from account'):
                final_stmt = str(final[0]).split('debited from account')[0]
                return "-" + final_stmt.strip('\n \n')

    def get_link_and_data_from_summary(self):
        """return news summary and link"""
        try:
            row = []
            regex = r"(')"
            if re.findall(r'(https?://\S+)', self.input_str):
                ans = re.findall(r'(https?://\S+)', self.input_str)
                for rows in ans:
                    rows = rows.strip('"><img')
                    row.append(rows)
            else:
                row.append('empty link')
            link = row[0]
            if self.input_str.split('</a>')[-1]:
                split_data = self.input_str.split('</a>')[-1]
                data = re.sub(regex, "", split_data, 0, re.MULTILINE)
                if data
            else:
                data = 'No summary found'
            return link, data
        except Exception as e:
            print(e)
            pass

    def clean_apostrophe(self):
        """Remove apostrophe from the string"""
        try:
            regex = r"(')"
            self.input_str = re.sub(regex, "", self.input_str, 0, re.MULTILINE)
            return self.input_str
        except Exception as e:
            print(e)

    def re_wake_me_up_at(self):
        try:
            regex = r"(wake me up at)"
            matches = re.finditer(regex, str(self.input_str).lower(), re.MULTILINE)
            for matchNum, match in enumerate(matches, start=1):
                matches = match.group()
                if len(str(matches)) > 0:
                    return True
                else:
                    return False
        except Exception as e:
            print(e)
            return False

    def re_let_me_know(self):
        try:
            regex = r"(let me know when it is)"
            matches = re.finditer(regex, str(self.input_str).lower(), re.MULTILINE)
            for matchNum, match in enumerate(matches, start=1):
                matches = match.group()
                if len(str(matches)) > 0:
                    return True
                else:
                    return False
        except Exception as e:
            print(e)
            return False

    def re_set_alarm(self):
        try:
            regex = r"(alarm)"
            matches = re.finditer(regex, str(self.input_str).lower(), re.MULTILINE)
            for matchNum, match in enumerate(matches, start=1):
                matches = match.group()
                if len(str(matches)) > 0:
                    return True
                else:
                    return False
        except Exception as e:
            print(e)
            return False

    def re_set_reminder(self):
        try:
            regex = r"(remind me| reminder|remember)"
            matches = re.finditer(regex, str(self.input_str).lower(), re.MULTILINE)
            for matchNum, match in enumerate(matches, start=1):
                matches = match.group()
                if len(str(matches)) > 0:
                    return True
                else:
                    return False
        except Exception as e:
            print(e)
            return False

