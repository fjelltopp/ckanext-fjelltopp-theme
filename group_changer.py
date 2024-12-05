import re
import os
import polib
import argparse


def process(input_file, singular_term, plural_term):
    """
    Process PO file replacing 'group/Group' with singular term
    and 'groups/Groups' with plural term
    """
    po = polib.pofile(input_file, encoding='utf-8')

    for entry in po:
        if not entry.msgstr:
            entry.msgstr = entry.msgid

        msgstr = entry.msgstr

        template_pattern = re.compile(r'{\s*groups?\s*}', re.IGNORECASE)
        if template_pattern.search(msgstr):
            continue

        # Replace singular forms
        msgstr = re.sub(r'\bGroup\b', singular_term.capitalize(), msgstr)
        msgstr = re.sub(r'\bgroup\b', singular_term.lower(), msgstr)

        # Replace plural forms
        msgstr = re.sub(r'\bGroups\b', plural_term.capitalize(), msgstr)
        msgstr = re.sub(r'\bgroups\b', plural_term.lower(), msgstr)

        entry.msgstr = msgstr

    po.save(input_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update group terms in PO file')
    parser.add_argument('path', help='Path to the PO file')
    parser.add_argument('singular', help='Singular term to replace "group"')
    parser.add_argument('plural', help='Plural term to replace "groups"')

    args = parser.parse_args()
    process(args.path, args.singular, args.plural)
