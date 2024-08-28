import argparse

def callicog_run(pa, args):
	print(f'callicog{pa} running for animal {args.animal} and template {args.template} @{args.server}')
	return 'runlol'

def callicog_resume(pa, args):
	print(f'callicog{pa} resuming experiment {args.experiment} @{args.server}')
	return 'resumelol'

parser = argparse.ArgumentParser(prog='CALLICOG')
parser.add_argument('server', type=str)
subparsers = parser.add_subparsers(help='sub-command help')

parser_run = subparsers.add_parser('run', help='run help')
parser_run.add_argument('animal', type=str)
parser_run.add_argument('template', type=str)
parser_run.set_defaults(func=callicog_run)

parser_resume = subparsers.add_parser('resume', help='resume help')
parser_resume.add_argument('experiment', type=int)
parser_resume.set_defaults(func=callicog_resume)

args = parser.parse_args()
ret = args.func(2, args)
print(ret)