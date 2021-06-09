"dockerjudge main functions"

from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import PurePosixPath

import docker

from . import processor as _processor
from . import test_case
from .dockerpy import exec_run, put_bin
from .status import Status


def judge(processor, source, tests, config=None, client=None):
    config = config or {}
    client = client or docker.from_env(version="auto")

    if isinstance(processor, str):
        processor = {
            "PyPy": _processor.PyPy(),
            "Python": _processor.Python(),
            "PyPy3": _processor.PyPy(),
            "Python3": _processor.Python(),
            "PyPy2": _processor.PyPy(version=2),
            "Python2": _processor.Python(version=2),

            "Cpp": _processor.GCC(language=_processor.GCC.Language.cpp),
            "C": _processor.GCC(language=_processor.GCC.Language.c),
            "Java": _processor.OpenJDK(),
        }[processor]
    else:
        try:
            processor = getattr(_processor, processor[0])(**processor[1])
        except TypeError:
            try:
                processor = getattr(_processor, processor[0])(*processor[1])
            except TypeError:
                pass


    container = client.containers.run(
        #processor.image,
        #'doj_allinone_timeout',
        "nvat/doj_allinone_timeout:v0.1", ### An all-in-one docker image that is on docker hub
        detach=True,
        tty=True,
        network_disabled=not config.get("network"),
    )
    try:
        return run(container, processor, source, tests, config)
    finally:
        container.remove(force=True)


def compile_source_code(container, processor, source, config):
    "Compile the source file"
    container.exec_run(f"mkdir -p {processor.workdir}/0")
    put_bin(
        container,
        PurePosixPath(f"{processor.workdir}/0/{processor.source}"),
        source,
    )

    exec_run(container, processor.before_compile, f"{processor.workdir}/0")
    exec_result = container.exec_run(
        processor.compile,
        workdir=f"{processor.workdir}/0",
        demux=config["demux"].get("compile", False),
    )
    if "compile" in config["callback"]:
        config["callback"]["compile"](
            exec_result.exit_code, exec_result.output
        )
    exec_run(container, processor.after_compile, f"{processor.workdir}/0")
    return exec_result


def judge_test_cases(container, processor, tests, config):
    "Judge test cases"
    with ThreadPoolExecutor(max_workers=config.get("threads")) as executor:
        futures = []
        for i, test in zip(range(len(tests)), tests):
            futures.append(
                executor.submit(
                    test_case.__init__,
                    container,
                    processor,
                    i + 1,
                    test,
                    config,
                )
            )
            futures[-1].add_done_callback(partial(done_callback, i, config))
    return [
        future.result()
        if not future.exception()
        else (Status.UE, (None, None), 0.0, 0)
        for future in futures
    ]


def done_callback(i, config, future):
    "Callback function for concurrent.futures.Future.add_done_callback"
    result = (
        (Status.UE, (None, None), 0.0, 0)
        if future.exception()
        else future.result()
    )
    try:
        config["callback"].get("judge")(i, *result)
    except TypeError:
        pass


def run(container, processor, source, tests, config=None):
    "Compile and judge"
    config.setdefault("callback", {})
    config.setdefault("demux", {})
    config.setdefault("iofilename", {})
    exec_result = compile_source_code(container, processor, source, config)
    if exec_result.exit_code:
        return [
            [(Status.CE, (None, None), 0.0, 0)] * len(tests),
            exec_result.output,
        ]

    res = judge_test_cases(container, processor, tests, config)
    return [res, exec_result.output]
