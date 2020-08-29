""" Provides some utilities to deal with jupyter notebook specific issues """

def source(*functions):
    """ source a script as if we have written the script in jupyter notebook and executed it """
    source_code = '\n\n'.join(getsource(fn) for fn in functions)        
    display(HTML(highlight(source_code, PythonLexer(), HtmlFormatter(full=True))))