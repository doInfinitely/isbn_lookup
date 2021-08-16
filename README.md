# It’S BeeN Stressful Typing All These ISBNs
Motivation: I’m building a model to understand narratives in books, and in order to troubleshoot and iterate on that model, I need a dataset of relatively easy books I’ve read already. I have a bunch of books I read prior to undergraduate lying around, so I want to use those. As a first step I create a .tsv (tab-separated value) file of the book title and the ISBN (it’s always good to pair machine readable stuff like an ISBN with a human readable label like the book title). I was growing increasingly nervous that I made a typo in one or more of the ISBNs I typed from the books, so I decided to design a software solution.

Specification:
For a given ISBN, determine the associated book title.

For a given associated book title, determine if it’s *similar enough* to the human readable label provided by the user.

For a given ISBN, find all ISBNs with a hamming distance (edit distance) of 1.

For a set of ISBNs and a single label entered by the user, find the ISBN from the set that is associated with a book title closest to the label.
