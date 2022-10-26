# Toolbox library in python

## License

This is free and unencumbered software released into the public domain.
For more information, please refer to <http://unlicense.org/>


## What

This python library provides a bunch of utility functions. 

## Why

So I don't have to keep reinventing every wheel I ever want to use.

## How 

For details of how to use the various functions and methods, see 'pydoc tbx'.

Usage examples may be found in the projects listed below in "Projects that
depend on this one".

## When

This code was developed organically from 2016 to the present (2022 at the time
of this update).

## Who

Tom Barron (tusculum@gmail.com)

## Running tests

        $ py.test

With a coverage report (must have coverage and pytest-cov installed):

        $ py.test --cov

With a coverage report showing the lines not tested

        $ py.test --cov --cov-report term-missing

## Notes

 * Notice that there is an assymetry between `run(<cmd>, input=<str>, ...)`
   and `run(<cmd>, ..., output=<str>)`.

    * Specifically, `input=<str>` can use the string directly as input, or
      use it as a redirection expression (`<cmd> |` or `> <path>`).

    * However, in the case of `output=<str>`, the called run function can't
      assign into the string named as the output argument. The output
      argument can use the string as a redirection expression, but that's all.

## Projects that depend on this one

 * https://github.com/tbarron/backscratcher
 * https://github.com/tbarron/dtm
 * https://github.com/tbarron/nldt
 * https://github.com/tbarron/bearomator
 * https://github.com/tbarron/editor
 * https://github.com/tbarron/fx
 * https://github.com/tbarron/pytool
