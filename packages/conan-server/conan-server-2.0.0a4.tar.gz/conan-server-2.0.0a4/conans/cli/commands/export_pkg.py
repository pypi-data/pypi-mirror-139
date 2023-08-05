import os

from conans.cli.command import conan_command, COMMAND_GROUPS, OnceArgument
from conans.cli.commands import make_abs_path
from conans.cli.commands.install import _get_conanfile_path
from conans.cli.common import get_lockfile, add_profiles_args, get_profiles_from_args


@conan_command(group=COMMAND_GROUPS['creator'])
def export_pkg(conan_api, parser, *args, **kwargs):
    """
    Export recipe to the Conan package cache
    """
    parser.add_argument("path", help="Path to a folder containing a recipe (conanfile.py)")

    parser.add_argument("--name", action=OnceArgument,
                        help='Provide a package name if not specified in conanfile')
    parser.add_argument("--version", action=OnceArgument,
                        help='Provide a package version if not specified in conanfile')
    parser.add_argument("--user", action=OnceArgument,
                        help='Provide a user')
    parser.add_argument("--channel", action=OnceArgument,
                        help='Provide a channel')
    parser.add_argument("-j", "--json", default=None, action=OnceArgument,
                        help='Path to a json file where the install information will be '
                             'written')
    parser.add_argument("-l", "--lockfile", action=OnceArgument,
                        help="Path to a lockfile.")
    parser.add_argument("--lockfile-out", action=OnceArgument,
                        help="Filename of the updated lockfile")
    parser.add_argument("--ignore-dirty", default=False, action='store_true',
                        help='When using the "scm" feature with "auto" values, capture the'
                             ' revision and url even if there are uncommitted changes')
    add_profiles_args(parser)
    args = parser.parse_args(*args)

    cwd = os.getcwd()
    lockfile_path = make_abs_path(args.lockfile, cwd)
    lockfile = get_lockfile(lockfile=lockfile_path, strict=True)
    path = _get_conanfile_path(args.path, cwd, py=None) if args.path else None
    profile_host, profile_build = get_profiles_from_args(conan_api, args)

    ref = conan_api.export.export(path=path,
                                  name=args.name,
                                  version=args.version,
                                  user=args.user,
                                  channel=args.channel,
                                  lockfile=lockfile,
                                  ignore_dirty=args.ignore_dirty)

    # TODO: Maybe we want to be able to export-pkg it as --build-require
    root_node = conan_api.graph.load_root_virtual_conanfile(ref, profile_host)
    deps_graph = conan_api.graph.load_graph(root_node, profile_host=profile_host,
                                            profile_build=profile_build,
                                            lockfile=lockfile,
                                            remotes=None,
                                            update=None)
    conan_api.graph.analyze_binaries(deps_graph, build_mode=[ref.name])
    deps_graph.report_graph_error()

    conan_api.export.export_pkg(deps_graph, path)

    if args.lockfile_out:
        lockfile_out = make_abs_path(args.lockfile_out, cwd)
        lockfile.save(lockfile_out)
