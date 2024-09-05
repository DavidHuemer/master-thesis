/**
 Grammar for Java Modeling Language (JML) expressions.
 */

grammar JML;

jml: condition+ EOF;

condition: LINE_START (requires_condition | ensures_condition);

requires_condition: '@requires' expression;
ensures_condition: '@ensures' expression;

expression: inequivalence_expression;

inequivalence_expression:
	<assoc = left> inequivalence_expression INEQUIVALENCE inequivalence_expression
	| equivalence_expression;

equivalence_expression:
	<assoc = left> equivalence_expression EQUIVALENCE equivalence_expression
	| implication_expression;

implication_expression:
	<assoc = right> implication_expression IMPLICATION implication_expression
	| or_expression;

// or is neither left nor right associative
or_expression: and_expression (OR and_expression)*;

// and is also neither left nor right associative
and_expression: equality_expression (AND equality_expression)*;

equality_expression:
	<assoc = left> equality_expression op = EQUALITY equality_expression
	| <assoc = left> equality_expression op = INEQUALITY equality_expression
	| relational_expression;

relational_expression: numeric_predicate | boolean_expression;

// All numeric expression are numeric operations that return a boolean value
numeric_predicate:
	less_num_expression
	| greater_num_expression
	| num_equality_expression;

less_num_expression:
	<assoc = left>left = numeric_value op = (LESS | LESS_EQUAL) right = less_numm_expression_extension;

less_numm_expression_extension:
	less_num_expression
	| numeric_value;

greater_num_expression:
	left = numeric_value op = (GREATER | GREATER_EQUAL) (
		greater_num_expression
		| numeric_value
	);

num_equality_expression:
	numeric_value (EQUALITY | INEQUALITY) (
		num_equality_expression
		| numeric_value
	);

numeric_value: additive_expression;

additive_expression:
	<assoc = left>left = additive_expression op = PLUS right = additive_expression
	| <assoc = right>left = additive_expression op = MINUS right = additive_expression
	| multiplicative_expression;

multiplicative_expression:
	multiplicative_expression op = (MULTIPLY | DIVIDE) multiplicative_expression
	| atomic_expression;

atomic_expression: INTEGER | IDENTIFIER | '(' numeric_value ')';

boolean_expression:
	boolean_expression EQUALITY boolean_expression
	| boolean_expression INEQUALITY boolean_expression
	| not_expression;

not_expression: (NOT not_expression) | primary_expression;

primary_expression:
	BOOL_LITERAL
	| IDENTIFIER
	| '(' expression ')';

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

// comparison
LESS: '<';
LESS_EQUAL: '<=';
GREATER: '>';
GREATER_EQUAL: '>=';

// JML keywords
RESULT: '\result';

IDENTIFIER: [a-zA-Z_][a-zA-Z_0-9]*;
INTEGER: [0-9]+;
WS: [ \t\r\n]+ -> skip;