%childOf(X,Y) - X is a child of Y
%Facts for both parents
childOf(andrew,elizabeth).
childOf(andrew,philip).
childOf(anne,elizabeth).
childOf(anne,philip).
childOf(beatrice,andrew).
childOf(beatrice,sarah).
childOf(charles,elizabeth).
childOf(charles,philip).
childOf(diana,kydd).
childOf(diana,spencer).
childOf(edward,elizabeth).
childOf(edward,philip).
childOf(elizabeth,george).
childOf(elizabeth,mum).
childOf(eugenie,andrew).
childOf(eugenie,sarah).
childOf(harry,charles).
childOf(harry,diana).
childOf(james,edward).
childOf(james,sophie).
childOf(louise,edward).
childOf(louise,sophie).
childOf(margaret,george).
childOf(margaret,mum).
childOf(peter,anne).
childOf(peter,mark).
childOf(william,charles).
childOf(william,diana).
childOf(zara,anne).
childOf(zara,mark).

female(anne).
female(beatrice).
female(diana).
female(elizabeth).
female(kydd).
female(louise).
female(margaret).
female(mum).
female(sarah).
female(sophie).
female(zara).

male(andrew).
male(charles).
male(edward).
male(eugenie).
male(george).
male(harry).
male(james).
male(mark).
male(peter).
male(philip).
male(spencer).
male(william).

%base cases for spouse
married(anne,mark).
married(diana,charles).
married(elizabeth,philip).
married(kydd,spencer).
married(mum,george).
married(sarah,andrew).
married(sophie,edward).

%********************************%
%     implement the following    %
%You may add more clauses to help%
%********************************%
% spouse(X,Y) Symmetric version of married
spouse(X,Y):-
	married(Y,X);
	married(X,Y).

%daughterOf(X,Y) - X is the female child of Y
daughterOf(X,Y):-
	female(X),
	childOf(X,Y).

%sonOf(X,Y) - X is the male child of Y
sonOf(X,Y):-
	male(X),
	childOf(X,Y).

%brotherOf(X,Y) - X is the male sibling of Y
brotherOf(X,Y) :-
	male(X),
	childOf(X,Z),
	childOf(Y,Z),
	X \= Y.

%sisterOf(X,Y) - X is the female sibling of Y
sisterOf(X,Y):-
    female(X),
    childOf(X,Z),
    childOf(Y,Z),
    X \= Y.

% grandchildOf(X,Y) - X is a grandchild of Y
grandchildOf(X,Y):-
    childOf(X,Z),
    childOf(Z,Y).

%ancestorOf(X,Y) - X is an ancestor of Y
%Base Case - X is an ancestor of Y if Y is the child of X
ancestorOf(X,Y):-
    childOf(Y,X).
%Recursive Case - X is also an ancestor of Y if Y is child of W and X is
%ancestor of W
ancestorOf(X,Y):-
    childOf(Y, W),
    ancestorOf(X,W).

%auntOf(X,Y) - X is the aunt of Y
auntOf(X,Y):-
    female(X),
    childOf(Y,W),
    sisterOf(X,W).

%uncleOf(X,Y) - X is the uncle of Y
uncleOf(X,Y):-
    male(X),
    childOf(Y,W),
    brotherOf(X,W).

%firstCousinOf(X,Y) - X is the first cousin of Y; i.e. one of X's parents is siblings with one of Y's parents
firstCousinOf(X,Y):-
    childOf(X,W),
    childOf(Y,Z),
    siblingOf(W,Z).


%brotherInLawOf(X,Y) - X is the brother of Y's spouse or X is the male spouse of Y's sibling
brotherInLawOf(X,Y):-
    brotherOf(X,W),
    spouse(W,Y);
    male(X),
    spouse(X,W),
    siblingOf(W,Y).

%sisterInLawOf(X,Y) - X is the sister of Y's spouse or X is the female spouse of Y's sibling
sisterInLawOf(X,Y):-
    sisterOf(X,W),
    spouse(W,Y);
    female(X),
    spouse(X,W),
    siblingOf(W,Y).

%siblingOf(X,Y) - X is a sibling of Y if X is a brother or a sister of Y.
%Additional clause to help with firstcousinOf
siblingOf(X,Y):-
    brotherOf(X,Y);
    sisterOf(X,Y).