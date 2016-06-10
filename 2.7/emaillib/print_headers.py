from argparse import ArgumentParser, FileType
from email import message_from_file
from email.header import decode_header
from email.utils import getaddresses


def get_args_parser():
    pars = ArgumentParser(
        description="""API printing MIME headers with decoding.
        To print headers type -h or --get-headers and give str
        from standard input.""")
    pars.add_argument('-g', '--get-headers', nargs='?', type=bool,
                      help='printing MIME headers with decode', const=True)
    pars.add_argument('-f', '--files', nargs='+', type=FileType('r'),
                      help='files for decoding', default=[])

    return pars.parse_args()


def print_eml_headers(eml_files):
    for file_ in eml_files:
        eml = message_from_file(file_)

        for header in ['from', 'to', 'cc']:

            # Getting value/addresses from MIME header
            header_value = eml.get_all(header, [])
            addresses = getaddresses(header_value)

            print '\n', header.upper(), ':'

            for real_name, email in addresses:
                for name, encoding in decode_header(real_name):

                    # Check for decode
                    if encoding is None:
                        print real_name, ':', email
                    else:
                        print name.decode(encoding), ':', email

    print '\n'

if __name__ == '__main__':
    args = get_args_parser()

    if args.get_headers:
        if not args.files:
            raise AttributeError('Not given files')

        print_eml_headers(args.files)
