import argparse
import logging

from . import ips, bps
from .util import identify, PatchType

logging.basicConfig(format='vidua: %(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger()

type_map = {
    PatchType.IPS: ips,
    PatchType.BPS: bps,
}


def main():
    parser = argparse.ArgumentParser(description='Apply or validate patches.')
    parser.add_argument('patch',
                        metavar='PATCH',
                        type=argparse.FileType('rb'),
                        help='the patch file')
    parser.add_argument('original',
                        nargs='?',
                        metavar='ORIGINAL',
                        type=argparse.FileType('rb'),
                        help='the file to be patched')
    parser.add_argument('output',
                        nargs='?',
                        metavar='OUTPUT',
                        type=argparse.FileType('xb'),
                        help='filename to write patched file')
    parser.add_argument('-v', '--validate',
                        action='store_true',
                        help='validate the patch only; do not apply it')
    parser.add_argument('-q', '--quiet',
                        action='store_true',
                        help='suppress output except errors')

    args = parser.parse_args()

    if args.quiet:
        logger.setLevel(logging.ERROR)

    module = type_map.get(identify(args.patch))
    if not module:
        parser.error("The patch file is not of a supported type.")

    if args.validate:
        try:
            module.validate_patch(args.patch)
            logger.info("The patch file is valid.")
        except ValueError as e:
            logger.error(e)
            parser.exit(1)
    else:
        if not args.original:
            parser.error("Must specify ORIGINAL or -v")
        if not args.output:
            parser.error("Must specify OUTPUT or -v")
        try:
            args.output.write(module.patch(args.original, args.patch).read())
        except Exception as e:
            logger.error(e)
            parser.exit(1)


if __name__ == '__main__':
    main()
