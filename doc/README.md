# About the documentation

This folder holds the documentation of the HHG Analysis code.
It is using [Sphinx][] (which makes use of [reStructuredText][]).

To publish the documentation to Github, the method described
[here](https://gist.github.com/3089937) is being used:

For the very first time, we do this:

    cd doc
    rm -rf _build/html
    mkdir -p _build/html
    git clone git@github.com:pklaus/HHG-Analysis-Python.git _build/html
    cd _build/html/
    git symbolic-ref HEAD refs/heads/gh-pages
    rm .git/index
    git clean -fdx
    cd ../..
    make html
    cd _build/html
    touch .nojekyll
    git add .
    git commit -m 'first docs to gh-pages'
    git push origin gh-pages

If the gh-pages branch exists already but the repository is not sitting
in doc/_build/html, get it again using:

    cd doc
    rm -rf _build/html
    mkdir -p _build/html
    git clone git@github.com:pklaus/HHG-Analysis-Python.git _build/html
    cd _build/html
    git checkout gh-pages

Now, when you run `make html` and need to update your documentation,
you can do it "normally" without worrying about the many vagaries of
submodule syncing (I can never get the order correct). just make
changes, then:

    cd doc
    make html
    cd _build/html
    git commit -a -m 'made some changes, yo'
    git push origin gh-pages

[Sphinx]: http://sphinx.pocoo.org/
[reStructuredText]: http://docutils.sourceforge.net/rst.html
