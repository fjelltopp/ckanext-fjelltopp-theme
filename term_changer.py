import re
import os
import polib
import argparse


def process(input_file, source_singular, source_plural, new_singular, new_plural):
    """
    Process PO file replacing source terms with new terms.

    Args:
        input_file (str): Path to the PO file
        source_singular (str): Original singular term to be replaced (e.g., 'group' or 'person')
        source_plural (str): Original plural term to be replaced (e.g., 'groups' or 'people')
        new_singular (str): New singular term to use as replacement
        new_plural (str): New plural term to use as replacement
    """
    po = polib.pofile(input_file, encoding='utf-8')

    for entry in po:
        if not entry.msgstr:
            entry.msgstr = entry.msgid

        msgstr = entry.msgstr

        has_template = False
        template_content = None
        # Check for template variables
        template_pattern = re.compile(r'{\s*(' + re.escape(source_singular) + '|' +
                                      re.escape(source_plural) + r')\s*}')

        if template_match := template_pattern.search(msgstr):
            has_template = True
            template_content = template_match.group()
            msgstr = msgstr.replace(template_content, '###########')

        # Replace singular forms (both capitalized and lowercase)
        msgstr = re.sub(rf'\b{source_singular.capitalize()}\b', new_singular.capitalize(), msgstr)
        msgstr = re.sub(rf'\b{source_singular.lower()}\b', new_singular.lower(), msgstr)

        # Replace plural forms (both capitalized and lowercase)
        msgstr = re.sub(rf'\b{source_plural.capitalize()}\b', new_plural.capitalize(), msgstr)
        msgstr = re.sub(rf'\b{source_plural.lower()}\b', new_plural.lower(), msgstr)


        if has_template:
            msgstr = msgstr.replace('###########', template_content)

        entry.msgstr = msgstr

    po.save(input_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update terms in PO file')
    parser.add_argument('path', help='Path to the PO file')
    parser.add_argument('source_singular', help='Original singular term to replace (e.g., "group" or "person")')
    parser.add_argument('source_plural', help='Original plural term to replace (e.g., "groups" or "people")')
    parser.add_argument('new_singular', help='New singular term for replacement')
    parser.add_argument('new_plural', help='New plural term for replacement')

    args = parser.parse_args()
    process(args.path, args.source_singular, args.source_plural,
            args.new_singular, args.new_plural)
