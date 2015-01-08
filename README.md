# Textplot-TCF

Textplot-TCF builds on [textplot](https://github.com/davidmcclure/textplot) and adds support for linguistically annotated text files in the [TCF](http://weblicht.sfs.uni-tuebingen.de/weblichtwiki/index.php/The_TCF_Format) format. Parsing TCF is done using [TCFlib](https://github.com/SeNeReKo/TCFlib).

Using TCF as an input format for textplot has some advantages:

* It allows to use various state of the art components for linguistic annotation (e.g., tokenization, lemmatization).
* It allows to use textplot for non-English languages.

However, using lemmas instead of stemmed words produces slightly different results. If these differences are for the better or for the worse might depend on the specific case at hand.

There are also some disadvantages:

* It requires an additional annotation step before the text can be processed.
* The [WebLicht](https://weblicht.sfs.uni-tuebingen.de/WebLicht-4/) tool for creating annotations in TCF format is not openly available, but restricted to members of European academic institutions.

## Annotating Text

The easiest way to create linguistic annotations in TCF format for a text is using the [WebLicht](https://weblicht.sfs.uni-tuebingen.de/WebLicht-4/) application. It allows to upload a text in plain text format and run a series of annotation steps. For textplot-tcf, the only required annotation layer is "lemmas".

## Generating Graphs

This step is the same as in textplot, except that the input is a TCF file:

```bash
In [1]: from textplot_tcf import frequent

In [2]: g = frequent("pg598_tcf.xml")
Indexing terms:
[################################] 125000/125250 - 00:00:10
Generating graph:
[################################] 501/501 - 00:00:01

In [3]: g.write_gml("pg598_tcf.gml")
```

For further details, please check the textplot documentation.