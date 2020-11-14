This part is where things will get interesting: we'll be reading in a corpus (a collection of documents) with two possible true labels and training a classifier to determine which label a query document is more likely to have.
Here's the twist: the corpus is created from your essays about AI100 and the essays on the same topic from 2016, and based on training data from each, you'll be predicting whether an essay was written in 2020 or 2016. (Your classifier will probably be bad at this! It's okay, we're looking for a very subtle difference here.)
You will need: corpus.tar.gz
