"""
Veeeeeeeery much inspired by displacy's own visualizer:

https://github.com/explosion/spaCy/tree/master/spacy/displacy
"""


# from typing import Dict, Tuple, Optional, Any
from wsgiref import simple_server
from spacy.displacy.render import DependencyRenderer
from spacy.util import is_in_jupyter
from ..models.sentence_parser import SentenceParser
# from patchcomm.models.coref_resolver import CoreferenceResolver


class DependencyParseVisualizer:
    def __init__(self, sentence_parser: SentenceParser):
        self._html = {}
        # self.sentence_parser = SpacyBasedSentenceParser(sentence)
        self.sentence_parser = sentence_parser
        # self.doc = self.sentence_parser.doc
        self.nlp = self.sentence_parser.nlp  # this is so that we don't have to load spaCy model again!
        # self.doc = self.nlp(sentence)
        self.renderer = DependencyRenderer(options={})
        self.converter = self.sentence_parser.getSpacyParse

    def _convertByteToStr(self, byte):
        """
        Convert a bytes object to a string
        :params
            bytes: The object to convert
        :returns (unicode):
            The converted string
        """
        ## Important: if no encoding is set, string becomes 'b'...''
        return str(byte, encoding='utf8')

    def _app(self, environ, start_response):
        # FIXME: check out if env is necessary
        headers = [(
            self._convertByteToStr(b'Content-type'),
            self._convertByteToStr(b'text/html; charset=utf-8')
        )]
        start_response(
            self._convertByteToStr(b'200 OK'),
            headers
        )
        res = self._html['parsed'].encode()
        return [res]

    def render(
            self,
            sentence: str,
            use_conceptnet: bool = True,
            use_retrogan_drd: bool = False,
            page=False,
            minify=False
    ):
        """
        Render displaCy visualisation
        :params
            doc (list or Doc): Document(s) to visualize
            page (bool): Render markup as full HTML page
            minify (bool): Minify HTML markup
        :returns (unicode):
            Rendered HTML markup
        """
        # doc: Doc = self.nlp(sentence)
        # if isinstance(doc, (Doc, Span, dict)):
        #     docs = [doc]
        # else:
        #     docs = doc
        # docs = [obj if not isinstance(obj, Span) else obj.as_doc() for obj in docs]
        # if not all(isinstance(obj, (Doc, Span, dict)) for obj in docs):
        #     raise ValueError(Errors.E096)
        sentences = [sentence]
        parsed = [self.converter(sentence, use_conceptnet, use_retrogan_drd) for sentence in sentences]
        self._html['parsed'] = self.renderer.render(parsed, page=page, minify=minify).strip()
        html = self._html['parsed']
        if is_in_jupyter() is True:
            from IPython.core.display import display, HTML
            return display(HTML(f'<span class="tex2jax_ignore">{html}</span>'))
        return html

    def serve(self, sentence: str, host='127.0.0.1', port=1995, page=True, minify=False):
        """
        Serve displaCy visualisation
        :params
            host (str): Host to serve visualisation
            port (int): Port to serve visualisation
            doc (list or Doc): Document(s) to visualise
            page (bool): Render markup as full HTML page
            minify (bool): Minify HTML markup
        """
        self.render(sentence=sentence, page=page, minify=minify)
        httpd = simple_server.make_server(host, port, self._app)
        print('')
        print(f'Serving on http://{host}:{port} ...')
        print('')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f'Shutting down server on port {port}')
        finally:
            httpd.server_close()
