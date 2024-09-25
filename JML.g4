/**
 Grammar for Java Modeling Language (JML) expressions.
 */

grammar JML;

jml: jml_item+ EOF;

jml_item: behavior_expr | condition;

behavior_expr: '@' 'public' special_behavior;

special_behavior: NORMAL_BEHAVIOR | EXCEPTIONAL_BEHAVIOR;

condition: (
		requires_condition
		| ensures_condition
		| signals_condition
		| signals_only_condition
		| also_condition
	) ';'?;

requires_condition: '@' 'requires' expression;
ensures_condition: '@' 'ensures' expression;
signals_condition: '@' 'signals' exception_expression;
signals_only_condition: '@' 'signals_only' IDENTIFIER;
also_condition: '@' 'also' behavior = special_behavior?;

expression: question_mark_expression | inequivalence_expression;

question_mark_expression:
	expr = inequivalence_expression QUESTION_MARK true_val = inequivalence_expression COLON
		false_val = inequivalence_expression;

inequivalence_expression:
	<assoc = left> left = inequivalence_expression op = INEQUIVALENCE right =
		inequivalence_expression
	| equivalence_expression;

equivalence_expression:
	<assoc = left> left = equivalence_expression op = EQUIVALENCE right = equivalence_expression
	| implication_expression;

implication_expression:
	<assoc = right> left = implication_expression op = IMPLICATION right = implication_expression
	| or_expression;

// or is neither left nor right associative
or_expression:
	<assoc = left> left = or_expression op = OR right = or_expression
	| and_expression;

// and is also neither left nor right associative
and_expression:
	<assoc = left> left = and_expression op = AND right = and_expression
	| equality_expression;

equality_expression:
	<assoc = left> left = equality_expression op = EQUALITY right = equality_expression
	| <assoc = left> left = equality_expression op = INEQUALITY right = equality_expression
	| relational_expression;

relational_expression: numeric_predicate | boolean_expression;

// All numeric expression are numeric operations that return a boolean value
numeric_predicate:
	less_num_expression
	| greater_num_expression
	| num_equality_expression;

less_num_expression:
	<assoc = left>left = numeric_value op = (LESS | LESS_EQUAL) right =
		less_numm_expression_extension;

less_numm_expression_extension:
	less_num_expression
	| numeric_value;

greater_num_expression:
	<assoc = left> left = numeric_value op = (
		GREATER
		| GREATER_EQUAL
	) right = greater_num_expression_extension;

greater_num_expression_extension:
	greater_num_expression
	| numeric_value;

num_equality_expression:
	<assoc = left>left = num_equality_expression op = (
		EQUALITY
		| INEQUALITY
	) right = num_equality_expression
	| numeric_value;

numeric_value: additive_expression;

additive_expression:
	<assoc = left>left = additive_expression op = PLUS right = additive_expression
	| <assoc = right>left = additive_expression op = MINUS right = additive_expression
	| multiplicative_expression;

multiplicative_expression:
	left = multiplicative_expression op = (MULTIPLY | DIVIDE) right = multiplicative_expression
	| atomic_expression;

atomic_expression:
	INTEGER
	| RESULT
	| NULL
	| IDENTIFIER
	| negative_number
	| array_length_expression
	| array_index_expression
	| numeric_quantifier_expression
	| '(' numeric_value ')';

negative_number: '-' atomic_expression;

array_length_expression: IDENTIFIER '.' LENGTH;

array_index_expression: IDENTIFIER '[' numeric_value ']';

boolean_expression:
	boolean_expression EQUALITY boolean_expression
	| boolean_expression INEQUALITY boolean_expression
	| not_expression;

not_expression: (NOT not_expression) | primary_expression;

primary_expression:
	| bool_quantifier_expression
	| '(' expression ')'
	| BOOL_LITERAL
	| NULL
	| IDENTIFIER
	| '(' IDENTIFIER ')';

bool_quantifier_expression:
	forall_expression
	| exists_expression;

forall_expression: FORALL bool_quantifier_core_expression;

exists_expression: EXISTS bool_quantifier_core_expression;

bool_quantifier_core_expression:
	type_declarations ';' range_expression ';' expression;

type_declarations: type_declaration (',' type_declaration)*;

type_declaration: 'int' IDENTIFIER (',' IDENTIFIER)*;

range_expression:
	single_range_expression ('&&' single_range_expression)*;

single_range_expression:
	left = start_range_comparison op = '&&' right = end_range_comparison;

start_range_comparison:
	(expr = numeric_value op = ('<=' | '<') ident = IDENTIFIER)
	| ident = IDENTIFIER op = ('>=' | '>') expr = numeric_value;

end_range_comparison:
	ident = IDENTIFIER op = ('<=' | '<') expr = numeric_value;

numeric_quantifier_expression:
	max_quantifier_expression
	| min_quantifier_expression
	| sum_quantifier_expression
	| product_quantifier_expression;

max_quantifier_expression:
	MAX numeric_quantifier_core_expression;

min_quantifier_expression:
	MIN numeric_quantifier_core_expression;

sum_quantifier_expression:
	SUM numeric_quantifier_core_expression;

product_quantifier_expression:
	PRODUCT numeric_quantifier_core_expression;

numeric_quantifier_core_expression:
	numeric_quantifier_value_expression
	| numeric_quantifier_range_core_expression;

numeric_quantifier_value_expression:
	'(' value = numeric_quantifier_value ')';

numeric_quantifier_value: IDENTIFIER;

numeric_quantifier_range_core_expression:
	type_declarations ';' range_expression ';' expression;

exception_expression:
	declaration = exception_declaration expr = expression;

exception_declaration:
	'(' exception = IDENTIFIER name = IDENTIFIER ')';

// jml rules
LINE_START: '//';

BOOL_LITERAL: 'true' | 'false';

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

QUESTION_MARK: '?';
COLON: ':';

// comparison
LESS: '<';
LESS_EQUAL: '<=';
GREATER: '>';
GREATER_EQUAL: '>=';

LENGTH: 'length';

// JML keywords
RESULT: '\\result';
FORALL: '\\forall';
EXISTS: '\\exists';

MAX: '\\max';
MIN: '\\min';
SUM: '\\sum';
PRODUCT: '\\product';

// Behaviors
NORMAL_BEHAVIOR: 'normal_behavior';
EXCEPTIONAL_BEHAVIOR: 'exceptional_behavior';

NULL: 'null';

IDENTIFIER: [a-zA-Z_][a-zA-Z_0-9]*;

INTEGER: '-'? [0-9]+;
WS: [\t\r\n ]+ -> skip;