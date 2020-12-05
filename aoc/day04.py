from arpeggio import PTNodeVisitor, visit_parse_tree
from arpeggio.cleanpeg import ParserPEG
from marshmallow import Schema, ValidationError, fields, validate

from .registry import register

grammar = r'''
    passports = passport (nl nl passport)* nl+ EOF
    passport = field (field_sep field)*
    field_sep = nl / ws
    field = key ":" value
    value = r'[^ \n]+'
    key = letter+
    letter = r'[a-z]'
    ws = r'[ ]+'
    nl = r'[\r\n]'
'''


class PassportVisitor(PTNodeVisitor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def visit_passports(self, node, children):
        return children

    def visit_passport(self, node, children):
        return dict(iter(children))

    def visit_field(self, node, children):
        return children

    def visit_key(self, node, children):
        return ''.join(children)

    def visit_ws(self, node, children):
        pass

    def visit_nl(self, node, children):
        pass


def validate_height(hgt):
    if hgt.endswith('cm'):
        try:
            n = int(hgt[:-2])
        except ValueError:
            raise ValidationError('Invalid height')

        if n < 150 or n > 193:
            raise ValidationError('Height outside range')
    elif hgt.endswith('in'):
        try:
            n = int(hgt[:-2])
        except ValueError:
            raise ValidationError('Invalid height')

        if n < 59 or n > 76:
            raise ValidationError('Height outside range')
    else:
        raise ValidationError('Invalid height')


class PassportSchema(Schema):
    byr = fields.Integer(required=True, validate=validate.Range(min=1920, max=2002))
    iyr = fields.Integer(required=True, validate=validate.Range(min=2010, max=2020))
    eyr = fields.Integer(required=True, validate=validate.Range(min=2020, max=2030))
    hgt = fields.String(required=True, validate=validate_height)
    hcl = fields.String(required=True, validate=validate.Regexp(r'^#[0-9a-f]{6}$'))
    ecl = fields.String(
        required=True,
        validate=validate.OneOf(['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']),
    )
    pid = fields.String(required=True, validate=validate.Regexp(r'^[0-9]{9}$'))
    cid = fields.String()


@register(day=4)
def solve(file, verbose):
    parser = ParserPEG(grammar, root_rule_name='passports', skipws=False)
    parse_tree = parser.parse(file.read())
    required = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}

    valid_keys = 0
    valid_strict = 0
    schema = PassportSchema()

    for passport in visit_parse_tree(parse_tree, PassportVisitor()):
        if required <= passport.keys():
            valid_keys += 1

        if not schema.validate(passport):
            valid_strict += 1

    print('Part 1:', valid_keys)
    print('Part 2:', valid_strict)
