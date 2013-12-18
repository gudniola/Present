import re
import sys
import os
import argparse

import pyjade
import mako.template


def inline_javascript(html_src, path):
    """Inlines every included javascript file"""
    return html_src


def inline_css(html_src, path):
    """Inlines every included css file"""
    return html_src


def render_html(html_template, slides_src):
    """Applies namespace to in_html_template"""
    return mako.template.Template(html_template).render(slides=slides_src)


def parse_jade(presentation_src):
    """Parses a jade_file, producing a mako template"""
    validation_re = re.compile("""(^(?!(\.slide)|(div\.slide)))|(\n(?!((\.slide)|(div\.slide))))""")
    if validation_re.match(presentation_src):
        raise Exception("Does not describe a deck.js slide deck")
    return pyjade.process(presentation_src)


def render_presentation(presentation_src):
    """Renders a presentation to a single html src from jade_file and returns it"""
    #Load boilerplate.html template
    with open("res/deck.js/boilerplate.html", 'r') as btf:
        boilerplate_template = btf.read()

    #Inline javascript
    boilerplate_template = inline_javascript(boilerplate_template)

    #Inline CSS
    boilerplate_template = inline_css(boilerplate_template)

    #parse_jade
    slides_src = parse_jade(presentation_src)

    #render boilerplate_template using results of parse_jade
    return render_html(boilerplate_template, slides_src)


def present_main(args):
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("presentation_file",
                            type=str,
                            help="The jade template containing the slides.")
    arg_parser.add_argument("-o", "--out-file",
                            type=str,
                            help="The file to save the rendered presentation in.")

    parsed_args = arg_parser.parse_args(args)

    with open(parsed_args.presentation_file, 'r') as pf:
        presentation_src = pf.read()

    presentation_html = render_presentation(presentation_src)
    presentation_html_name = parsed_args.out_file or parsed_args.presentation_file + ".html"

    with open(presentation_html_name, 'w') as phf:
        phf.write(presentation_html)

if __name__ == '__main__':
    present_main(sys.argv[1:])
