/**
 Grammar for Java Modeling Language (JML) expressions.
 */

grammar JML;

jml: jml_item+ EOF;

jml_item: behavior = behavior_expr | cond = condition;

behavior_expr: PUBLIC behavior = special_behavior;

special_behavior: NORMAL_BEHAVIOR | EXCEPTIONAL_BEHAVIOR;

condition: (
		requires_condition
		| ensures_condition
		| signals_condition
		| signals_only_condition
		| also_condition
	) ';'?;

requires_condition: REQUIRES expr = expression;
ensures_condition: ENSURES expr = expression;
signals_condition: SIGNALS expr = exception_expression;
signals_only_condition:
	SIGNALS_ONLY signals = signal_only_signals;
also_condition: ALSO behavior = special_behavior?;

expression:
	primary
	| old_expression
	| this_expression
	| method_call
	| quantifier_expression
	| expr = expression LEFT_SQUARE_BRACKET index_expr = expression RIGHT_SQUARE_BRACKET
	| expr = expression '.' method = method_call
	| expr = expression '.' ident = IDENTIFIER
	| prefix = (PLUS | MINUS | '++' | '--' | '~' | '!') expr = expression
	| <assoc = left> left = expression op = (MULTIPLY | DIVIDE) right = expression
	| <assoc = left> left = expression op = (PLUS | MINUS) right = expression
	| <assoc = left> left =expression op = MUDULO right = expression
	| <assoc = left> left = expression op = (
		LESS
		| LESS_EQUAL
		| GREATER
		| GREATER_EQUAL
	) right = expression
	| <assoc = left> left = expression op = (
		EQUALITY
		| INEQUALITY
	) right = expression
	| <assoc = left> left = expression op = AND right = expression
	| <assoc = left> left = expression op = OR right = expression
	| <assoc = right> expr = expression question_mark = '?' true_expr = expression colon = ':'
		false_expr = expression
	| <assoc = right> left = expression op = IMPLICATION right = expression
	| <assoc = left> left = expression op = EQUIVALENCE right = expression
	| <assoc = left> left = expression op = INEQUIVALENCE right = expression
	| atomic_value;

expressionList: expression (',' expression)*;

signal_only_signals: IDENTIFIER (',' IDENTIFIER)*;

primary: '(' expression ')';

method_call: ident = IDENTIFIER args = arguments;

arguments: '(' expressions = expressionList? ')';

// question_mark_expression: expr = inequivalence_expression QUESTION_MARK true_val =
// inequivalence_expression COLON false_val = inequivalence_expression;

atomic_value:
	INTEGER
	| DOUBLE
	| BOOL_LITERAL
	| RESULT
	| NULL
	| IDENTIFIER;

quantifier_expression:
	(bool_quantifier_expression | numeric_quantifier_expression);

bool_quantifier_expression:
	forall_expression
	| exists_expression;

forall_expression:
	FORALL expr = bool_quantifier_core_expression;

exists_expression:
	EXISTS expr = bool_quantifier_core_expression;

bool_quantifier_core_expression:
	types = type_declarations ';' ranges = expression ';' expr = expression;

type_declarations: type_declaration (',' type_declaration)*;

type_declaration: 'int' IDENTIFIER (',' IDENTIFIER)*;

range_expression_value:
	primary
	| old_expression
	| this_expression
	| expr = range_expression_value '.' method = method_call
	| range_expression_value '[' range_expression_value ']'
	| expr = range_expression_value '.' ident = IDENTIFIER
	| prefix = (PLUS | MINUS | '++' | '--' | '~' | NOT) range_expression_value
	| <assoc = left> left = range_expression_value op = (
		MULTIPLY
		| DIVIDE
	) right = range_expression_value
	| <assoc = left> left = range_expression_value op = (
		PLUS
		| MINUS
	) right = range_expression_value
	| atomic_value;

numeric_quantifier_expression:
	max_quantifier_expression
	| min_quantifier_expression
	| sum_quantifier_expression
	| product_quantifier_expression;

max_quantifier_expression:
	MAX expr = numeric_quantifier_core_expression ';'?;

min_quantifier_expression:
	MIN expr = numeric_quantifier_core_expression ';'?;

sum_quantifier_expression:
	SUM expr = numeric_quantifier_core_expression ';'?;

product_quantifier_expression:
	PRODUCT expr = numeric_quantifier_core_expression ';'?;

numeric_quantifier_core_expression:
	numeric_quantifier_values_expression
	| numeric_quantifier_range_core_expression ';'?;

numeric_quantifier_values_expression:
	'(' expression (',' expression)* ')';

numeric_quantifier_value:
	numeric_quantifier_expression
	| atomic_value;

numeric_quantifier_range_core_expression:
	types = type_declarations ';' ranges = expression (
		';'
		| '&&'
		| '==>'
	) expr = expression;

exception_expression:
	declaration = exception_declaration expr = expression;

exception_declaration:
	'(' exception = IDENTIFIER (name = IDENTIFIER)? ')';

old_expression: OLD '(' expr = expression ')';

this_expression: JML_THIS '.' expr = expression;

// jml rules
BOOL_LITERAL: 'true' | 'false';

PUBLIC: 'public';

AND: '&&';
OR: '||';

EQUALITY: '==';
INEQUALITY: '!=';
IMPLICATION: '==>';
EQUIVALENCE: '<==>';
INEQUIVALENCE: '<=!=>';

NOT: '!';

PLUS: '+';
MINUS: '-';
MULTIPLY: '*';
DIVIDE: '/';
MUDULO: '%';

QUESTION_MARK: '?';
COLON: ':';

LEFT_SQUARE_BRACKET: '[';
RIGHT_SQUARE_BRACKET: ']';

// comparison
LESS: '<';
LESS_EQUAL: '<=';
GREATER: '>';
GREATER_EQUAL: '>=';

// JML keywords

REQUIRES: 'requires';
ENSURES: 'ensures';
SIGNALS: 'signals';
SIGNALS_ONLY: 'signals_only';
ALSO: 'also';

RESULT: '\\result';
FORALL: '\\forall';
EXISTS: '\\exists';

MAX: '\\max';
MIN: '\\min';
SUM: '\\sum';
PRODUCT: '\\product';

OLD: '\\old';
JML_THIS: '\\this';

// Behaviors
NORMAL_BEHAVIOR: 'normal_behavior';
EXCEPTIONAL_BEHAVIOR: 'exceptional_behavior';

NULL: 'null';
AT: '@' -> skip;

IDENTIFIER: [a-zA-Z_][a-zA-Z_0-9]*;

INTEGER: [0-9]+;
DOUBLE: [0-9]+ ('.' [0-9]+);
WS: [\t\r\n ]+ -> skip;
COMMENT: '//' -> skip;