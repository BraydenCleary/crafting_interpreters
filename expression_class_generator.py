def define_ast(output_file, base_class, classes_to_define):
    output = ''

    output += """
from abc import ABC

class {}(ABC):
    def __init__(self):
        pass

    def accept(self, visitor):
        pass
    """.format(base_class)

    output += """
class ExprVisitor(ABC):
    """

    for class_to_define in classes_to_define:
        class_name = class_to_define.split(':')[0]
        attributes = class_to_define.split(':')[1].split(',')

        output +=   """
    def visit{}{}(self, expr_instance):
        pass

        """.format(class_name, base_class)

    for class_to_define in classes_to_define:
        class_name = class_to_define.split(':')[0]
        attributes = class_to_define.split(':')[1].split(',')
        setting_attributes = '\n'.join([f"        self.{attribute} = {attribute}" for attribute in attributes])
        output +=   """
class {}({}):
    def __init__(self, {}):
{}

    def accept(self, visitor):
        return visitor.visit{}{}(self)
        """.format(class_name, base_class, ', '.join(attributes), setting_attributes, class_name, base_class)

    with open(output_file, 'w') as f:
        f.write(output.strip())


if __name__ == '__main__':
    define_ast('expression.py', 'Expr', [
        "Binary:left,operator,right",
        "Grouping:expression",
        "Literal:value",
        "Unary:operator,right"
    ])
