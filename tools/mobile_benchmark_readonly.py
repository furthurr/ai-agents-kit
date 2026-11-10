"""Restricted inspection entry points for benchmark participants."""
import os
from pathlib import Path
import subprocess
import stat
import sys

DENIED = {'.git', '.ssh', '.aws', '.config', 'build', '.gradle', 'node_modules'}
SUFFIXES = ('.pem', '.key', '.p12', '.pfx', '.jks', '.keystore')


def checked(root, value):
    path = Path(value)
    path = path if path.is_absolute() else Path.cwd() / path
    resolved = path.resolve()
    if resolved != root and root not in resolved.parents:
        raise ValueError('outside workspace')
    for part in path.parts + resolved.parts:
        if (part in DENIED or part.startswith('.env') or part.endswith(SUFFIXES)
                or part in {'.npmrc', '.pypirc', '.netrc', 'local.properties'}):
            raise ValueError('excluded path')
    return path


def main(root, tool, args):
    root = Path(root).resolve()
    checked(root, '.')
    if tool == 'head':
        count, files = 10, []
        iterator = iter(args)
        for value in iterator:
            if value == '-n':
                count = int(next(iterator))
            elif value.startswith('-') and value[1:].isdigit():
                count = int(value[1:])
            elif value.startswith('-'):
                raise ValueError('unsupported head option')
            else:
                files.append(checked(root, value))
        if not 0 <= count <= 10000:
            raise ValueError('unsupported head line count')
        def emit(stream):
            for _ in range(count):
                line = stream.readline()
                if not line:
                    break
                print(line, end='')
        if not files:
            emit(sys.stdin)
        for path in files:
            with path.open() as stream:
                emit(stream)
        return 0
    if tool == 'git':
        if not args or args[0] not in ('status', 'diff', 'ls-files'):
            raise ValueError('unsupported git operation')
        operation, values = args[0], args[1:]
        allowed = {
            'status': {'--short', '-s', '-b', '-sb', '--branch', '--porcelain', '--porcelain=v1',
                       '--untracked-files=all', '--untracked-files=normal', '--untracked-files=no'},
            'diff': {'--check', '--stat', '--shortstat', '--numstat', '--name-only', '--name-status',
                     '--no-color', '--no-ext-diff', '--no-textconv'},
            'ls-files': {'--cached', '--others', '--exclude-standard', '-z'},
        }[operation]
        for value in values:
            if value == '--' or value in allowed:
                continue
            if value.startswith('-'):
                raise ValueError('unsupported git option')
            checked(root, value)
            if ':' in value:
                raise ValueError('git object expressions are excluded')
        command = [os.environ['BENCHMARK_GIT'], operation]
        if operation == 'diff':
            command += ['--no-ext-diff', '--no-textconv']
        if operation != 'status':
            return subprocess.run([*command, *values], check=False).returncode
        # The frozen baseline lives in the index, without a synthetic commit.
        # Report only worktree changes, not thousands of staged baseline files.
        result = subprocess.run([*command, '--short', '--untracked-files=all', *values],
                                capture_output=True, text=True, check=False)
        for line in result.stdout.splitlines():
            if len(line) > 2 and (line.startswith('??') or line[1] != ' '):
                print((' ' + line[1:]) if line[0] == 'A' else line)
        return result.returncode
    if tool == 'ls':
        flags = [a for a in args if a.startswith('-')]
        if any(a != '--' and (a.startswith('--') or not set(a[1:]) <= set('alh1dAF')) for a in flags):
            raise ValueError('unsupported ls option')
        for value in [a for a in args if not a.startswith('-')] or ['.']:
            path = checked(root, value)
            for entry in sorted(path.iterdir() if path.is_dir() else [path]):
                try:
                    checked(root, str(entry))
                except ValueError:
                    continue
                print(entry.name)
        return 0
    if tool != 'rg':
        raise ValueError('unsupported command')
    options, positionals = [], []
    takes_value = {'-g', '--glob', '-t', '--type', '-e', '--regexp', '-A', '-B', '-C', '--max-count'}
    simple = {'-n', '--line-number', '-l', '--files-with-matches', '-i', '--ignore-case',
              '-S', '--smart-case', '-F', '--fixed-strings', '-w', '--word-regexp',
              '-c', '--count', '--files', '--hidden', '--no-heading', '--heading'}
    iterator = iter(args)
    for arg in iterator:
        if arg in takes_value:
            options.extend([arg, next(iterator)])
        elif arg in simple or (arg.startswith('-') and not arg.startswith('--')
                               and set(arg[1:]) <= set('nliSFwc')):
            options.append(arg)
        elif arg == '--':
            positionals.extend(iterator)
            break
        elif arg.startswith('-'):
            raise ValueError('unsupported rg option')
        else:
            positionals.append(arg)
    has_pattern = '-e' in options or '--regexp' in options or '--files' in options
    pattern = [] if has_pattern else [positionals.pop(0)]
    command = [os.environ['BENCHMARK_RG'], '--no-config', *options, *pattern]
    if not positionals and stat.S_ISFIFO(os.fstat(0).st_mode) and '--files' not in options:
        return subprocess.run(command, check=False).returncode
    files = []
    for value in positionals or ['.']:
        path = checked(root, value)
        if path.is_dir():
            for directory, dirs, names in os.walk(path, followlinks=False):
                dirs[:] = [d for d in dirs if d not in DENIED and not (Path(directory) / d).is_symlink()]
                for name in names:
                    try:
                        files.append(str(checked(root, str(Path(directory) / name))))
                    except ValueError:
                        continue
        else:
            files.append(str(path))
    if not files:
        return 1
    return subprocess.run([*command, '--', *files], check=False).returncode


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3:]))
    except (ValueError, StopIteration, OSError, IndexError) as error:
        print('Restricted read-only command: ' + str(error), file=sys.stderr)
        sys.exit(2)
