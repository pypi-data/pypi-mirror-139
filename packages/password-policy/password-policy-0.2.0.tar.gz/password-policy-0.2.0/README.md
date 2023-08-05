---
title: Password Policy Library API
layout: page
---

This library provides a machine readable representation of password composition policies. The ultimate goal for this library is to allow websites to upload policy descriptions and then have password generators download and use these descriptions to generate compliant passwords.

## Policy Descriptions

Policies are defined using the following objects `PCP`, `PCPRule`, `PCPSubsetRequirement`, and `PCPCharsetRequirement`. There is also a utility function `SimplePCP` for creating simple policies.

### SimplePCP

`SimplePCP` is a shortcut function for creating PCP objects. It is the same as calling `PCP([PCPRule(*args, **kwargs)])`.

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| min_length | int | 1 | The minimum number of characters that must be in the password. |
| max_length | int | None | The maximum number of characters allowed in the password. |
| max_consecutive | int | None | The maximum number of times the same character can appear in a row. |
| prohibited_strings | set[str] | None | A set of strings that must not appear in the password. |
| require | list[int] | None | A list of charsets that must appear in the password. |
| require_subset | PCPSubsetRequirement | None | A list of charsets for which a subset must appear in the password. |
| charset_requirements | dict[str,PCPCharsetRequirement] | None | A mapping between charsets and additional requirements for that charset. |

### PCP

`PCP` is the root class for all policies. It contains the following information.

| Member | Type | Default | Description |
| --- | --- | --- | --- |
| charsets | dict[str,str] | `DEFAULT_CHARSETS` | The set of character allowed in the password, split into one or more disjoint character sets ('charset' for short). The key is the name of the charset and the value is a string containing the characters that make up the charset. |
| rules | list[PCPRule] | N/A | The list of rules that make up the policy. As long as one rule matches, the policy is considered valid. At least one rule is required to be set. |

Two charsets are provided by the library:

* `DEFAULT_CHARSETS`—Includes lowercase letters (*lower*), uppercase letters (*upper*), digits (*digits*), and symbols (*symbols*). This uses the charsets defined in python's `string` package. Symbols includes punctuation and whitespace.
* `ALPHABET_CHARSETS`—Same as `DEFAULT_CHARSETS` except that lowercase and uppercase are merged into a single charset (*alphabet*).

The `PCP` class also provides several utility methods:

* `validate()->None`—Validates that the policy is self consistent. For example, checking that it doesn't require more characters than it allows. Raises an exception if their are issues with the policy.
* `dumps(**kwargs) -> str`—Dumps the policy to JSON. Tries to create the most succinct representation. Passed `**kwargs` to `json.dumps`, allowing formatted output.
* `@staticmethod loads(s: str) -> PCP`— Loads a PCP object from the provided JSON.

### PCPRule

`PCPRule` specifies one or more requirements passwords must meet to satisfy the rule. All requirements must be met for the rule to be satisfied. Possible requirements are,

| Member | Type | Default | Description |
| --- | --- | --- | --- |
| min_length | int | 1 | The minimum number of characters that must be in the password. |
| max_length | int | None | The maximum number of characters allowed in the password. |
| max_consecutive | int | None | The maximum number of times the same character can appear in a row. |
| prohibited_strings | set[str] | None | A set of strings that must not appear in the password. |
| require | list[int] | None | A list of charsets that must appear in the password. |
| require_subset | PCPSubsetRequirement | None | A list of charsets for which a subset must appear in the password. |
| charset_requirements | dict[str,PCPCharsetRequirement] | None | A mapping between charsets and additional requirements for that charset. |

### PCPSubsetRequirement

Describes a subset requirement.

| Member | Type | Default |Description |
| --- | --- | --- | --- |
| options | set[str] | None | The list of character sets to use. If not set, the list of all charsets will be used for the options when processing the rule.
| count | int | N/A | The minimum number of options that must be in the password. Needs to be between 1 (inclusive) and the number of options (exclusive). Must be set if a subset requirement is used. |

### PCPCharsetRequirement

Requirements specific to the mapped charset.

| Member | Type | Default |Description |
| --- | --- | --- | --- |
| min_required | int | None | Minimum characters required from the specified charset. |
| max_allowed| int | None | Maximum characters from the charset allowed. |
| max_consecutive | int | None | Maximum number of character from this charset allowed in a row. Note, the characters don't have to be the same, just from the same charset. |
| required_locations| list[int] | None | Which locations in the password (0-indexed, allows reverse indexing) must contain a character from this charset. |
|prohibited_locations| list[int] | None | Which locations in the password (0-indexed, allows reverse indexing) must *not* contain a character from this charset. |

## Default character sets

`DEFAULT_CHARSETS` contains four character sets:

* `lower`—Lowercase alphabetic letters (a–z).
* `upper`—Uppercase alphabetic letters (A–Z).
* `digits`—Digits (0–9).
* `symbols`—All ASCII symbols, including whitespace.

`ALPHABET_CHARSETS` contains three character sets:

* `alphabet`—Lowercase alphabetic letters (a–z) and uppercase alphabetic letters (A–Z).
* `digits`—Digits (0–9).
* `symbols`—All ASCII symbols, including space.

## Checking Passwords

The `check_password(password: str, pcp: PCP) -> bool` method can be used to check a password against a policy. It will return `True` if the password matches at least one of the rules in the policy and `False` otherwise.

## Measuring Policy Strength

This library provides two methods for estimating the strength of passwords created using the given policy:

* `check_machine_strength(pcp: PCP) -> int`—Estimates the number of passwords that a password generator could generate using the given policy, assuming it generates passwords equal to the smallest required `min_length`.
* `check_human_strength(pcp: PCP, preferences: list[str]) -> int`—Estimates the strength of passwords that humans would create using the given policy. This method assume that humans will generate passwords equal to the smallest required `min_length`. Additionally, it assumes that users will select charsets based on the provided preferences (as long as they are allowed by the policy). If not set, preferences defaults to `['lower', 'upper', 'digits', 'symbols']`.

For both methods, the return value is half of the estimated number of passwords that can be generated. This is done because on average, the generated password would be guessed after searching half the search space.
