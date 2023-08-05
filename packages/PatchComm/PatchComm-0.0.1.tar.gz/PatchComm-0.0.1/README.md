## PatchComm: Commonsense Knowledge Enabled Natural Language Understanding
PatchComm uses commonsense and contextual knowledge to guide syntactic parsers toward making
better-informed parsing decisions, and at the same time, builds up a frame-like representation to
embody discourse-level knowledge.  The discourse-level knowledge is an integration of
context-independent commonsense knowledge that comes from external commonsense knowledge bases (CSKB)
and context-dependent knowledge that comes from the discourse itself.

Consider the two well-studied syntactic ambiguities: prepositional-phrase attachment ambiguities and 
pronoun coreference ambiguities.  Both kinds of ambiguities are intrinsic in the notion of “natural 
language” or “human language.”

As an example to get us started, consider the sentence

    That person saved that bird with one arm.

Logically speaking, the prepositional phrase “with one arm” can be attached either to “person”/“save”
or to “bird.”  However, anyone who knows about people and birds is expected to know that “with one arm”
should be attached to “person”/“save” rather than “bird.”  Therefore, we only have a _logical_ ambiguity,
but we don't have any _commonsensical_ ambiguity here.

As another example, consider the sentence

    Alex went to the shopping mall with a lot of people.

Here, it's not only logically ambiguous whether “with a lot of people” attaches to “Alex”/“go” or to “mall,”
but it's also commonsensically ambiguous: Without further context, we just can't know whether Alex went with
a lot of people, or the mall had a lot of people.  In cases such as this one, it is much better to leave
the syntactic ambiguities as is, until further contextual information rolls around, rather than prematurely
attempting to make some sort of “best” parsing decision.

Nevertheless, for whatever reason, when people build syntactic parsers, they still require the parsers to
output one single best _parse tree_.  To date, engineering efforts in syntactic parsing are, in my view,
counterintuitive and counterproductive.  Counterintuitive, because they assume there is no need for
underlying commonsense, whereas as we saw before, syntactic parsing really does need underlying commonsense.
Counterproductive, because the end goal of sentence-level processing is discourse-level processing. By
prematurely forcing every sentence to have an independently “best” parse, we necessarily involve ourselves
into the hopeless problem of _Combinatorial Explosion_, as follows:

If a discourse has 20 sentences and each sentence has two possible parses, that's over a million possible
combinations for the discourse.  Suppose there is one “best” interpretation for the discourse, then by
prematurely forcing each sentence to settle on one of the two possible parses, we are gambling on the possibility
that the 20 parses we get from the sentences can chain together into an integral interpretation that either
matches or isn't too far off from that “best” discourse interpretation.  To me, this gamble is unwarranted.

Further, suppose that this gamble fails.  Which one or ones of the 20 sentences should the system modify?
Recall that there are over a million such modifications that the system can potentially do, which is practically
impossible unless the system gets much extra input and monitoring from human — which defeats the purpose of
building a discourse-understanding system in the first place.

It is much better to have a system that keeps track of all the points of ambiguities as it reads away one or 
multiple sentences.  Whenever more commonsense and contextual knowledge present themselves, the system utilizes 
such additional knowledge to double-check the points of ambiguities that it has already encountered and resolved, 
to see whether changes need to be made to any of these points.  This makes sure that the discourse-level 
representation is always consistent with the knowledge and context so-far, and that the sentence parses are 
consistent with the discourse-level representation.

The discourse-level representation is  useful for analyzing high-level concepts, especially ones that may not be
explicitly mentioned via keywords in the original discourse (e.g., concept patterns in Genesis).  The sentence-level
parses are useful for answering specific questions, as a way of testing and evaluating the system.



### Update, 23 September 2021
Added `requirements.txt`.

Detailed steps for running this project:
+ Set up a separate Conda virtual environment for this project:
  ```conda create -n <venv_name> python=<verson>```
+ Install all requirements:
  ```pip install -r requirements.txt```
+ Install `neuralcoref` from its source:
  ```
  git clone https://github.com/huggingface/neuralcoref.git
  cd neuralcoref
  pip install -r requirements.txt  # !!! NOT to be confused with the same command in previous step !!!
  pip install -e .
  ```
+ Download spaCy language models
  ```
  python -m spacy download en_core_web_sm  # small
  python -m spacy download en_core_web_md  # medium
  python -m spacy download en_core_web_lg  # large
  ```



### Update, 11 May 2021
PatchComm is still primarily focusing on sentence-level processing.  It now can
- resolve one or more prepositional-phrase (PP) attachment ambiguities within a sentence
- resolve one or more pronoun coreference ambiguities within a sentence

Both PP attachment and coreference resolution are important problems in not only syntactic parsing, but natural
language understanding in general — as argued above.

More updates to follow.



### Update, 1 March 2021
The sentence parser now supports
- spaCy, as of version 2.3.5
- START parser, which is the brain child of the InfoLab Group at CSAIL, MIT

Check out the parser's (still limited) capabilities of resolving prepositional-phrase attachment ambiguities and
of resolving co-reference, by running:

    python -m unittest src.patchcomm.tests.test_sentence_parser.py

Visualize the dependency parse, very much per spaCy, by running:

    python -m unittest src.patchcomm.tests.test_dependency_visualizer.py

If you ran some really complicated sentences on these tests and discovered that the tests failed, do not worry.

We recommend using the visualizer all the time, because (1) the output being visualized comes entirely from the
sentence parser, and (2) the more visual the better.



### A Note on the Commonsense Knowledge Base (CSKB) Software
PatchComm uses ConceptNet [(Speer et al, 2017)](https://arxiv.org/abs/1612.03975),
a large-scale commonsense knowledge base, ConceptNet, to guide syntactic parsers toward making more
commonsensically informed parsing decisions.
