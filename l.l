%{
#include <stdio.h>
void display(char[], int);
int flag;
%}

%%

[a-zA-Z ]+     { flag = 1; display(yytext,flag); return 0; }
[0-9 ]+        { flag = 0; display(yytext,flag); return 0; }
.+            { flag = -1; display(yytext,flag); return 0; }

%%

void display(char a[], int flag) {
    if (flag == 1)
        printf("The given string '%s' is a word\n", a);
    if (flag == 0)
        printf("The given string '%s' is a number\n", a);
    if (flag == -1)
        printf("The given string '%s' is everything\n", a);
}
int main() {
    printf("Enter a string: ");
    yylex();
    return 0;
}
int yywrap() {
    return 1;
}

%{
#include<stdio.h>
#include<string.h> 
int wc=0,cc=0,lc=0,sc=0;
%}

%%

[\n] { lc++ ;  }
[  \t] { sc++ ;  }
[^\t\n ]+ { 
    if(strcmp(yytext, "-1") == 0) {
        return 0;     
    }
    wc++;
    cc+=yyleng;
}
%%
int main( int argc , char * argv[])
{
    printf("Enter the input: \n");
    yylex();
    printf("The number of lines are : %d\n",lc);
    printf("The number of words are : %d\n",wc);  
    printf("The number of spaces are : %d\n",sc);  
    printf("The number of characters are : %d\n",cc);
    return 0;
}
int yywrap(){
    return 1;
}

%{
#include <stdio.h>
#include <stdlib.h>
%}

%%
[ \t\n]+                 ; /* Skip whitespace */
"int"|"float"|"char"     { printf("KEYWORD: %s\n", yytext); }
[0-9]+                   { printf("NUMBER: %s\n", yytext); return 0;}
[a-zA-Z_][a-zA-Z0-9_]*   { printf("IDENTIFIER: %s\n", yytext); }
"+"|"-"|"*"|"/"          { printf("OPERATOR: %s\n", yytext); }
"="                      { printf("ASSIGNMENT: %s\n", yytext); }
"("                      { printf("PUNCTUATION: ( \n"); }
")"                      { printf("PUNCTUATION: ) \n"); }
"{"                      { printf("PUNCTUATION: { \n"); }
"}"                      { printf("PUNCTUATION: } \n"); }
"["                      { printf("PUNCTUATION: [ \n"); }
"]"                      { printf("PUNCTUATION: ] \n"); }
.                        { printf("UNKNOWN: %s\n", yytext); }
%%

int main() {
    printf("Enter your input: ");
    yylex();  /* Call the lexer */
    return 0;
}

//vowel.l

%{
#include <stdio.h>
%}

%%
[aeiouAEIOU]              { printf("Input is a vowel\n"); }
[A-Za-z(^aeiouAEIOU)]   { printf("Input is not a vowel\n"); }
%%

int main() {
    printf("Enter a character: ");
    yylex();
    return 0;
}

int yywrap() {
    return 1;
}