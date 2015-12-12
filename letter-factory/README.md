# letter-factory #

A small convenience script to auto-generte letters from a LaTeX template document and a YAML file of substitutions.

## Example ##

All that is needed is a LaTeX template document that contains several markers. These markers are replaces with content according to the given YAML file and the resulting files are compiled. The PDFs are then copied to the working directory. 

For example, suppose we have a file `template.tex`like this:

    \documentclass[a4paper, 10pt]{scrlttr2}
    ....

    \setkomavar{subject}{§MARKER_SUBJECT§}

    \begin{letter}{§MARKER_ADDR§}

    \opening{Dear Mr. X}

    lorem ipsum

    \end{letter}
    \end{doucument}

We have defined two substitutions: `§MARKER_SUBJECT§` and `$MARKER_ADDR§`. We can now specify how to substitute those. Create a file called `subs.txt` like so:

    name: some_letter_filename
    patterns:
        - Exp: §MARKER_SUBJECT§
          Sub: Coffee tastes great!!!
        - Exp: §MARKER_ADDR§
          Sub: 1234 Fake Street
    ---
    name: some_other_letter_name
    patterns:
        - Exp: §MARKER_SUBJECT§
          Sub: Drink more coffee!!!
        - Exp: §MARKER_ADDR§
          Sub: 1234 Fake Street

Now we can run `./letter-factory.py subs.txt -t temaplate.tex`. We will get two letters, one named `some_letter_filename.pdf` and `some_other_letter_name.pdf`.
