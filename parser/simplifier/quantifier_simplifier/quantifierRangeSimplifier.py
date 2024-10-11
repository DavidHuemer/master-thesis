from parser.generated import JMLParser


class QuantifierRangeSimplifier:
    @staticmethod
    def get_type_declarations(types: JMLParser.JMLParser.Type_declarationsContext):
        variable_names = []

        for type_declaration in types.children:
            # Type is the first child of the type declaration
            t = type_declaration.children[0].getText()

            # All other children are variable names
            for i in range(1, len(type_declaration.children)):
                if type_declaration.children[i].getText() == ',':
                    continue
                variable_names.append((t, type_declaration.children[i].getText()))

        return variable_names
