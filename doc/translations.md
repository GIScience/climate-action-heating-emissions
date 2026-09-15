# Translations

[[_TOC_]]

We use [GNU gettext](https://www.gnu.org/software/gettext/) with support
of [pybabel](https://babel.pocoo.org/en/latest/) and the [translate-toolkit](https://github.com/translate/translate) for
translations.
In short, the workflow thereof consists of two isolated steps:

1. As a preparation, extract translatable strings from the source code into lookup files
2. On runtime, translate these strings in an efficient fashion on the fly

In practice this means the following general steps need to be taken to translate a plugin

1. Mark translatable strings in the source code.
   They can also be seen as message IDs because they are the reference point for the lookup table of translations.
2. Extract these strings into a `.pot` template file.
3. Copy this file into dedicated translation `.po` files per language.
4. Write the language-specific translations.
5. Compile the `.po` files into `.mo` files to be referenced at runtime.

## 0. Preparation

The following steps are required when first translating a plugin:

- add the `translate-toolkit` and `mistletoe` to your dev-dependencies:

   ```shell
   poetry add translate-toolkit mistletoe --group dev
   ```

- add `RUN poetry run pybabel compile -d resources/locales; exit 0` to your Dockerfile to automatically generate the
  `.mo` files.
  _Read in [this issue](https://github.com/python-babel/babel/issues/1268) why the `; exit0` is required._
  Then, you should also exclude these files from version control and docker build by adding `*.mo` to `.gitignore` and
  potentially `.dockerignore`
- Create a directory for the language you will translate to

   ```shell
   mkdir -p resources/locales/<target-lang>/LC_MESSAGES
   ```

## 1. Mark for extraction

### Markdown

No marking is necessary.

### Source Code

In the source code, the steps _mark-for-extraction_ and _translate-on-runtime_ can be located together OR be separated.
In the former, the function `tr('my-string')` will mark a string for extraction as well as translate it **at that
point** during runtime.
For the latter, the combination of the functions `N_('my-string')` and `tr(string_variable)` can be used.
This is required if the system is not fully language-loaded when the string is declared, e.g. for constants which are
initialised on module import.
Both functions can be imported from `climatoology.base.i18n`.

#### Teaser and Input

To translate the teaser and computation input parameter descriptions, it suffices to mark the respective strings in the
source code as translatable where they are declared.
I.e. surround the strings by `N_('my translatable string')`.
`climatoology` will automatically apply the translations at the appropriate time.

Note that for computation input parameters, currently only the title and description can be translated.

#### Computation

In most places where strings are handled during computation (and should be translated for the user's consumption), they
can directly be translated.
I.e. surround them by `tr('my translatable string')`.

In cases where the translation must be applied later (e.g. for strings that are used as dictionary keys or column names
in a dataframe), use `N_` on the original string _declaration_ as explained above.
You must then explicitly call `tr` on the string _variable_ later to apply the translation.

For dataframes, we use `climatoology.base.i18n.translate_dataframe`, which provides a deep translation of dataframes,
including column names, index names, index values, and all dataframe values (by applying `tr` to each of these).

There is no easy way to identify translatable strings and numbers in the code if translation is not built into a plugin
from the start.
Apart for simply looking at all **string** occurences in the code another method is to look at the output generated in
the
front-end and identify translatable strings from there.

## 2. Template (.pot) extraction

### Markdown Files

Our **default** methodology and purpose files are in `resources/locales/en`.

Run

```shell
poetry run md2po \
  -m 120 \
  -P \
  -S \
  resources/locales/en/*.md \
  resources/locales
```

to create the translation template files. [^linelengthnote]

### Source Code

To extract the translatable strings (as marked by `N_` and `tr`) and create `.pot` files, run:

```shell
poetry run pybabel extract heating_emissions/ \
    -w 120 \
    -o resources/locales/messages.pot \
    --keyword=tr \
    --copyright-holder="HeiGIT gGmbH" \
    --project=heating_emissions
```

## 3. Translation files (.po)

Then copy the templates across into `.po` files.
Side note for Markdown: While the translate-toolkit allows to create `.po` files directly, we suggest to use this more
standard
approach via `.pot` files.

```shell
poetry run pot2po \
  -m 120 \
  -t resources/locales/<target-lang>/LC_MESSAGES \
  -i resources/locales \
  -o resources/locales/<target-lang>/LC_MESSAGES
```

This will update all .po files of a certain language.
If instead you want to update one .po file in all languages, you can use

```shell
poetry run pybabel update \
    -w 120 \
    -i resources/locales/<your desired file>.pot \
    -d resources/locales/
```

When first initialising a new language add `--init-missing -l <target-lang>` to the above command to create the
inital `.po` file.

## 4. Translation

Now go ahead and translate to the new language in the `.po` files by filling in the `msgstr`.
You can also use tools like https://poedit.net to support you.

## 5. Compilation

### Markdown

As methodology and purpose can be long markdown files, we use a dedicated translation procedure for them.
They are fully pretranslated, so the source code is packaged already with a markdown file per language.
Create the translated files using

```shell
poetry run po2md \
  -m 120 \
  -i resources/locales/<target-lang>/LC_MESSAGES/ \
  -t resources/locales/en/ \
  -o resources/locales/<target-lang>
```

### Source Code

As described above, the docker container will compile the source code lookup file on build.
If you want to run the plugin locally, you will have to compile the file manually.
If you used poedit, saving the file will create the `.mo`.
Otherwise run

```shell
poetry run pybabel compile -d resources/locales
````

## 6. Repeat

To translate to more languages, repeat from 3.

To update existing translations you can safely run steps 1-5 again.

[^linelengthnote]: Note that you will see `-w 120` or `-m 120` in some of the commands below.
This will set the line length of the output files to prevent random changes to the files due to
line-length-disagreements.
Make sure all your tools editing the files share the same line-length setting (e.g. poedit mentioned later).
Note that other random changes can still appear in the header or the random lines due
to [this issue in the translate toolkit](https://github.com/translate/translate/issues/6249#issuecomment-4690195254) or
due to [other tool failures](https://github.com/python-babel/babel/issues/1266).
