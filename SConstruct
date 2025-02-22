#!/usr/bin/env python
import os

# Local
import methods


env = Environment(tools=["default"], PLATFORM="")
env.msvc = False

# 构建选项
customs = ["custom.py"]
profile = ARGUMENTS.get("profile", "")
if profile:
    if os.path.isfile(profile):
        customs.append(profile)
    elif os.path.isfile(profile + ".py"):
        customs.append(profile + ".py")
opts = Variables(customs, ARGUMENTS)
opts.Add(BoolVariable("debug_symbols", "是否构建调试符号", False))
opts.Add(EnumVariable("warnings", "warning等级", "all", ("extra", "all", "moderate", "no")))
opts.Add(BoolVariable("compiledb", "是否生成compile_commands.json", False))
opts.Add(BoolVariable("werror", "是否视警告为错误", False))
opts.Update(env, {**ARGUMENTS, **env.Dictionary()})
Help(opts.GenerateHelpText(env))


# include目录
env.Append(CPPPATH=["src"])


# cpp文件
sources = []
for root, dirs, files in os.walk('src'):
    for f in files:
        if f.endswith('.cpp'):
            print('['+str(len(sources))+']' + root + '/' + f)
            sources.append(root + '/' + f)


# debug_symbols
if env["debug_symbols"]:
    # gcc ?
    env.Append(CCFLAGS=["-gdwarf-4"])
    env.Append(CCFLAGS=["-g3"])


# Enforce our minimal compiler version requirements
cc_version = methods.get_compiler_version(env) or {
    "major": None,
    "minor": None,
    "patch": None,
    "metadata1": None,
    "metadata2": None,
    "date": None,
}
cc_version_major = int(cc_version["major"] or -1)
cc_version_minor = int(cc_version["minor"] or -1)
cc_version_metadata1 = cc_version["metadata1"] or ""

# warnings
    # GCC, Clang
common_warnings = []
if methods.using_gcc(env):
    common_warnings += ["-Wshadow", "-Wno-misleading-indentation"]
    if cc_version_major == 7:  # Bogus warning fixed in 8+.
        common_warnings += ["-Wno-strict-overflow"]
    if cc_version_major < 11:
        # Regression in GCC 9/10, spams so much in our variadic templates
        # that we need to outright disable it.
        common_warnings += ["-Wno-type-limits"]
    if cc_version_major >= 12:  # False positives in our error macros, see GH-58747.
        common_warnings += ["-Wno-return-type"]
elif methods.using_clang(env) or methods.using_emcc(env):
    common_warnings += ["-Wshadow-field-in-constructor", "-Wshadow-uncaptured-local"]
    # We often implement `operator<` for structs of pointers as a requirement
    # for putting them in `Set` or `Map`. We don't mind about unreliable ordering.
    common_warnings += ["-Wno-ordered-compare-function-pointers"]

if env["warnings"] == "extra":
    env.Append(CCFLAGS=["-Wall", "-Wextra", "-Wwrite-strings", "-Wno-unused-parameter"] + common_warnings)
    env.Append(CXXFLAGS=["-Wctor-dtor-privacy", "-Wnon-virtual-dtor"])
    if methods.using_gcc(env):
        env.Append(
            CCFLAGS=[
                "-Walloc-zero",
                "-Wduplicated-branches",
                "-Wduplicated-cond",
                "-Wstringop-overflow=4",
            ]
        )
        env.Append(CXXFLAGS=["-Wplacement-new=1"])
        # Need to fix a warning with AudioServer lambdas before enabling.
        # if cc_version_major != 9:  # GCC 9 had a regression (GH-36325).
        #    env.Append(CXXFLAGS=["-Wnoexcept"])
        if cc_version_major >= 9:
            env.Append(CCFLAGS=["-Wattribute-alias=2"])
        if cc_version_major >= 11:  # Broke on MethodBind templates before GCC 11.
            env.Append(CCFLAGS=["-Wlogical-op"])
    elif methods.using_clang(env) or methods.using_emcc(env):
        env.Append(CCFLAGS=["-Wimplicit-fallthrough"])
elif env["warnings"] == "all":
    env.Append(CCFLAGS=["-Wall"] + common_warnings)
elif env["warnings"] == "moderate":
    env.Append(CCFLAGS=["-Wall", "-Wno-unused"] + common_warnings)
else:  # 'no'
    env.Append(CCFLAGS=["-w"])

if env["werror"]:
    env.Append(CCFLAGS=["-Werror"])


# 构建任务
default_args = [env.Program(target='main', source = sources)]

if env["compiledb"]:
    env.Tool("compilation_db")
    env.Alias("compiledb", env.CompilationDatabase())
    env.NoCache(env.CompilationDatabase())
    default_args += ["compiledb"]

env.Default(*default_args)
