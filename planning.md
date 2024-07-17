# HD Wallet Brainstorm

## Structure of an HD Wallet
The structure adheres to a format known as a derivation path, which appears as follows: m/##'/#'/#'/#/# 

The components are as follows, in order (excluding m):

 1. Purpose
 2. Coin Type
 3. Account
 4. Change
 5. Index

## Purpose
Defines the scheme of wallet BIP 44,49, and 84. For this project, only the specified formats will be considered.

The purpose of the wallet address determines its structure, with various purposes requiring specific algorithms to generate their respective addresses.
### Implementation Solution
Initially I considered three design patterns for the implementation.

 1. Strategy
 2. Template
 3. Visitor

The Visitor pattern excels when a group of objects implementing a common interface is iterated through and a shared method is invoked. However, in this case, it is not necessary.

The Template pattern excels when multiple similar processes share the same number of steps in the implementation their functionality. However, in this case, the address generation steps vary.

This leaves the Strategy pattern, which is ultimately the best option for the case of wallet schemes. Users shall define the wallet scheme in order to generate the correct addresses for their "receiving" and "change" addresses. 

In the implementation, a Factory can be utilized to produce a specified Strategy specified by the user, allowing the wallet to generate the correct address as needed.

