from libgenapi import Libgenapi
import pprint

l = Libgenapi("http://libgen.rs")
pprint.pprint(l.libgen.search("python", number_results=10))
# pprint.pprint(l.fiction.search("harry potter", number_results=10))
